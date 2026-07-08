from typing import Optional

from pyrogram import raw

from ..object import Object


class AuctionRound(Object):
    """Describes a round of an auction."""

    def __init__(
        self,
        number: int,
        duration: int,
        extend_time: Optional[int] = None,
        top_winner_count: Optional[int] = None,
    ):
        super().__init__()

        self.number = number
        self.duration = duration
        self.extend_time = extend_time
        self.top_winner_count = top_winner_count

    @staticmethod
    def _parse(auction_round: "raw.base.StarGiftAuctionRound"):
        if isinstance(auction_round, raw.types.StarGiftAuctionRound):
            return AuctionRound(
                number=auction_round.num,
                duration=auction_round.duration,
            )

        if isinstance(auction_round, raw.types.StarGiftAuctionRoundExtendable):
            return AuctionRound(
                number=auction_round.num,
                duration=auction_round.duration,
                extend_time=auction_round.extend_window,
                top_winner_count=auction_round.extend_top,
            )
