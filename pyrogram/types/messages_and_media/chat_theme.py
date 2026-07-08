from typing import Optional

import pyrogram
from pyrogram import raw, types

from ..object import Object


class ChatTheme(Object):
    """Describes a chat theme."""

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        gift: Optional["types.Gift"] = None,
    ):
        super().__init__()

        self.name = name
        self.gift = gift

    @staticmethod
    async def _parse(client: "pyrogram.Client", theme: "raw.base.ChatTheme") -> "ChatTheme":
        if isinstance(theme, raw.types.ChatTheme):
            return ChatTheme(name=theme.emoticon)

        if isinstance(theme, raw.types.ChatThemeUniqueGift):
            return ChatTheme(gift=await types.Gift._parse(client, theme.gift))

        return None
