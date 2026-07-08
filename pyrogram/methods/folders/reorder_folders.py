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
from pyrogram import raw


class ReorderFolders:
    async def reorder_folders(
        self: "pyrogram.Client",
        folder_ids: List[int],
        main_chat_list_position: int = 0
    ) -> bool:
        """Change the order of chat folders.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            folder_ids (List of ``int``):
                Identifiers of chat folders in the new correct order.

            main_chat_list_position (``int``, *optional*):
                Position of the main chat list among chat folders, 0-based.
                Can be non-zero only for Premium users.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Reorder folders
                await app.reorder_folders([2, 5, 4])
        """
        if main_chat_list_position:
            folder_ids.insert(main_chat_list_position, 0)

        r = await self.invoke(
            raw.functions.messages.UpdateDialogFiltersOrder(
                order=folder_ids
            )
        )

        return r
