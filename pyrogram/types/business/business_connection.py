#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2024 Dan <https://github.com/delivrance>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  This file is part of Pyroblack.
#
#  Pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  Pyroblack is a continuation fork of Pyrogram <https://github.com/pyrogram/pyrogram>
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pyrogram import raw, types, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime

log = logging.getLogger(__name__)


class BusinessConnection(Object):
    """Describes the connection of the bot with a business account.

    Parameters
    ----------
        id (``str``):
            Unique identifier of the business connection

        user (:obj:`~pyrogram.types.User`):
            Business account user that created the business connection

        user_chat_id (``int``):
            Identifier of a private chat with the user who created the business connection. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.

        date (:py:obj:`~datetime.datetime`):
            Date the connection was established in Unix time

        rights (:obj:`~pyrogram.types.BusinessBotRights`, *optional*):
            Rights of the business bot.

        is_enabled (``bool``):
            True, if the connection is active

    """

    def __init__(
        self,
        *,
        id: str | None = None,
        user: types.User = None,
        user_chat_id: int | None = None,
        date: datetime,
        rights: types.BusinessBotRights | None = None,
        is_enabled: bool | None = None,
        _raw: raw.types.UpdateBotBusinessConnect = None,
    ) -> None:
        super().__init__()

        self.id = id
        self.user = user
        self.user_chat_id = user_chat_id
        self.date = date
        self.rights = rights
        self.is_enabled = is_enabled
        self._raw = _raw

    @staticmethod
    def _parse(
        client,
        business_connect_update: raw.types.UpdateBotBusinessConnect,
        users: dict,
        chats: dict,
    ) -> BusinessConnection:
        return BusinessConnection(
            _raw=business_connect_update,
            id=business_connect_update.connection.connection_id,
            user=types.User._parse(
                client,
                users[business_connect_update.connection.user_id],
            ),
            user_chat_id=business_connect_update.connection.user_id,
            date=utils.timestamp_to_datetime(business_connect_update.connection.date),
            rights=types.BusinessBotRights._parse(
                client,
                business_connect_update.connection.rights,
            ),
            is_enabled=not bool(
                getattr(business_connect_update.connection, "disabled", None)
            ),
        )

    @property
    def can_reply(self) -> str:
        log.warning(
            "This property is deprecated. Please use rights instead",
        )
        if self.rights:
            return self.rights.can_reply
        return False
