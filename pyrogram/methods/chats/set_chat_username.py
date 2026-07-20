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


class SetChatUsername:
    async def set_chat_username(
        self: pyrogram.Client,
        chat_id: int | str,
        username: str | None,
    ) -> bool:
        """Set a channel or a supergroup username.

        To set your own username (for users only, not bots) you can use :meth:`~pyrogram.Client.set_username`.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``)
                Unique identifier (int) or username (str) of the target chat.

            username (``str`` | ``None``):
                Username to set. Pass "" (empty string) or None to remove the username.

        Returns
        -------
            ``bool``: True on success.

        Raises
        ------
            ValueError: In case a chat id belongs to a user or chat.

        Example:
            .. code-block:: python

                await app.set_chat_username(chat_id, "new_username")

        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return bool(
                await self.invoke(
                    raw.functions.channels.UpdateUsername(
                        channel=peer,
                        username=username or "",
                    ),
                ),
            )
        msg = f'The chat_id "{chat_id}" belongs to a user or chat'
        raise ValueError(msg)
