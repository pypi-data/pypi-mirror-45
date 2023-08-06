import asyncio
import itertools
import random
import time
import datetime

from .users import UserMethods
from .. import events, utils, errors
from ..tl import types, functions
from ..events.common import EventCommon
from ..statecache import StateCache


class UpdateMethods(UserMethods):

    # region Public methods

    async def _run_until_disconnected(self):
        try:
            await self.disconnected
        except KeyboardInterrupt:
            pass
        finally:
            await self.disconnect()

    def run_until_disconnected(self):
        """
        Runs the event loop until `disconnect` is called or if an error
        while connecting/sending/receiving occurs in the background. In
        the latter case, said error will ``raise`` so you have a chance
        to ``except`` it on your own code.

        If the loop is already running, this method returns a coroutine
        that you should await on your own code.
        """
        if self.loop.is_running():
            return self._run_until_disconnected()
        try:
            return self.loop.run_until_complete(self.disconnected)
        except KeyboardInterrupt:
            pass
        finally:
            # No loop.run_until_complete; it's already syncified
            self.disconnect()

    def on(self, event):
        """
        Decorator helper method around `add_event_handler`. Example:

        >>> from telethon import TelegramClient, events
        >>> client = TelegramClient(...)
        >>>
        >>> @client.on(events.NewMessage)
        ... async def handler(event):
        ...     ...
        ...
        >>>

        Args:
            event (`_EventBuilder` | `type`):
                The event builder class or instance to be used,
                for instance ``events.NewMessage``.
        """
        def decorator(f):
            self.add_event_handler(f, event)
            return f

        return decorator

    def add_event_handler(self, callback, event=None):
        """
        Registers the given callback to be called on the specified event.

        Args:
            callback (`callable`):
                The callable function accepting one parameter to be used.

                Note that if you have used `telethon.events.register` in
                the callback, ``event`` will be ignored, and instead the
                events you previously registered will be used.

            event (`_EventBuilder` | `type`, optional):
                The event builder class or instance to be used,
                for instance ``events.NewMessage``.

                If left unspecified, `telethon.events.raw.Raw` (the
                :tl:`Update` objects with no further processing) will
                be passed instead.
        """
        builders = events._get_handlers(callback)
        if builders is not None:
            for event in builders:
                self._event_builders.append((event, callback))
            return

        if isinstance(event, type):
            event = event()
        elif not event:
            event = events.Raw()

        self._event_builders.append((event, callback))

    def remove_event_handler(self, callback, event=None):
        """
        Inverse operation of :meth:`add_event_handler`.

        If no event is given, all events for this callback are removed.
        Returns how many callbacks were removed.
        """
        found = 0
        if event and not isinstance(event, type):
            event = type(event)

        i = len(self._event_builders)
        while i:
            i -= 1
            ev, cb = self._event_builders[i]
            if cb == callback and (not event or isinstance(ev, event)):
                del self._event_builders[i]
                found += 1

        return found

    def list_event_handlers(self):
        """
        Lists all added event handlers, returning a list of pairs
        consisting of (callback, event).
        """
        return [(callback, event) for event, callback in self._event_builders]

    async def catch_up(self):
        """
        "Catches up" on the missed updates while the client was offline.
        You should call this method after registering the event handlers
        so that the updates it loads can by processed by your script.

        This can also be used to forcibly fetch new updates if there are any.
        """
        pts, date = self._state_cache[None]
        self.session.catching_up = True
        try:
            while True:
                d = await self(functions.updates.GetDifferenceRequest(
                    pts, date, 0
                ))
                if isinstance(d, (types.updates.DifferenceSlice,
                                  types.updates.Difference)):
                    if isinstance(d, types.updates.Difference):
                        state = d.state
                    else:
                        state = d.intermediate_state

                    pts, date = state.pts, state.date
                    self._handle_update(types.Updates(
                        users=d.users,
                        chats=d.chats,
                        date=state.date,
                        seq=state.seq,
                        updates=d.other_updates + [
                            types.UpdateNewMessage(m, 0, 0)
                            for m in d.new_messages
                        ]
                    ))

                    # TODO Implement upper limit (max_pts)
                    # We don't want to fetch updates we already know about.
                    #
                    # We may still get duplicates because the Difference
                    # contains a lot of updates and presumably only has
                    # the state for the last one, but at least we don't
                    # unnecessarily fetch too many.
                    #
                    # updates.getDifference's pts_total_limit seems to mean
                    # "how many pts is the request allowed to return", and
                    # if there is more than that, it returns "too long" (so
                    # there would be duplicate updates since we know about
                    # some). This can be used to detect collisions (i.e.
                    # it would return an update we have already seen).
                else:
                    if isinstance(d, types.updates.DifferenceEmpty):
                        date = d.date
                    elif isinstance(d, types.updates.DifferenceTooLong):
                        pts = d.pts
                    break
        except (ConnectionError, asyncio.CancelledError):
            pass
        finally:
            # TODO Save new pts to session
            self._state_cache._pts_date = (pts, date)
            self.session.catching_up = False

    # endregion

    # region Private methods

    # It is important to not make _handle_update async because we rely on
    # the order that the updates arrive in to update the pts and date to
    # be always-increasing. There is also no need to make this async.
    def _handle_update(self, update):
        self.session.process_entities(update)
        self._entity_cache.add(update)

        if isinstance(update, (types.Updates, types.UpdatesCombined)):
            entities = {utils.get_peer_id(x): x for x in
                        itertools.chain(update.users, update.chats)}
            for u in update.updates:
                self._process_update(u, entities)
        elif isinstance(update, types.UpdateShort):
            self._process_update(update.update)
        else:
            self._process_update(update)

        self._state_cache.update(update)

    def _process_update(self, update, entities=None):
        update._entities = entities or {}

        # This part is somewhat hot so we don't bother patching
        # update with channel ID/its state. Instead we just pass
        # arguments which is faster.
        channel_id = self._state_cache.get_channel_id(update)
        args = (update, channel_id, self._state_cache[channel_id])
        if self._updates_queue is None:
            self._loop.create_task(self._dispatch_update(*args))
        else:
            self._updates_queue.put_nowait(args)
            if not self._dispatching_updates_queue.is_set():
                self._dispatching_updates_queue.set()
                self._loop.create_task(self._dispatch_queue_updates())

        self._state_cache.update(update)

    async def _update_loop(self):
        # Pings' ID don't really need to be secure, just "random"
        rnd = lambda: random.randrange(-2**63, 2**63)
        while self.is_connected():
            try:
                await asyncio.wait_for(
                    self.disconnected, timeout=60, loop=self._loop
                )
                continue  # We actually just want to act upon timeout
            except asyncio.TimeoutError:
                pass
            except asyncio.CancelledError:
                return
            except Exception:
                continue  # Any disconnected exception should be ignored

            # We also don't really care about their result.
            # Just send them periodically.
            try:
                self._sender.send(functions.PingRequest(rnd()))
            except (ConnectionError, asyncio.CancelledError):
                return

            # Entities and cached files are not saved when they are
            # inserted because this is a rather expensive operation
            # (default's sqlite3 takes ~0.1s to commit changes). Do
            # it every minute instead. No-op if there's nothing new.
            self.session.save()

            # We need to send some content-related request at least hourly
            # for Telegram to keep delivering updates, otherwise they will
            # just stop even if we're connected. Do so every 30 minutes.
            #
            # TODO Call getDifference instead since it's more relevant
            if time.time() - self._last_request > 30 * 60:
                if not await self.is_user_authorized():
                    # What can be the user doing for so
                    # long without being logged in...?
                    continue

                try:
                    await self(functions.updates.GetStateRequest())
                except (ConnectionError, asyncio.CancelledError):
                    return

    async def _dispatch_queue_updates(self):
        while not self._updates_queue.empty():
            await self._dispatch_update(*self._updates_queue.get_nowait())

        self._dispatching_updates_queue.clear()

    async def _dispatch_update(self, update, channel_id, pts_date):
        built = EventBuilderDict(self, update)
        if self._conversations:
            for conv in self._conversations.values():
                ev = built[events.NewMessage]
                if ev:
                    if not ev._load_entities():
                        await ev._get_difference(channel_id, pts_date)
                    conv._on_new_message(ev)

                ev = built[events.MessageEdited]
                if ev:
                    if not ev._load_entities():
                        await ev._get_difference(channel_id, pts_date)
                    conv._on_edit(ev)

                ev = built[events.MessageRead]
                if ev:
                    if not ev._load_entities():
                        await ev._get_difference(channel_id, pts_date)
                    conv._on_read(ev)

                if conv._custom:
                    await conv._check_custom(built, channel_id, pts_date)

        for builder, callback in self._event_builders:
            event = built[type(builder)]
            if not event:
                continue

            if not builder.resolved:
                await builder.resolve(self)

            if not builder.filter(event):
                continue

            try:
                # Although needing to do this constantly is annoying and
                # error-prone, this part is somewhat hot, and always doing
                # `await` for `check_entities_and_get_difference` causes
                # unnecessary work. So we need to call a function that
                # doesn't cause a task switch.
                if isinstance(event, EventCommon) and not event._load_entities():
                    await event._get_difference(channel_id, pts_date)

                await callback(event)
            except errors.AlreadyInConversationError:
                name = getattr(callback, '__name__', repr(callback))
                self._log[__name__].debug(
                    'Event handler "%s" already has an open conversation, '
                    'ignoring new one', name)
            except events.StopPropagation:
                name = getattr(callback, '__name__', repr(callback))
                self._log[__name__].debug(
                    'Event handler "%s" stopped chain of propagation '
                    'for event %s.', name, type(event).__name__
                )
                break
            except Exception:
                name = getattr(callback, '__name__', repr(callback))
                self._log[__name__].exception('Unhandled exception on %s',
                                              name)

    async def _handle_auto_reconnect(self):
        # TODO Catch-up
        return
        try:
            self._log[__name__].info(
                'Asking for the current state after reconnect...')

            # TODO consider:
            # If there aren't many updates while the client is disconnected
            # (I tried with up to 20), Telegram seems to send them without
            # asking for them (via updates.getDifference).
            #
            # On disconnection, the library should probably set a "need
            # difference" or "catching up" flag so that any new updates are
            # ignored, and then the library should call updates.getDifference
            # itself to fetch them.
            #
            # In any case (either there are too many updates and Telegram
            # didn't send them, or there isn't a lot and Telegram sent them
            # but we dropped them), we fetch the new difference to get all
            # missed updates. I feel like this would be the best solution.

            # If a disconnection occurs, the old known state will be
            # the latest one we were aware of, so we can catch up since
            # the most recent state we were aware of.
            await self.catch_up()

            self._log[__name__].info('Successfully fetched missed updates')
        except errors.RPCError as e:
            self._log[__name__].warning('Failed to get missed updates after '
                                        'reconnect: %r', e)
        except Exception:
            self._log[__name__].exception('Unhandled exception while getting '
                                          'update difference after reconnect')

    # endregion


class EventBuilderDict:
    """
    Helper "dictionary" to return events from types and cache them.
    """
    def __init__(self, client, update):
        self.client = client
        self.update = update

    def __getitem__(self, builder):
        try:
            return self.__dict__[builder]
        except KeyError:
            event = self.__dict__[builder] = builder.build(self.update)
            if isinstance(event, EventCommon):
                event.original_update = self.update
                event._set_client(self.client)
            elif event:
                event._client = self.client

            return event
