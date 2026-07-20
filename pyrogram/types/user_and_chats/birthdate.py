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


class Birthdate(Object):
    """Parameters
    day (``int``):
        Day of the user's birth; 1-31.

    month (``int``):
        Month of the user's birth; 1-12

    year (``int``, *optional*):
        Year of the user's birth

    """

    def __init__(
        self,
        *,
        day: int,
        month: int,
        year: int | None = None,
    ) -> None:
        super().__init__()

        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def _parse(
        birthday: raw.types.Birthday,
    ) -> Birthdate:
        return Birthdate(
            day=birthday.day,
            month=birthday.month,
            year=getattr(birthday, "year", None),
        )

    def write(self):
        return raw.types.Birthday(
            day=self.day,
            month=self.month,
            year=self.year,
        )
