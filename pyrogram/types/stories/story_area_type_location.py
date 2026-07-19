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

import pyrogram
from pyrogram import raw, types

from .story_area_type import StoryAreaType


class StoryAreaTypeLocation(StoryAreaType):
    """This object describes a story area pointing to a location. Currently, a story can have up to 10 location areas.

    Parameters
    ----------
        latitude (``float``):
            Location latitude in degrees.

        longitude (``float``):
            Location longitude in degrees.

        horizontal_accuracy (``float``, *optional*):
            The radius of uncertainty for the location, measured in meters; 0-1500.

        address (:obj:`~pyrogram.types.LocationAddress`, *optional*):
            Address of the location.

    """

    def __init__(
        self,
        latitude: float | None = None,
        longitude: float | None = None,
        horizontal_accuracy: float = 0,
        address: types.LocationAddress | None = None,
    ) -> None:
        super().__init__()

        self.latitude = latitude
        self.longitude = longitude
        self.horizontal_accuracy = horizontal_accuracy
        self.address = address

    async def write(
        self,
        client: pyrogram.Client,
        coordinates: raw.types.MediaAreaCoordinates,
    ):
        return raw.types.MediaAreaGeoPoint(
            coordinates=coordinates,
            geo=raw.types.GeoPoint(
                long=self.longitude,
                lat=self.latitude,
                access_hash=0,
                accuracy_radius=self.horizontal_accuracy,
            ),
            address=raw.types.GeoPointAddress(
                country_iso2=self.address.country_code,
                state=self.address.state,
                city=self.address.city,
                street=self.address.street,
            )
            if self.address
            else None,
        )
