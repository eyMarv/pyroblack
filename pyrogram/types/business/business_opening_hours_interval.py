from datetime import datetime

from ..object import Object


class BusinessOpeningHoursInterval(Object):
    def __init__(self, *, start: int = None, end: int = None):
        super().__init__()
        self.start = start
        self.end = end

    @staticmethod
    def _parse(weekly_open) -> "BusinessOpeningHoursInterval":
        return BusinessOpeningHoursInterval(
            start=getattr(weekly_open, "start_minute", None),
            end=getattr(weekly_open, "end_minute", None),
        )
