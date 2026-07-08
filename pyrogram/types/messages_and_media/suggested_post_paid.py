from typing import Optional

from pyrogram import types, utils
from pyrogram.errors import MessageIdsEmpty
from pyrogram import raw

from ..object import Object


class SuggestedPostPaid(Object):
    """Describes a service message about a successful payment for a suggested post."""

    def __init__(
        self,
        *,
        suggested_post_message_id: int = None,
        suggested_post_message: Optional["types.Message"] = None,
        amount: int = None,
        star_amount: "types.StarAmount" = None,
    ):
        super().__init__()

        self.suggested_post_message_id = suggested_post_message_id
        self.suggested_post_message = suggested_post_message
        self.amount = amount
        self.star_amount = star_amount

    @staticmethod
    async def _parse(client, message) -> "SuggestedPostPaid":
        action = message.action

        from_id = utils.get_peer_id(message.from_id) if message.from_id else None
        peer_id = utils.get_peer_id(message.peer_id)
        chat_id = peer_id or from_id

        suggested_post_message_id = None
        suggested_post_message = None
        amount = None
        star_amount = None

        if getattr(message.reply_to, "reply_to_msg_id", None):
            suggested_post_message_id = message.reply_to.reply_to_msg_id
            if getattr(client, "fetch_replies", None):
                try:
                    suggested_post_message = await client.get_messages(
                        chat_id=chat_id,
                        message_ids=suggested_post_message_id
                    )
                except MessageIdsEmpty:
                    pass

        if isinstance(getattr(action, "price", None), raw.types.StarsTonAmount):
            amount = action.price.amount
        elif isinstance(getattr(action, "price", None), raw.types.StarsAmount):
            star_amount = types.StarAmount._parse(action.price)

        return SuggestedPostPaid(
            suggested_post_message_id=suggested_post_message_id,
            suggested_post_message=suggested_post_message,
            amount=amount,
            star_amount=star_amount
        )
