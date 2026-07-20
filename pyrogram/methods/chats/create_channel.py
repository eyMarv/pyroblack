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

import pyrogram
from pyrogram import raw, types


class CreateChannel:
    async def create_channel(
        self: "pyrogram.Client",
        title: str,
        description: str = "",
        message_auto_delete_time: int = 0,
    ) -> "types.Chat":
        """Create a new broadcast channel.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            title (``str``):
                The channel title.

            description (``str``, *optional*):
                The channel description.

            message_auto_delete_time (``int``, *optional*):
                Message auto-delete time value, in seconds; must be from 0 up to 365 * 86400 and be divisible by 86400. If 0, then messages aren't deleted automatically.

        Returns
        -------
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                await app.create_channel("Channel Title", "Channel Description")

        """
        r = await self.invoke(
            raw.functions.channels.CreateChannel(
                title=title,
                about=description,
                broadcast=True,
                ttl_period=message_auto_delete_time,
            ),
        )

        return types.Chat._parse_chat(self, r.chats[0])
