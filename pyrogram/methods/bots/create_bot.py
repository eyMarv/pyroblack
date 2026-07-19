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


class CreateBot:
    async def create_bot(
        self: pyrogram.Client,
        manager_bot_user_id: int | str,
        name: str,
        username: str,
        via_link: bool | None = None,
    ) -> types.User:
        """Creates a bot which will be managed by another bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            manager_bot_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the bot that will manage the created bot.

            name (``str``):
                Name of the bot, 1-64 characters.

            username (``str``):
                Username of the bot.
                The username must end with "bot".
                Use :meth:`~pyrogram.Client.check_bot_username` to find whether the name is suitable.

            via_link (``bool``):
                Pass True if the bot is created from link.

        Returns
        -------
            :obj:`~pyrogram.types.User`: On success, created bot is returned.

        """
        r = await self.invoke(
            raw.functions.bots.CreateBot(
                name=name,
                username=username,
                manager_id=await self.resolve_peer(manager_bot_user_id),
                via_deeplink=via_link,
            ),
        )

        return types.User._parse(self, r)
