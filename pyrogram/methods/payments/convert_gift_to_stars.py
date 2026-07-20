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
from pyrogram import raw, utils


class ConvertGiftToStars:
    async def convert_gift_to_stars(
        self: pyrogram.Client,
        owned_gift_id: str,
        business_connection_id: str | None = None,
    ) -> bool:
        """Convert a given regular gift to Telegram Stars.

        .. note::

            Requires the `can_convert_gifts_to_stars` business bot right.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            owned_gift_id (``str``):
                Unique identifier of the regular gift that should be converted to Telegram Stars.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.
                For bots only.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Convert gift
                await app.convert_gift_to_stars(message_id=123)

        """
        return await self.invoke(
            raw.functions.payments.ConvertStarGift(
                stargift=await utils.get_input_stargift(self, owned_gift_id),
            ),
            business_connection_id=business_connection_id,
        )
