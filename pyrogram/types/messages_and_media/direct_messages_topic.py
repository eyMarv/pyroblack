from typing import Dict, Optional

from pyrogram import types

from ..object import Object


class DirectMessagesTopic(Object):
    """Contains information about a topic in a channel direct messages chat."""

    def __init__(
        self,
        *,
        id: int,
        user: Optional["types.User"] = None,
        can_send_unpaid_messages: Optional[bool] = None,
        is_marked_as_unread: Optional[bool] = None,
        unread_count: Optional[int] = None,
        last_read_inbox_message_id: Optional[int] = None,
        last_read_outbox_message_id: Optional[int] = None,
        unread_reactions_count: Optional[int] = None,
        last_message: Optional["types.Message"] = None
    ):
        super().__init__()

        self.id = id
        self.user = user
        self.can_send_unpaid_messages = can_send_unpaid_messages
        self.is_marked_as_unread = is_marked_as_unread
        self.unread_count = unread_count
        self.last_read_inbox_message_id = last_read_inbox_message_id
        self.last_read_outbox_message_id = last_read_outbox_message_id
        self.unread_reactions_count = unread_reactions_count
        self.last_message = last_message

    @staticmethod
    def _parse(
        client,
        topic,
        messages: dict = None,
        users: Dict[int, "types.User"] = None,
        chats: Dict[int, "types.Chat"] = None
    ) -> "DirectMessagesTopic":
        if not topic:
            return None

        messages = messages or {}
        users = users or {}
        chats = chats or {}

        return DirectMessagesTopic(
            id=topic.peer.user_id,
            user=types.User._parse(client, users.get(topic.peer.user_id)),
            can_send_unpaid_messages=topic.nopaid_messages_exception,
            is_marked_as_unread=topic.unread_mark,
            unread_count=topic.unread_count,
            last_read_inbox_message_id=topic.read_inbox_max_id,
            last_read_outbox_message_id=topic.read_outbox_max_id,
            unread_reactions_count=topic.unread_reactions_count,
            last_message=messages.get(topic.top_message),
        )
