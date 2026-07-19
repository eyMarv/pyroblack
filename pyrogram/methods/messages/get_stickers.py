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

import logging

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class GetStickers:
    async def get_stickers(
        self: "pyrogram.Client",
        short_name: str,
    ) -> list["types.Sticker"]:
        """Get all stickers from set by short name.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            short_name (``str``):
                Short name of the sticker set, serves as the unique identifier for the sticker set.

        Returns
        -------
            List of :obj:`~pyrogram.types.Sticker`: A list of stickers is returned.

        Example:
            .. code-block:: python

                # Get all stickers by short name
                await app.get_stickers("short_name")

        Raises
        ------
            ValueError: In case of invalid arguments.

        """
        sticker_set = await self.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=short_name),
                hash=0,
            ),
        )

        return [
            await types.Sticker._parse(self, doc, {type(a): a for a in doc.attributes})
            for doc in sticker_set.documents
        ]
