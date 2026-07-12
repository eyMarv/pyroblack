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

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class BusinessLocation(Object):
    """

    Parameters:
        address (``str``):
            Address of the business

        location (:obj:`~pyrogram.types.Location`, *optional*):
            Location of the business

    """

    def __init__(
        self,
        *,
        address: str = None,
        location: "types.Location" = None
    ):
        super().__init__()

        self.address = address
        self.location = location


    @staticmethod
    def _parse(
        client,
        business_location: "raw.types.BusinessLocation"
    ) -> "BusinessLocation":
        return BusinessLocation(
            address=getattr(business_location, "address", None),
            location=types.Location._parse(
                client,
                business_location.geo_point
            ) if getattr(business_location, "geo_point", None) else None
        )
