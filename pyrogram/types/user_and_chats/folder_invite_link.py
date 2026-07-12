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

from typing import List, Optional

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
        name: Optional[str] = None,
        chat_ids: Optional[List[int]] = None
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

