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
from ..object import Object


class Birthday(Object):
    """Birthday information of a user.

    Parameters:
        day (``int``):
            Birthday day.

        month (``int``):
            Birthday month.

        year (``int``, *optional*):
            Birthday year.
    """

    def __init__(self, *, day: int, month: int, year: int = None):
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def _parse(birthday: "raw.types.Birthday" = None) -> "Birthday":
        if not birthday:
            return
        return Birthday(
            day=birthday.day, month=birthday.month, year=getattr(birthday, "year", None)
        )

    async def write(self) -> "raw.types.Birthday":
        return raw.types.Birthday(day=self.day, month=self.month, year=self.year)
