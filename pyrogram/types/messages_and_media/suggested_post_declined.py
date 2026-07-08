from typing import Optional

from pyrogram import types, utils
from pyrogram.errors import MessageIdsEmpty

from ..object import Object


class SuggestedPostDeclined(Object):
    """Describes a service message about the rejection of a suggested post."""

    def __init__(
        self,
        *,
        suggested_post_message_id: Optional[int] = None,
        suggested_post_message: Optional["types.Message"] = None,
        comment: Optional[str] = None
    ):
        super().__init__()

        self.suggested_post_message_id = suggested_post_message_id
        self.suggested_post_message = suggested_post_message
        self.comment = comment

    @staticmethod
    async def _parse(client, message) -> "SuggestedPostDeclined":
        action = message.action
        if not getattr(action, "rejected", None):
            return None

        from_id = utils.get_peer_id(message.from_id) if message.from_id else None
        peer_id = utils.get_peer_id(message.peer_id)
        chat_id = peer_id or from_id

        suggested_post_message_id = None
        suggested_post_message = None
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

        return SuggestedPostDeclined(
            suggested_post_message_id=suggested_post_message_id,
            suggested_post_message=suggested_post_message,
            comment=getattr(action, "reject_comment", None) or None,
        )
