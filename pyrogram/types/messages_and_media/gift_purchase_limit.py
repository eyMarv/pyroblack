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

from ..object import Object


class GiftPurchaseLimit(Object):
    """Describes the maximum number of times that a specific gift can be purchased.

    Parameters:
        total_count (``int``, *optional*):
            The maximum number of times the gifts can be purchased.

        remaining_count (``int``, *optional*):
            Number of remaining times the gift can be purchased.
    """
    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        remaining_count: Optional[int] = None
    ):
        super().__init__()

        self.total_count = total_count
        self.remaining_count = remaining_count

    @staticmethod
    def _parse(total: int, remains: int) -> Optional["GiftPurchaseLimit"]:
        if total is None or total <= 0:
            return None

        return GiftPurchaseLimit(
            total_count=total,
            remaining_count=remains
        )

