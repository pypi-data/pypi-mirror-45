# mautrix-facebook - A Matrix-Facebook Messenger puppeting bridge
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Optional, Dict, List, Awaitable, Iterator
from abc import ABC, abstractmethod
from itertools import chain
import asyncio
import logging

from aiohttp import ClientConnectionError

from mautrix.types import (UserID, FilterID, Filter, RoomEventFilter, RoomFilter, EventFilter,
                           EventType, SyncToken, RoomID, Event, PresenceState)
from mautrix.appservice import AppService, IntentAPI
from mautrix.errors import IntentError, MatrixRequestError

from . import matrix as m


class CustomPuppetError(Exception):
    """Base class for double puppeting setup errors."""


class InvalidAccessToken(CustomPuppetError):
    def __init__(self):
        super().__init__("The given access token was invalid.")


class OnlyLoginSelf(CustomPuppetError):
    def __init__(self):
        super().__init__("You may only replace your puppet with your own Matrix account.")


class CustomPuppetMixin(ABC):
    sync_with_custom_puppets: bool = True

    az: AppService
    loop: asyncio.AbstractEventLoop
    log: logging.Logger
    mx: m.MatrixHandler

    by_custom_mxid: Dict[UserID, 'CustomPuppetMixin']

    default_mxid: UserID
    default_mxid_intent: IntentAPI
    custom_mxid: Optional[UserID]
    access_token: Optional[str]

    intent: IntentAPI
    sync_task: asyncio.Future

    @abstractmethod
    def save(self) -> None:
        pass

    @property
    def mxid(self) -> UserID:
        return self.custom_mxid or self.default_mxid

    @property
    def is_real_user(self) -> bool:
        return bool(self.custom_mxid and self.access_token)

    def _fresh_intent(self) -> IntentAPI:
        return (self.az.intent.user(self.custom_mxid, self.access_token)
                if self.is_real_user else self.default_mxid_intent)

    async def switch_mxid(self, access_token: Optional[str], mxid: Optional[UserID]) -> None:
        prev_mxid = self.custom_mxid
        self.custom_mxid = mxid
        self.access_token = access_token
        self.intent = self._fresh_intent()

        await self.init_custom_mxid()

        try:
            del self.by_custom_mxid[prev_mxid]  # type: ignore
        except KeyError:
            pass
        if self.mxid != self.default_mxid:
            self.by_custom_mxid[self.mxid] = self
            await self._leave_rooms_with_default_user()
        self.save()

    async def init_custom_mxid(self) -> None:
        if not self.is_real_user:
            return

        mxid = await self.intent.whoami()
        if not mxid or mxid != self.custom_mxid:
            self.custom_mxid = None
            self.access_token = None
            self.intent = self._fresh_intent()
            if mxid != self.custom_mxid:
                raise OnlyLoginSelf()
            raise InvalidAccessToken()
        if self.sync_with_custom_puppets:
            self.log.debug(f"Initialized custom mxid: {mxid}. Starting sync task")
            self.sync_task = asyncio.ensure_future(self.sync(), loop=self.loop)
        else:
            self.log.debug(f"Initialized custom mxid: {mxid}. Not starting sync task")

    def default_puppet_should_leave_room(self, room_id: RoomID) -> bool:
        return True

    async def _leave_rooms_with_default_user(self) -> None:
        for room_id in await self.default_mxid_intent.get_joined_rooms():
            try:
                if self.default_puppet_should_leave_room(room_id):
                    await self.default_mxid_intent.leave_room(room_id)
                    await self.intent.ensure_joined(room_id)
            except (IntentError, MatrixRequestError):
                pass

    def _create_sync_filter(self) -> Awaitable[FilterID]:
        return self.intent.create_filter(Filter(
            account_data=EventFilter(types=[]),
            room=RoomFilter(
                include_leave=False,
                state=RoomEventFilter(types=[]),
                timeline=RoomEventFilter(types=[]),
                account_data=RoomEventFilter(types=[]),
                ephemeral=RoomEventFilter(types=[
                    EventType.TYPING,
                    EventType.RECEIPT,
                ]),
            ),
            presence=EventFilter(
                types=[EventType.PRESENCE],
                senders=[self.custom_mxid],
            )
        ))

    def _filter_events(self, room_id: RoomID, events: List[Dict]) -> Iterator[Event]:
        # We only want events about the custom puppet user, but we can't use
        # filters for typing and read receipt events.
        for event in events:
            event["room_id"] = room_id
            evt_type = EventType.find(event.get("type", None))
            event.setdefault("content", {})
            if evt_type == EventType.TYPING:
                is_typing = self.custom_mxid in event["content"].get("user_ids", [])
                event["content"]["user_ids"] = [self.custom_mxid] if is_typing else []
            elif evt_type == EventType.RECEIPT:
                val = None
                evt = None
                for event_id in event["content"]:
                    try:
                        val = event["content"][event_id]["m.read"][self.custom_mxid]
                        evt = event_id
                        break
                    except KeyError:
                        pass
                if val and evt:
                    event["content"] = {evt: {"m.read": {
                        self.custom_mxid: val
                    }}}
                else:
                    continue
            yield event

    def handle_sync(self, sync_resp: Dict) -> None:
        # Get events from rooms -> join -> [room_id] -> ephemeral -> events (array)
        ephemeral_events = (
            event
            for room_id, data in sync_resp.get("rooms", {}).get("join", {}).items()
            for event in self._filter_events(room_id, data.get("ephemeral", {}).get("events", []))
        )

        # Get events from presence -> events (array)
        presence_events = sync_resp.get("presence", {}).get("events", [])

        # Deserialize and handle all events
        coro = asyncio.gather(*[self.mx.try_handle_event(Event.deserialize(event))
                                for event in chain(ephemeral_events, presence_events)],
                              loop=self.loop)
        asyncio.ensure_future(coro, loop=self.loop)

    async def sync(self) -> None:
        try:
            await self._sync()
        except asyncio.CancelledError:
            self.log.info("Syncing cancelled")
        except Exception:
            self.log.exception("Fatal error syncing")

    async def _sync(self) -> None:
        if not self.is_real_user:
            self.log.warning("Called sync() for non-custom puppet.")
            return
        custom_mxid: UserID = self.custom_mxid
        access_token_at_start: str = self.access_token
        errors: int = 0
        next_batch: Optional[SyncToken] = None
        filter_id: FilterID = await self._create_sync_filter()
        self.log.debug(f"Starting syncer for {custom_mxid} with sync filter {filter_id}.")
        while access_token_at_start == self.access_token:
            try:
                sync_resp = await self.intent.sync(filter_id=filter_id, since=next_batch,
                                                   set_presence=PresenceState.OFFLINE)
                errors = 0
                if next_batch is not None:
                    self.handle_sync(sync_resp)
                next_batch = sync_resp.get("next_batch", None)
            except (MatrixRequestError, ClientConnectionError) as e:
                wait = min(errors, 11) ** 2
                self.log.warning(f"Syncer for {custom_mxid} errored: {e}. "
                                 f"Waiting for {wait} seconds...")
                errors += 1
                await asyncio.sleep(wait)
        self.log.debug(f"Syncer for custom puppet {custom_mxid} stopped.")
