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

        return types.List([types.FolderInviteLink._parse(invite) for invite in r.invites])
