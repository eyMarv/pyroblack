from typing import Optional

from pyrogram import errors

from ..object import Object


class GiveawayCompleted(Object):
    """Represents a service message about the completion of a giveaway without public winners."""

    def __init__(
        self,
        *,
        winner_count: int,
        unclaimed_prize_count: int = None,
        giveaway_message_id: int = None,
        giveaway_message=None,
        is_star_giveaway: bool = None
    ):
        super().__init__()

        self.winner_count = winner_count
        self.unclaimed_prize_count = unclaimed_prize_count
        self.giveaway_message_id = giveaway_message_id
        self.giveaway_message = giveaway_message
        self.is_star_giveaway = is_star_giveaway

    @staticmethod
    async def _parse(client, giveaway_results, chat=None, message_id: int = None) -> "GiveawayCompleted":
        giveaway_message = None
        if chat and message_id:
            try:
                giveaway_message = await client.get_messages(
                    chat_id=chat.id,
                    message_ids=message_id,
                    replies=0
                )
            except (errors.ChannelPrivate, errors.ChannelInvalid):
                pass

        return GiveawayCompleted(
            winner_count=giveaway_results.winners_count,
            unclaimed_prize_count=giveaway_results.unclaimed_count,
            giveaway_message_id=message_id,
            giveaway_message=giveaway_message,
            is_star_giveaway=getattr(giveaway_results, "stars", None),
        )
