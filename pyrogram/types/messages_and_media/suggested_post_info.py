from datetime import datetime
from typing import Optional

from pyrogram import enums, types, utils

from ..object import Object


class SuggestedPostInfo(Object):
    """Contains information about a suggested post."""

    def __init__(
        self,
        *,
        price: Optional["types.SuggestedPostPrice"] = None,
        send_date: Optional[datetime] = None,
        state: Optional["enums.SuggestedPostState"] = None
    ):
        super().__init__()

        self.price = price
        self.send_date = send_date
        self.state = state

    @staticmethod
    def _parse(suggested_post) -> Optional["SuggestedPostInfo"]:
        if not suggested_post:
            return None

        if getattr(suggested_post, "accepted", None):
            state = enums.SuggestedPostState.APPROVED
        elif getattr(suggested_post, "rejected", None):
            state = enums.SuggestedPostState.DECLINED
        else:
            state = enums.SuggestedPostState.PENDING

        return SuggestedPostInfo(
            price=types.SuggestedPostPrice._parse(getattr(suggested_post, "price", None)),
            send_date=utils.timestamp_to_datetime(getattr(suggested_post, "schedule_date", None)),
            state=state,
        )
