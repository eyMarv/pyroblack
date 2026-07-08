from typing import Optional

import pyrogram
from pyrogram import raw, types

from ..object import Object


class GiftAuctionState(Object):
    """Represents auction state of a gift."""

    def __init__(
        self,
        *,
        gift: "types.Gift",
        state: "types.AuctionState",
        raw: Optional["raw.base.StarGiftAuctionState"] = None,
    ):
        super().__init__()

        self.gift = gift
        self.state = state
        self.raw = raw

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        gift_auction_state: "raw.base.StarGiftAuctionState",
    ) -> "GiftAuctionState":
        state = None

        if isinstance(gift_auction_state.state, raw.types.StarGiftAuctionState):
            state = await types.AuctionStateActive._parse(gift_auction_state.state)
        elif isinstance(gift_auction_state.state, raw.types.StarGiftAuctionStateFinished):
            state = await types.AuctionStateFinished._parse(gift_auction_state.state)

        return GiftAuctionState(
            gift=await types.Gift._parse(client, gift_auction_state.gift),
            state=state,
            raw=gift_auction_state,
        )
