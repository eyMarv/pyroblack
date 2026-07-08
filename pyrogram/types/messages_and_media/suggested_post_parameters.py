from datetime import datetime
from typing import Optional

from pyrogram import raw, types, utils

from ..object import Object


class SuggestedPostParameters(Object):
    """Contains parameters of a post that is being suggested."""

    def __init__(
        self,
        *,
        price: Optional["types.SuggestedPostPrice"] = None,
        send_date: Optional[datetime] = None
    ):
        super().__init__()

        self.price = price
        self.send_date = send_date

    def write(self) -> "raw.types.SuggestedPost":
        return raw.types.SuggestedPost(
            price=self.price.write() if self.price else None,
            schedule_date=utils.datetime_to_timestamp(self.send_date)
        )
