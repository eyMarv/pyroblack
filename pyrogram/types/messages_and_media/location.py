#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union
import pyrogram

from pyrogram import raw
from ..object import Object


class Location(Object):
    """A point on the map.

    Parameters:
        longitude (``float``):
            Longitude as defined by sender.

        latitude (``float``):
            Latitude as defined by sender.

        accuracy_radius (``int``, *optional*):
            The estimated horizontal accuracy of the location, in meters as defined by the sender.

        address (``str``, *optional*):
            Textual description of the address (mandatory).
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        longitude: float,
        latitude: float,
        accuracy_radius: int = None,
        address: str = None
    ):
        super().__init__(client)

        self.longitude = longitude
        self.latitude = latitude
        self.accuracy_radius = accuracy_radius
        self.address = address

    @staticmethod
    def _parse(client, geo_point: Union["raw.types.GeoPoint", "raw.types.BusinessLocation"]) -> "Location":
        if isinstance(geo_point, raw.types.GeoPoint):
            return Location(
                longitude=geo_point.long,
                latitude=geo_point.lat,
                accuracy_radius=getattr(geo_point, "accuracy_radius", None),
                client=client
            )

        if isinstance(geo_point, raw.types.BusinessLocation):
            return Location(
                longitude=getattr(geo_point.geo_point, "long", None),
                latitude=getattr(geo_point.geo_point, "lat", None),
                accuracy_radius=getattr(geo_point.geo_point, "accuracy_radius", None),
                address=geo_point.address,
                client=client
            )
