from typing import Optional

from ..object import Object


class GiveawayCreated(Object):
    """Represents a service message about the creation of a scheduled giveaway."""

    def __init__(self, *, prize_star_count: Optional[int] = None):
        super().__init__()

        self.prize_star_count = prize_star_count

    @staticmethod
    def _parse(client, giveaway_launch) -> "GiveawayCreated":
        return GiveawayCreated(
            prize_star_count=getattr(giveaway_launch, "stars", None)
        )
