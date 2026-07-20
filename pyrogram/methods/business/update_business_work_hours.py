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

# ***************************
# GENERATED FILE - DO NOT EDIT
# Source: tl:account.updateBusinessWorkHours
# ***************************

from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class UpdateBusinessWorkHours:
    async def update_business_work_hours(
        self: pyrogram.Client,
        business_work_hours: raw.types.BusinessWorkHours | None = None,
    ) -> types.Message:
        """Update business work hours for your business account.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            business_work_hours (raw.types.BusinessWorkHours): Business work hours (timezone + weekly schedule)

        Returns
        -------
            :obj:`~pyrogram.types.Message`

        Example:
            .. code-block:: python

                await app.update_business_work_hours(...)

        """
        await self.invoke(
            raw.functions.account.updateBusinessWorkHours(
                business_work_hours=business_work_hours,
            ),
        )
