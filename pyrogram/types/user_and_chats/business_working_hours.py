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

from pyrogram import raw, types
from pyrogram.types.object import Object


class BusinessWorkingHours(Object):
    """Business working hours.

    Parameters
    ----------
        timezone (``str``):
            Timezone of the business.

        working_hours (List of :obj:`~pyrogram.types.BusinessWeeklyOpen`):
            Working hours of the business.

        is_open_now (``bool``, *optional*):
            True, if the business is open now.

    """

    def __init__(
        self,
        *,
        timezone: str,
        working_hours: list[types.BusinessWeeklyOpen],
        is_open_now: bool | None = None,
    ) -> None:
        self.timezone = timezone
        self.is_open_now = is_open_now
        self.working_hours = working_hours

    @staticmethod
    def _parse(
        work_hours: raw.types.BusinessWorkHours = None,
    ) -> BusinessWorkingHours | None:
        if not work_hours:
            return None

        return BusinessWorkingHours(
            timezone=work_hours.timezone_id,
            working_hours=types.List(
                types.BusinessWeeklyOpen._parse(i) for i in work_hours.weekly_open
            ),
            is_open_now=getattr(work_hours, "open_now", None),
        )
