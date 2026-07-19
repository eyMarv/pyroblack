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

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class MessageOrigin(Object):
    """This object describes the origin of a message.

    It can be one of:

    - :obj:`~pyrogram.types.MessageOriginUser`
    - :obj:`~pyrogram.types.MessageOriginHiddenUser`
    - :obj:`~pyrogram.types.MessageOriginChat`
    - :obj:`~pyrogram.types.MessageOriginChannel`
    - :obj:`~pyrogram.types.MessageImportInfo`

    """

    def __init__(
        self,
        type: str,
        date: datetime | None = None,
    ) -> None:
        super().__init__()

        self.type = type
        self.date = date

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        forward_header: raw.types.MessageFwdHeader,
        users: dict,  # raw
        chats: dict,  # raw
    ) -> MessageOrigin:
        if not forward_header:
            return None
        forward_date = utils.timestamp_to_datetime(forward_header.date)
        forward_signature = getattr(forward_header, "post_author", None)
        if forward_header.from_id:
            raw_peer_id = utils.get_raw_peer_id(forward_header.from_id)
            peer_id = utils.get_peer_id(forward_header.from_id)
            if peer_id > 0:
                forward_from = types.User._parse(client, users[raw_peer_id])
                return types.MessageOriginUser(
                    date=forward_date,
                    sender_user=forward_from,
                )
            forward_from_chat = types.Chat._parse_channel_chat(
                client, chats[raw_peer_id]
            )
            forward_from_message_id = forward_header.channel_post
            if forward_from_message_id:
                return types.MessageOriginChannel(
                    date=forward_date,
                    chat=forward_from_chat,
                    message_id=forward_from_message_id,
                    author_signature=forward_signature,
                )
            return types.MessageOriginChat(
                date=forward_date,
                sender_chat=forward_from_chat,
                author_signature=forward_signature,
            )
        if forward_header.imported:
            return types.MessageImportInfo(
                date=forward_date,
                sender_user_name=forward_header.from_name or forward_signature,
            )
        if forward_header.from_name:
            forward_sender_name = forward_header.from_name
            return types.MessageOriginHiddenUser(
                date=forward_date,
                sender_user_name=forward_sender_name,
            )
        return None
