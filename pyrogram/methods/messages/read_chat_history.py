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


class ReadChatHistory:
    async def read_chat_history(
        self: pyrogram.Client,
        chat_id: int | str,
        max_id: int = 0,
    ) -> bool:
        """Mark a chat's message history as read.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            max_id (``int``, *optional*):
                The id of the last message you want to mark as read; all the messages before this one will be marked as
                read as well. Defaults to 0 (mark every unread message as read).

        Returns
        -------
            ``bool`` - On success, True is returned.

        Example:
            .. code-block:: python

                # Mark the whole chat as read
                await app.read_chat_history(chat_id)

                # Mark messages as read only up to the given message id
                await app.read_chat_history(chat_id, 12345)

        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            q = raw.functions.channels.ReadHistory(
                channel=peer,
                max_id=max_id,
            )
        else:
            q = raw.functions.messages.ReadHistory(
                peer=peer,
                max_id=max_id,
            )

        await self.invoke(q)

        return True
