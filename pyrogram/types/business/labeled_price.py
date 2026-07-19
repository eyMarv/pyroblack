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


class LabeledPrice(Object):
    """This object represents a portion of the price for goods or services.

    Parameters
    ----------
        label (``str``):
            Portion label.

        amount (``int``):
            Price of the product in the smallest units of the currency (integer, **not** float/double). For example, for a price of ``US$ 1.45`` pass ``amount = 145``. See the __exp__ parameter in `currencies.json <https://core.telegram.org/bots/payments/currencies.json>`_, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).

    """

    def __init__(
        self,
        label: str,
        amount: int,
    ) -> None:
        super().__init__()

        self.label = label
        self.amount = amount

    @staticmethod
    def _parse(labeled_price: "raw.types.LabeledPrice") -> "LabeledPrice":
        if isinstance(labeled_price, raw.types.LabeledPrice):
            return LabeledPrice(
                label=labeled_price.label,
                amount=labeled_price.amount,
            )
        return None

    def write(self):
        return raw.types.LabeledPrice(
            label=self.label,
            amount=self.amount,
        )
