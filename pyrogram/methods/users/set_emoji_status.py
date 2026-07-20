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

from typing import Optional

import pyrogram
from pyrogram import raw, types


class SetEmojiStatus:
    async def set_emoji_status(
        self: "pyrogram.Client",
        emoji_status: Optional["types.EmojiStatus"] = None,
    ) -> bool:
        """Set the emoji status.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            emoji_status (:obj:`~pyrogram.types.EmojiStatus`, *optional*):
                The emoji status to set. None to remove.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from pyrogram import types

                await app.set_emoji_status(types.EmojiStatus(custom_emoji_id="1234567890987654321"))

        """
        await self.invoke(
            raw.functions.account.UpdateEmojiStatus(
                emoji_status=(
                    emoji_status.write()
                    if emoji_status
                    else raw.types.EmojiStatusEmpty()
                ),
            ),
        )

        return True
