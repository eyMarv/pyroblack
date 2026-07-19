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

from typing import Union

import pyrogram
from pyrogram import raw, types
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from pyrogram.types.object import Object
from pyrogram.types.update import Update


class StoryDeleted(Object, Update):
    """A deleted story.

    Parameters
    ----------
        id (``int``):
            Unique story identifier.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Sender of the story.

        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Sender of the story. If the story is from channel.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
    ) -> None:
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.sender_chat = sender_chat

    async def _parse(
        self: "pyrogram.Client",
        stories: raw.base.StoryItem,
        peer: Union["raw.types.PeerChannel", "raw.types.PeerUser"],
    ) -> "StoryDeleted":
        from_user = None
        sender_chat = None
        try:
            if isinstance(peer, raw.types.PeerChannel):
                sender_chat = await self.get_chat(peer.channel_id)
            elif isinstance(peer, raw.types.InputPeerSelf):
                from_user = self.me
            else:
                from_user = await self.get_users(peer.user_id)
        except PeerIdInvalid:
            pass

        return StoryDeleted(
            id=stories.id,
            from_user=from_user,
            sender_chat=sender_chat,
            client=self,
        )
