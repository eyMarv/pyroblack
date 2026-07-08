import re
from typing import Union

import pyrogram
from pyrogram import raw, types


class GetGiftAuctionState:
    async def get_gift_auction_state(
        self: "pyrogram.Client",
        auction_id: Union[str, int]
    ) -> "types.GiftAuctionState":
        """Returns auction state for a gift."""

        if isinstance(auction_id, int):
            auction = raw.types.InputStarGiftAuction(gift_id=auction_id)
        else:
            match = re.match(
                r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:auction/))([\w-]+)$",
                auction_id,
            )

            if match:
                slug = match.group(1)
            elif isinstance(auction_id, str):
                slug = auction_id
            else:
                raise ValueError("Invalid auction link")

            auction = raw.types.InputStarGiftAuctionSlug(slug=slug)

        result = await self.invoke(
            raw.functions.payments.GetStarGiftAuctionState(
                auction=auction,
                version=0,
            )
        )

        return await types.GiftAuctionState._parse(self, result)
