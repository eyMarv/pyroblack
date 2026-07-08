from pyrogram import raw, types
from ..object import Object


class BusinessLocation(Object):
    def __init__(self, *, address: str = None, location: "types.Location" = None):
        super().__init__()
        self.address = address
        self.location = location

    @staticmethod
    def _parse(client, business_location: "raw.types.BusinessLocation") -> "BusinessLocation":
        return BusinessLocation(
            address=getattr(business_location, "address", None),
            location=types.Location._parse(client, business_location.geo_point) if getattr(business_location, "geo_point", None) else None,
        )
