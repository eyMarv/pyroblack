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


class GetStickerSet:
    async def get_sticker_set(
        self: "pyrogram.Client",
        set_short_name: str,
    ) -> "types.StickerSet":
        """Get info about a stickerset.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            set_short_name (``str``):
               Stickerset shortname.

        Returns
        -------
            :obj:`~pyrogram.types.StickerSet`: On success, the StickerSet information is returned.

        Example:
            .. code-block:: python

                await app.get_sticker_set("mypack1")

        """
        r = await self.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(
                    short_name=set_short_name,
                ),
                hash=0,
            ),
        )

        return types.StickerSet._parse(r.set)
