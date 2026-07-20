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

from pyrogram.types.object import Object


class ShippingAddress(Object):
    """Contains information about a shipping address.

    Parameters
    ----------
        street_line1 (``str``):
            First line for the address.

        street_line1 (``str``):
            Second line for the address.

        city (``str``):
            City for the address.

        state (``str``):
            State for the address, if applicable.

        post_code (``str``):
            Post code for the address.

        country_code (``str``):
            Two-letter ISO 3166-1 alpha-2 country code.

    """

    def __init__(
        self,
        *,
        street_line1: str,
        street_line2: str,
        city: str,
        state: str,
        post_code: str,
        country_code: str,
    ) -> None:
        super().__init__()

        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.city = city
        self.state = state
        self.post_code = post_code
        self.country_code = country_code
