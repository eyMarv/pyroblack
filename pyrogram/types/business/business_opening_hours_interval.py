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

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class BusinessOpeningHoursInterval(Object):
    """Parameters
    opening_minute (``int``):
        The minute's sequence number in a week, starting on Monday, marking the start of the time interval during which the business is open; 0 - 7 * 24 * 60.

    closing_minute (``int``):
        The minute's sequence number in a week, starting on Monday, marking the end of the time interval during which the business is open; 0 - 8 * 24 * 60

    """

    def __init__(
        self,
        *,
        opening_minute: int | None = None,
        closing_minute: int | None = None,
    ) -> None:
        super().__init__()

        self.opening_minute = opening_minute
        self.closing_minute = closing_minute

    @staticmethod
    def _parse(
        weekly_open_: raw.types.BusinessWeeklyOpen,
    ) -> BusinessOpeningHoursInterval:
        return BusinessOpeningHoursInterval(
            opening_minute=weekly_open_.start_minute,
            closing_minute=weekly_open_.end_minute,
        )
