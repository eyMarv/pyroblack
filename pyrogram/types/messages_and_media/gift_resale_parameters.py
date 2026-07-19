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

from pyrogram import raw
from pyrogram.types.object import Object


class GiftResaleParameters(Object):
    """Describes parameters of a unique gift available for resale.

    Parameters
    ----------
        star_count (``int``, *optional*):
            Resale price of the gift in Telegram Stars.

        toncoin_cent_count (``int``, *optional*):
            Resale price of the gift in 1/100 of Toncoin.

        toncoin_only (``bool``, *optional*):
            True, if the gift can be bought only using Toncoins.

    """

    def __init__(
        self,
        *,
        star_count: int | None = None,
        toncoin_cent_count: int | None = None,
        toncoin_only: bool | None = None,
    ) -> None:
        super().__init__()

        self.star_count = star_count
        self.toncoin_cent_count = toncoin_cent_count
        self.toncoin_only = toncoin_only

    @staticmethod
    def _parse(
        resell_amount: list[raw.base.StarsAmount], ton_only: bool
    ) -> GiftResaleParameters | None:
        if not resell_amount:
            return None

        star_count = None
        toncoin_cent_count = None

        for currency in resell_amount:
            if isinstance(currency, raw.types.StarsAmount):
                star_count = currency.amount
            elif isinstance(currency, raw.types.StarsTonAmount):
                toncoin_cent_count = currency.amount

        return GiftResaleParameters(
            star_count=star_count,
            toncoin_cent_count=toncoin_cent_count,
            toncoin_only=ton_only,
        )
