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
from pyrogram import enums, raw


class UpdateFolder:
    async def update_folder(
        self: pyrogram.Client,
        folder_id: int,
        title: str,
        included_chats: int | str | list[int | str] | None = None,
        excluded_chats: int | str | list[int | str] | None = None,
        pinned_chats: int | str | list[int | str] | None = None,
        contacts: bool | None = None,
        non_contacts: bool | None = None,
        groups: bool | None = None,
        channels: bool | None = None,
        bots: bool | None = None,
        exclude_muted: bool | None = None,
        exclude_read: bool | None = None,
        exclude_archived: bool | None = None,
        color: enums.FolderColor = None,
        emoji: str | None = None,
    ) -> bool:
        """Create or update a user's folder.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            folder_id (``int``):
                Unique folder identifier.

            title (``str``):
                Folder title.

            included_chats (``int`` | ``str`` | List of ``int`` or ``str``, *optional*):
                Users or chats that should added in the folder
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            excluded_chats (``int`` | ``str`` | List of ``int`` or ``str``, *optional*):
                Users or chats that should excluded from the folder
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            pinned_chats (``int`` | ``str`` | List of ``int`` or ``str``, *optional*):
                Users or chats that should pinned in the folder
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            contacts (``bool``, *optional*):
                Pass True if folder should contain contacts.

            non_contacts (``bool``, *optional*):
                Pass True if folder should contain non contacts.

            groups (``bool``, *optional*):
                Pass True if folder should contain groups.

            channels (``bool``, *optional*):
                Pass True if folder should contain channels.

            bots (``bool``, *optional*):
                Pass True if folder should contain bots.

            exclude_muted (``bool``, *optional*):
                Pass True if folder should exclude muted users.

            exclude_read (``bool``, *optional*):
                Pass True if folder should exclude chats with no unread messages.

            exclude_archived (``bool``, *optional*):
                Pass True if folder should exclude archived users.

            emoji (``str``, *optional*):
                Folder emoji.
                Pass None to leave the folder icon as default.

            color (:obj:`~pyrogram.enums.FolderColor`, *optional*):
                Color type.
                Pass :obj:`~pyrogram.enums.FolderColor` to set folder color.

        Returns
        -------
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Create or update folder
                app.update_folder(folder_id, title="New folder", included_chats="me")

        """
        if not isinstance(included_chats, list):
            included_chats = [included_chats] if included_chats else []
        if not isinstance(excluded_chats, list):
            excluded_chats = [excluded_chats] if excluded_chats else []
        if not isinstance(pinned_chats, list):
            pinned_chats = [pinned_chats] if pinned_chats else []

        return await self.invoke(
            raw.functions.messages.UpdateDialogFilter(
                id=folder_id,
                filter=raw.types.DialogFilter(
                    id=folder_id,
                    title=title,
                    pinned_peers=[
                        await self.resolve_peer(user_id) for user_id in pinned_chats
                    ],
                    include_peers=[
                        await self.resolve_peer(user_id) for user_id in included_chats
                    ],
                    exclude_peers=[
                        await self.resolve_peer(user_id) for user_id in excluded_chats
                    ],
                    contacts=contacts,
                    non_contacts=non_contacts,
                    groups=groups,
                    broadcasts=channels,
                    bots=bots,
                    exclude_muted=exclude_muted,
                    exclude_read=exclude_read,
                    exclude_archived=exclude_archived,
                    emoticon=emoji,
                    color=color.value if color else None,
                ),
            ),
        )
