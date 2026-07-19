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


class SetPersonalChat:
    async def set_personal_chat(
        self: pyrogram.Client,
        chat_id: int | str | None = None,
    ) -> bool:
        """Changes the personal chat of the current user.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``, *optional*):
                Identifier of the new personal chat; pass None to remove the chat. Use :meth:`~pyrogram.Client.get_created_chats` with ``is_suitable_for_my_personal_chat`` to get suitable chats

        Returns
        -------
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your personal chat
                await app.set_personal_chat(chat_id="@Pyrogram")

                # Hide your personal chat
                await app.set_personal_chat()

        """
        return bool(
            await self.invoke(
                raw.functions.account.UpdatePersonalChannel(
                    channel=await self.resolve_peer(
                        chat_id,
                    )
                    if chat_id
                    else raw.types.InputChannelEmpty(),
                ),
            ),
        )
