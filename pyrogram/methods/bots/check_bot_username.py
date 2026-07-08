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

import pyrogram
from pyrogram import raw


class CheckBotUsername:
    async def check_bot_username(
        self: "pyrogram.Client",
        username: str,
    ) -> bool:
        """Checks whether a username can be set for a new bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            username (``str``):
                Username to be checked.

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self.invoke(raw.functions.bots.CheckUsername(username=username))
