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
from pyrogram import raw


class ArchiveChats:
    async def archive_chats(
        self: pyrogram.Client,
        chat_ids: int | str | list[int | str],
    ) -> bool:
        """Archive one or more chats.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_ids (``int`` | ``str`` | List[``int``, ``str``]):
                Unique identifier (int) or username (str) of the target chat.
                You can also pass a list of ids (int) or usernames (str).

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Archive chat
                await app.archive_chats(chat_id)

                # Archive multiple chats at once
                await app.archive_chats([chat_id1, chat_id2, chat_id3])

        """
        if not isinstance(chat_ids, list):
            chat_ids = [chat_ids]

        folder_peers = []

        for chat in chat_ids:
            folder_peers.append(
                raw.types.InputFolderPeer(
                    peer=await self.resolve_peer(chat),
                    folder_id=1,
                ),
            )

        await self.invoke(
            raw.functions.folders.EditPeerFolders(
                folder_peers=folder_peers,
            ),
        )

        return True
