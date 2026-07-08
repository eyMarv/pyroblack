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

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types


class CreateBot:
    async def create_bot(
        self: "pyrogram.Client",
        manager_bot_user_id: Union[int, str],
        name: str,
        username: str,
        via_link: Optional[bool] = None,
    ) -> "types.User":
        """Creates a bot which will be managed by another bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            manager_bot_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the bot that will manage the created bot.

            name (``str``):
                Name of the bot, 1-64 characters.

            username (``str``):
                Username of the bot. The username must end with "bot".

            via_link (``bool``, *optional*):
                Pass True if the bot is created from link.

        Returns:
            :obj:`~pyrogram.types.User`: On success, the created bot user is returned.
        """
        r = await self.invoke(
            raw.functions.bots.CreateBot(
                name=name,
                username=username,
                manager_id=await self.resolve_peer(manager_bot_user_id),
                via_deeplink=via_link,
            )
        )

        return types.User._parse(self, r)
