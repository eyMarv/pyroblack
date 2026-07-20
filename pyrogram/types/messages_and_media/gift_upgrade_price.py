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

from datetime import datetime

from pyrogram import raw, utils
from pyrogram.types.object import Object


class GiftUpgradePrice(Object):
    """Describes a price required to pay to upgrade a gift.

    Parameters
    ----------
        date (:py:obj:`~datetime.datetime`):
            Date when the price will be in effect.

        star_count (``int``):
            The amount of Telegram Stars required to pay to upgrade the gift.

    """

    def __init__(
        self,
        *,
        date: datetime,
        star_count: int,
    ) -> None:
        super().__init__()

        self.date = date
        self.star_count = star_count

    @staticmethod
    def _parse(attr: "raw.base.StarGiftUpgradePrice") -> "GiftUpgradePrice":
        return GiftUpgradePrice(
            date=utils.timestamp_to_datetime(attr.date),
            star_count=attr.upgrade_stars,
        )
