from typing import List, Optional, Union

from pyrogram import enums, types

from ..object import Object


class ReplyParameters(Object):
    """Describes reply parameters for the message that is being sent."""

    def __init__(
        self,
        *,
        message_id: Optional[int] = None,
        story_id: Optional[int] = None,
        chat_id: Optional[Union[int, str]] = None,
        quote: Optional[str] = None,
        quote_parse_mode: Optional["enums.ParseMode"] = None,
        quote_entities: Optional[List["types.MessageEntity"]] = None,
        quote_position: Optional[int] = None,
        checklist_task_id: Optional[int] = None,
        poll_option_id: Optional[str] = None,
    ):
        super().__init__()

        self.message_id = message_id
        self.story_id = story_id
        self.chat_id = chat_id
        self.quote = quote
        self.quote_parse_mode = quote_parse_mode
        self.quote_entities = quote_entities
        self.quote_position = quote_position
        self.checklist_task_id = checklist_task_id
        self.poll_option_id = poll_option_id
