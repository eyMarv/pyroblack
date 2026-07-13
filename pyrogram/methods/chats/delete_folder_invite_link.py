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

import re

import pyrogram
from pyrogram import raw


class DeleteFolderInviteLink:
    async def delete_folder_invite_link(
        self: "pyrogram.Client",
        chat_folder_id: int,
        invite_link: str
    ) -> bool:
        """Deletes an invite link for a chat folder.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_folder_id (``int``):
                Unique identifier (int) of the target folder.

            invite_link (``str``):
                Invite link to be edited.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Delete folder link
                await app.delete_folder_invite_link(
                    chat_folder_id=folder_id,
                    invite_link="https://t.me/addlist/abcde"
                )
        """
        match = re.match(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:addlist/|\+))([\w-]+)$", invite_link)

        if match:
            slug = match.group(1)
        elif isinstance(invite_link, str):
            slug = invite_link
        else:
            raise ValueError("Invalid folder invite link")

        r = await self.invoke(
            raw.functions.chatlists.DeleteExportedInvite(
                chatlist=raw.types.InputChatlistDialogFilter(filter_id=chat_folder_id),
                slug=slug
            )
        )

        return r
