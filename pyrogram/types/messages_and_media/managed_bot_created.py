from typing import Dict

import pyrogram
from pyrogram import raw, types

from ..object import Object


class ManagedBotCreated(Object):
    """Contains information about the bot that was created to be managed by the current bot."""

    def __init__(
        self,
        *,
        bot: "types.User",
    ):
        super().__init__()

        self.bot = bot

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        managed_bot_created: "raw.types.MessageActionManagedBotCreated",
        users: Dict[int, "raw.types.User"],
    ) -> "ManagedBotCreated":
        if not isinstance(managed_bot_created, raw.types.MessageActionManagedBotCreated):
            return None

        return ManagedBotCreated(
            bot=types.User._parse(client, users.get(managed_bot_created.bot_id))
        )
