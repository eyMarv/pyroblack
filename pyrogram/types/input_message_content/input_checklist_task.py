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


import pyrogram
from pyrogram import enums, raw, types, utils
from ..object import Object


class InputChecklistTask(Object):
    """Describes a task to add to a checklist.

    Parameters:
        id  (``int``):
            Unique identifier of the task; must be positive and unique among all task identifiers currently present in the checklist.

        text  (``str``):
            Text of the task; 1-100 characters after entities parsing.
        
        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        text_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            List of special entities that appear in the poll option text, which can be specified instead of *text_parse_mode*.
            Currently, only bold, italic, underline, strikethrough, spoiler, and custom_emoji entities are allowed.

    """

    def __init__(
        self,
        id: int = None,
        text: str = None,
        parse_mode: "enums.ParseMode" = None,
        text_entities: list["types.MessageEntity"] = None,
    ):
        super().__init__()

        self.id = id
        self.text = text
        self.parse_mode = parse_mode
        self.text_entities = text_entities

    async def write(self, client: "pyrogram.Client") -> "raw.types.TodoItem":
        text, entities = (await utils.parse_text_entities(
            client, self.text, self.parse_mode, self.text_entities
        )).values()

        return raw.types.TodoItem(
            id=self.id,
            title=raw.types.TextWithEntities(
                text=text,
                entities=entities or []
            )
        )
