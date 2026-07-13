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

from typing import List
import pyrogram
from pyrogram import raw, types


class GetFolderInviteLinks:
    async def get_folder_invite_links(
        self: "pyrogram.Client",
        chat_folder_id: int
    ) -> List["types.FolderInviteLink"]:
        """Returns invite links created by the current user for a shareable chat folder.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_folder_id (``int``):
                Unique identifier (int) of the target folder.

        Returns:
            List of :obj:`~pyrogram.types.FolderInviteLink`: On success, information about the invite links is returned.

        Example:
            .. code-block:: python

                # Get all folder links
                await app.get_folder_invite_links(folder_id)
        """
        r = await self.invoke(
            raw.functions.chatlists.GetExportedInvites(
                chatlist=raw.types.InputChatlistDialogFilter(filter_id=chat_folder_id)
            )
        )

        return types.List([types.FolderInviteLink._parse(r) for r in r.invites])
