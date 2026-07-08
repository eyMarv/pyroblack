import random
from typing import Dict, Optional

from pyrogram import raw, types, utils
from pyrogram.errors import ChannelPrivate, MessageIdsEmpty

from ..object import Object


class GiveawayPrizeStars(Object):
    """Telegram Stars were received by the current user from a giveaway."""

    def __init__(
        self,
        *,
        star_count: int,
        transaction_id: str,
        boosted_chat: "types.Chat",
        giveaway_message_id: int,
        giveaway_message: Optional["types.Message"] = None,
        is_unclaimed: Optional[bool] = None,
        sticker: Optional["types.Sticker"] = None
    ):
        super().__init__()

        self.star_count = star_count
        self.transaction_id = transaction_id
        self.boosted_chat = boosted_chat
        self.giveaway_message_id = giveaway_message_id
        self.giveaway_message = giveaway_message
        self.is_unclaimed = is_unclaimed
        self.sticker = sticker

    @staticmethod
    async def _parse(client, action, chats: Dict[int, "raw.base.Chat"]) -> "GiveawayPrizeStars":
        raw_stickers = await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetPremiumGifts(),
                hash=0
            )
        )

        parsed_message = None
        try:
            parsed_message = await client.get_messages(
                chat_id=utils.get_peer_id(action.boost_peer),
                message_ids=action.giveaway_msg_id,
                replies=0
            )
        except (MessageIdsEmpty, ChannelPrivate):
            pass

        return GiveawayPrizeStars(
            star_count=action.stars,
            transaction_id=action.transaction_id,
            boosted_chat=types.Chat._parse_chat(client, chats.get(utils.get_raw_peer_id(action.boost_peer))),
            giveaway_message_id=action.giveaway_msg_id,
            giveaway_message=parsed_message,
            sticker=random.choice(
                types.List(
                    [
                        await types.Sticker._parse(
                            client,
                            doc,
                            {type(item): item for item in doc.attributes}
                        ) for doc in raw_stickers.documents
                    ]
                )
            )
        )
