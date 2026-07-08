#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from typing import List

from pyrogram import raw, types, utils
from ..object import Object


class FolderInviteLink(Object):
    """Contains a chat folder invite link.

    Parameters:
        invite_link (``str``):
            The chat folder invite link.

        name (``str``, *optional*):
            Name of the link.

        chat_ids (List of ``int``, *optional*):
            Identifiers of chats, included in the link.
    """

    def __init__(
        self,
        *,
        invite_link: str,
        name: str = None,
        chat_ids: List[int] = None
    ):
        super().__init__()

        self.invite_link = invite_link
        self.name = name
        self.chat_ids = chat_ids

    @staticmethod
    def _parse(invite: "raw.base.ExportedChatlistInvite") -> "FolderInviteLink":
        return FolderInviteLink(
            invite_link=invite.url,
            name=invite.title,
            chat_ids=types.List([utils.get_peer_id(peer) for peer in invite.peers])
        )
