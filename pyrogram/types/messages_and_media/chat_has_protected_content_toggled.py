from pyrogram import raw

from ..object import Object


class ChatHasProtectedContentToggled(Object):
    """Chat `has_protected_content` setting was changed or request to change it was rejected."""

    def __init__(
        self,
        *,
        request_message_id: int,
        old_has_protected_content: bool,
        new_has_protected_content: bool,
    ):
        super().__init__()

        self.request_message_id = request_message_id
        self.old_has_protected_content = old_has_protected_content
        self.new_has_protected_content = new_has_protected_content

    @staticmethod
    def _parse(message_id: int, action: "raw.types.MessageActionNoForwardsToggle") -> "ChatHasProtectedContentToggled":
        return ChatHasProtectedContentToggled(
            request_message_id=message_id,
            old_has_protected_content=action.prev_value,
            new_has_protected_content=action.new_value,
        )
