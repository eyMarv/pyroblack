from typing import Dict

from pyrogram import raw, types

from ..object import Object


class ChatOwnerChanged(Object):
    """Describes a service message about an ownership change in the chat."""

    def __init__(self, *, new_owner: "types.User"):
        super().__init__()

        self.new_owner = new_owner

    @staticmethod
    def _parse(client, action: "raw.types.MessageActionChangeCreator", users: Dict[int, "types.User"]) -> "ChatOwnerChanged":
        if isinstance(action, raw.types.MessageActionChangeCreator):
            return ChatOwnerChanged(
                new_owner=types.User._parse(client, users.get(action.new_creator_id))
            )

        return None
