from datetime import datetime
from typing import List, Optional

from pyrogram import raw, types, utils

from ..object import Object


class AuctionState(Object):
    """Describes state of an auction."""

    def __init__(self):
        super().__init__()


class AuctionStateActive(AuctionState):
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        min_bid: int,
        bid_levels: List["types.AuctionBid"],
        top_bidder_user_ids: List[int],
        auction_rounds: List["types.AuctionRound"],
        current_round_end_date: datetime,
        current_round_number: int,
        total_round_count: int,
        left_item_count: int,
    ):
        super().__init__()

        self.start_date = start_date
        self.end_date = end_date
        self.min_bid = min_bid
        self.bid_levels = bid_levels
        self.top_bidder_user_ids = top_bidder_user_ids
        self.auction_rounds = auction_rounds
        self.current_round_end_date = current_round_end_date
        self.current_round_number = current_round_number
        self.total_round_count = total_round_count
        self.left_item_count = left_item_count

    @staticmethod
    async def _parse(auction_state: "raw.types.StarGiftAuctionState"):
        return AuctionStateActive(
            start_date=utils.timestamp_to_datetime(auction_state.start_date),
            end_date=utils.timestamp_to_datetime(auction_state.end_date),
            min_bid=auction_state.min_bid_amount,
            bid_levels=types.List(types.AuctionBid._parse(bid_level) for bid_level in auction_state.bid_levels),
            top_bidder_user_ids=auction_state.top_bidders,
            auction_rounds=types.List(types.AuctionRound._parse(auction_round) for auction_round in auction_state.rounds),
            current_round_end_date=utils.timestamp_to_datetime(auction_state.next_round_at),
            current_round_number=auction_state.current_round,
            total_round_count=auction_state.total_rounds,
            left_item_count=auction_state.gifts_left,
        )


class AuctionStateFinished(AuctionState):
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        average_price: int,
        telegram_listed_item_count: Optional[int] = None,
        fragment_listed_item_count: Optional[int] = None,
        fragment_url: Optional[str] = None,
    ):
        super().__init__()

        self.start_date = start_date
        self.end_date = end_date
        self.average_price = average_price
        self.telegram_listed_item_count = telegram_listed_item_count
        self.fragment_listed_item_count = fragment_listed_item_count
        self.fragment_url = fragment_url

    @staticmethod
    async def _parse(auction_state: "raw.types.StarGiftAuctionStateFinished"):
        return AuctionStateFinished(
            start_date=utils.timestamp_to_datetime(auction_state.start_date),
            end_date=utils.timestamp_to_datetime(auction_state.end_date),
            average_price=auction_state.average_price,
            telegram_listed_item_count=auction_state.listed_count,
            fragment_listed_item_count=auction_state.fragment_listed_count,
            fragment_url=auction_state.fragment_listed_url,
        )
