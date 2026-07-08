from pyrogram import raw, utils

from ..object import Object


class StoryStealthMode(Object):
    def __init__(self, *, active_until_date: int = None, cooldown_until_date: int = None):
        super().__init__()
        self.active_until_date = active_until_date
        self.cooldown_until_date = cooldown_until_date

    @staticmethod
    def _parse(ssm: "raw.types.StoriesStealthMode") -> "StoryStealthMode":
        return StoryStealthMode(
            active_until_date=utils.timestamp_to_datetime(getattr(ssm, "active_until_date", 0)),
            cooldown_until_date=utils.timestamp_to_datetime(getattr(ssm, "cooldown_until_date", 0)),
        )
