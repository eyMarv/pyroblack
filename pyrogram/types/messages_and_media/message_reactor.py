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

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class MessageReactor(Object):
    """Contains information about a message reactor.

    Parameters
    ----------
        amount (``int``):
            Stars amount.

        is_top (``bool``, *optional*):
            True, if reactor is top.

        is_my (``bool``, *optional*):
            True, if the reaction is mine.

        is_anonymous (``bool``, *optional*):
            True, if reactor is anonymous.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Information about the reactor.

        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Information about the sender chat.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        amount: int,
        is_top: bool | None = None,
        is_my: bool | None = None,
        is_anonymous: bool | None = None,
        from_user: types.User = None,
        sender_chat: types.Chat = None,
    ) -> None:
        super().__init__(client)

        self.amount = amount
        self.is_top = is_top
        self.is_my = is_my
        self.is_anonymous = is_anonymous
        self.from_user = from_user
        self.sender_chat = sender_chat

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        message_reactor: raw.base.MessageReactor | None = None,
        users: dict[int, raw.types.User] | None = None,
        chats: dict[int, raw.types.Chat] | None = None,
    ) -> MessageReactor | None:
        if not message_reactor:
            return None

        is_anonymous = message_reactor.anonymous
        from_user = None
        sender_chat = None
        if not is_anonymous:
            if isinstance(message_reactor.peer_id, raw.types.PeerUser):
                from_user = types.User._parse(
                    client,
                    users.get(message_reactor.peer_id.user_id),
                )
            elif isinstance(message_reactor.peer_id, raw.types.PeerChannel):
                sender_chat = types.Chat._parse_channel_chat(
                    client,
                    chats.get(message_reactor.peer_id.channel_id),
                )

        return MessageReactor(
            client=client,
            amount=message_reactor.count,
            is_top=message_reactor.top,
            is_my=message_reactor.my,
            is_anonymous=is_anonymous,
            from_user=from_user,
            sender_chat=sender_chat,
        )
