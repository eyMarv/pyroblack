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

from typing import TYPE_CHECKING

from pyrogram import raw, types, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class UpgradedGiftOriginalDetails(Object):
    """Describes the original details about the gift.

    Parameters
    ----------
        sender (:obj:`~pyrogram.types.Chat`, *optional*):
            Identifier of the user or the chat that sent the gift.

        receiver (:obj:`~pyrogram.types.Chat`, *optional*):
            Identifier of the user or the chat that received the gift.

        text (:obj:`~pyrogram.types.FormattedText`, *optional*):
            Message added to the gift.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the gift was sent.

    """

    def __init__(
        self,
        *,
        sender: types.Chat | None = None,
        receiver: types.Chat | None = None,
        text: types.FormattedText | None = None,
        date: datetime | None = None,
    ) -> None:
        super().__init__()

        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.date = date

    @staticmethod
    async def _parse(
        client,
        attr: raw.types.StarGiftAttributeOriginalDetails,
        users: dict[int, raw.base.User],
        chats: dict[int, raw.base.Chat],
    ) -> UpgradedGiftOriginalDetails:
        sender_id = utils.get_raw_peer_id(attr.sender_id)
        recipient_id = utils.get_raw_peer_id(attr.recipient_id)

        return UpgradedGiftOriginalDetails(
            sender=types.User._parse(
                client, users.get(sender_id) or chats.get(sender_id)
            ),
            receiver=types.User._parse(
                client, users.get(recipient_id) or chats.get(recipient_id)
            ),
            text=types.FormattedText._parse(client, attr.message),
            date=utils.timestamp_to_datetime(attr.date),
        )
