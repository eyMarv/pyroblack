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
from pyrogram import raw, types


class GetCommonChats:
    async def get_common_chats(
        self: pyrogram.Client,
        user_id: int | str,
    ) -> list[types.Chat]:
        """Get the common chats you have with a user.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns
        -------
            List of :obj:`~pyrogram.types.Chat`: On success, a list of the common chats is returned.

        Raises
        ------
            ValueError: If the user_id doesn't belong to a user.

        Example:
            .. code-block:: python

                common = await app.get_common_chats(user_id)
                print(common)

        """
        peer = await self.resolve_peer(user_id)

        if isinstance(peer, raw.types.InputPeerUser):
            r = await self.invoke(
                raw.functions.messages.GetCommonChats(
                    user_id=peer,
                    max_id=0,
                    limit=100,
                ),
            )

            return types.List([types.Chat._parse_chat(self, x) for x in r.chats])

        msg = f'The user_id "{user_id}" doesn\'t belong to a user'
        raise ValueError(msg)
