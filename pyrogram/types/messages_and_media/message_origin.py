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

from datetime import datetime
from typing import Dict, Optional

import pyrogram
from pyrogram import enums, raw, types, utils

from ..object import Object


class MessageOrigin(Object):
    """This object describes the origin of a message.

    It can be one of:

    - :obj:`~pyrogram.types.MessageOriginChannel`
    - :obj:`~pyrogram.types.MessageOriginChat`
    - :obj:`~pyrogram.types.MessageOriginHiddenUser`
    - :obj:`~pyrogram.types.MessageOriginImport`
    - :obj:`~pyrogram.types.MessageOriginUser`
    """

    def __init__(
        self, type: "enums.MessageOriginType", date: Optional[datetime] = None
    ):
        super().__init__()

        self.type = type
        self.date = date

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        fwd_from: "raw.types.MessageFwdHeader",
        users: Dict[int, "raw.base.User"],
        chats: Dict[int, "raw.base.Chat"],
    ) -> Optional["MessageOrigin"]:
        if not fwd_from:
            return None

        forward_date = utils.timestamp_to_datetime(fwd_from.date)

        if fwd_from.from_id:
            raw_peer_id = utils.get_raw_peer_id(fwd_from.from_id)
            peer_id = utils.get_peer_id(fwd_from.from_id)
            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                return types.MessageOriginUser(
                    date=forward_date,
                    sender_user=types.User._parse(client, users.get(raw_peer_id)),
                )
            else:
                if fwd_from.channel_post:
                    return types.MessageOriginChannel(
                        date=forward_date,
                        chat=types.Chat._parse_channel_chat(
                            client, chats.get(raw_peer_id)
                        ),
                        message_id=fwd_from.channel_post,
                        author_signature=fwd_from.post_author,
                    )
                else:
                    return types.MessageOriginChat(
                        date=forward_date,
                        sender_chat=types.Chat._parse_channel_chat(
                            client, chats.get(raw_peer_id)
                        ),
                        author_signature=fwd_from.post_author,
                    )
        elif fwd_from.from_name:
            return types.MessageOriginHiddenUser(
                date=forward_date, sender_user_name=fwd_from.from_name
            )
        elif fwd_from.imported:
            return types.MessageOriginImport(
                date=forward_date, sender_user_name=fwd_from.post_author
            )
