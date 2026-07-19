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

from pyrogram import raw
from pyrogram.types.object import Object


class GiftResalePrice(Object):
    """Describes price of a resold gift.

    It can be one of:

    - :obj:`~pyrogram.types.GiftResalePriceStar`
    - :obj:`~pyrogram.types.GiftResalePriceTon`
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def write(self) -> "raw.base.StarsAmount":
        raise NotImplementedError


class GiftResalePriceStar(GiftResalePrice):
    """Describes price of a resold gift in Telegram Stars.

    Parameters
    ----------
        star_count (``int``):
            The amount of Telegram Stars expected to be paid for the gift.

    """

    def __init__(
        self,
        *,
        star_count: int,
    ) -> None:
        super().__init__()

        self.star_count = star_count

    def write(self) -> "raw.types.StarsAmount":
        return raw.types.StarsAmount(
            amount=self.star_count,
            nanos=0,
        )


class GiftResalePriceTon(GiftResalePrice):
    """Describes price of a resold gift in Toncoins.

    Parameters
    ----------
        toncoin_cent_count (``int``):
            The amount of 1/100 of Toncoin expected to be paid for the gift.

    """

    def __init__(
        self,
        *,
        toncoin_cent_count: int,
    ) -> None:
        super().__init__()

        self.toncoin_cent_count = toncoin_cent_count

    def write(self) -> "raw.types.StarsTonAmount":
        return raw.types.StarsTonAmount(
            amount=self.toncoin_cent_count,
        )
