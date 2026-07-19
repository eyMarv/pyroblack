#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2024 Dan <https://github.com/delivrance>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  This file is part of Pyroblack.
#
#  Pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  Pyroblack is a continuation fork of Pyrogram <https://github.com/pyrogram/pyrogram>
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.messages_and_media.message import Str
from pyrogram.types.object import Object


class TextQuote(Object):
    """This object contains information about the quoted part of a message that is replied to by the given message.

    Parameters
    ----------
        text (``str``):
            Text of the quoted part of a message that is replied to by the given message

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities that appear in the quote. Currently, only bold, italic, underline, strikethrough, spoiler, and custom_emoji entities are kept in quotes.

        position (``int``):
            Approximate quote position in the original message in UTF-16 code units as specified by the sender

        is_manual  (``bool``, *optional*):
            True, if the quote was chosen manually by the message sender. Otherwise, the quote was added automatically by the server.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        text: Str = None,
        entities: list[types.MessageEntity] | None = None,
        position: int | None = None,
        is_manual: bool | None = None,
    ) -> None:
        super().__init__(client)

        self.text = text
        self.entities = entities
        self.position = position
        self.is_manual = is_manual

    @staticmethod
    def _parse(
        client,
        chats: dict,
        users: dict,
        reply_to: raw.types.MessageReplyHeader,
    ) -> TextQuote:
        if not isinstance(reply_to, raw.types.MessageReplyHeader):
            return None

        if not reply_to.quote and not reply_to.quote_text:
            return None

        quote_text = reply_to.quote_text
        quote_entities = reply_to.quote_entities or []
        position = reply_to.quote_offset or 0

        entities = [
            types.MessageEntity._parse(client, entity, users)
            for entity in quote_entities
        ]
        entities = types.List(
            filter(lambda x: x is not None, entities),
        )

        return TextQuote(
            text=Str(quote_text).init(entities) if quote_text else None,
            entities=entities or None,
            position=position,
            is_manual=bool(reply_to.quote) or None,
        )
