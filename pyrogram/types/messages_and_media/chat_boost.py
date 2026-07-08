from datetime import datetime
from typing import Optional

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class ChatBoost(Object):
    """Contains information about one or more boosts applied by a specific user."""

    def __init__(
        self,
        *,
        id: str,
        date: datetime,
        expire_date: datetime,
        multiplier: int,
        from_user: Optional["types.User"] = None,
        is_gift: Optional[bool] = None,
        is_giveaway: Optional[bool] = None,
        is_unclaimed: Optional[bool] = None,
        giveaway_message_id: Optional[int] = None,
        used_gift_slug: Optional[str] = None,
        stars: Optional[int] = None
    ):
        super().__init__()

        self.id = id
        self.date = date
        self.expire_date = expire_date
        self.multiplier = multiplier
        self.from_user = from_user
        self.is_gift = is_gift
        self.is_giveaway = is_giveaway
        self.is_unclaimed = is_unclaimed
        self.giveaway_message_id = giveaway_message_id
        self.used_gift_slug = used_gift_slug
        self.stars = stars

    @staticmethod
    def _parse(client: "pyrogram.Client", boost: "raw.types.Boost", users) -> "ChatBoost":
        return ChatBoost(
            id=boost.id,
            date=utils.timestamp_to_datetime(boost.date),
            expire_date=utils.timestamp_to_datetime(boost.expires),
            multiplier=getattr(boost, "multiplier", 1),
            from_user=types.User._parse(client, users.get(boost.user_id)),
            is_gift=getattr(boost, "gift", None),
            is_giveaway=getattr(boost, "giveaway", None),
            is_unclaimed=getattr(boost, "unclaimed", None),
            giveaway_message_id=getattr(boost, "giveaway_msg_id", None),
            used_gift_slug=getattr(boost, "used_gift_slug", None),
            stars=getattr(boost, "stars", None),
        )
