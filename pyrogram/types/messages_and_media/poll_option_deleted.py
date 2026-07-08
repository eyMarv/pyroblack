from typing import Optional

from pyrogram import raw, types

from ..object import Object


class PollOptionDeleted(Object):
    """Describes a service message about an option deleted from a poll."""

    def __init__(
        self,
        *,
        poll_message: Optional["types.Message"] = None,
        option_persistent_id: str,
        text: "types.FormattedText"
    ):
        super().__init__()

        self.poll_message = poll_message
        self.option_persistent_id = option_persistent_id
        self.text = text

    @staticmethod
    async def _parse(client, reply_message: Optional["types.Message"], poll_option_deleted: "raw.types.MessageActionPollDeleteAnswer") -> "PollOptionDeleted":
        if not isinstance(poll_option_deleted, raw.types.MessageActionPollDeleteAnswer):
            return None

        answer = poll_option_deleted.answer
        return PollOptionDeleted(
            poll_message=reply_message,
            option_persistent_id=answer.option.decode(),
            text=types.FormattedText._parse(client, answer.text)
        )
