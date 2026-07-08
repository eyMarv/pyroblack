from pyrogram import raw, types
from ..object import Object


class BusinessOpeningHours(Object):
    def __init__(self, *, time_zone_name: str = None, opening_hours: list["types.BusinessOpeningHoursInterval"] = None, _raw: "raw.types.BusinessWorkHours" = None):
        super().__init__()
        self.time_zone_name = time_zone_name
        self.opening_hours = opening_hours
        self._raw = _raw

    @staticmethod
    def _parse(client, business_work_hours: "raw.types.BusinessWorkHours") -> "BusinessOpeningHours":
        return BusinessOpeningHours(
            time_zone_name=getattr(business_work_hours, "timezone_id", None),
            opening_hours=types.List([types.BusinessOpeningHoursInterval._parse(weekly_open_) for weekly_open_ in business_work_hours.weekly_open]) if getattr(business_work_hours, "weekly_open", None) else None,
            _raw=business_work_hours,
        )
