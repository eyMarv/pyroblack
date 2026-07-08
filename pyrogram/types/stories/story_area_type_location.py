from typing import Optional

import pyrogram
from pyrogram import raw, types

from .story_area_type import StoryAreaType


class StoryAreaTypeLocation(StoryAreaType):
    def __init__(
        self,
        latitude: float = None,
        longitude: float = None,
        horizontal_accuracy: float = 0,
        address: Optional["types.LocationAddress"] = None,
    ):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.horizontal_accuracy = horizontal_accuracy
        self.address = address

    async def write(self, client: "pyrogram.Client", coordinates: "raw.types.MediaAreaCoordinates"):
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
            ) if self.address else None,
        )
