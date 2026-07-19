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


class SetChatMenuButton:
    async def set_chat_menu_button(
        self: pyrogram.Client,
        chat_id: int | str | None = None,
        menu_button: types.MenuButton = None,
    ) -> bool:
        """Change the bot's menu button in a private chat, or the default menu button.

        .. include:: /_includes/usable-by/bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                If not specified, default bot's menu button will be changed.

            menu_button (:obj:`~pyrogram.types.MenuButton`, *optional*):
                The new bot's menu button.
                Defaults to :obj:`~pyrogram.types.MenuButtonDefault`.

        Raises
        ------
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        """
        await self.invoke(
            raw.functions.bots.SetBotMenuButton(
                user_id=await self.resolve_peer(chat_id or "me"),
                button=(
                    (await menu_button.write(self))
                    if menu_button
                    else (await types.MenuButtonDefault().write(self))
                ),
            ),
        )

        return True
