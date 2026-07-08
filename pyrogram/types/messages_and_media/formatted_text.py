from typing import List, Optional

from pyrogram import enums, raw, types, utils
from pyrogram.types.messages_and_media.message import Str

from ..object import Object


class FormattedText(Object):
    """Contains information about a text with some entities."""

    def __init__(
        self,
        *,
        text: Str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
    ):
        super().__init__()

        self.text = text
        self.parse_mode = parse_mode
        self.entities = entities

    def __str__(self) -> str:
        return self.text

    @staticmethod
    def _parse(client, text: "raw.types.TextWithEntities") -> "FormattedText":
        if not isinstance(text, raw.types.TextWithEntities):
            return None

        entities = types.List(
            filter(
                lambda item: item is not None,
                [types.MessageEntity._parse(client, entity, {}) for entity in text.entities],
            )
        )

        return FormattedText(
            text=Str(text.text).init(entities),
            entities=entities or None,
        )

    async def write(self, client) -> "raw.types.TextWithEntities":
        message, entities = (
            await utils.parse_text_entities(
                client,
                self.text,
                self.parse_mode or client.parse_mode,
                self.entities,
            )
        ).values()

        return raw.types.TextWithEntities(text=message, entities=entities or [])
