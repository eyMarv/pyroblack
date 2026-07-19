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
from pyrogram.types.object import Object


class FactCheck(Object):
    """Represents a fact-check created by an independent fact-checker.

    Parameters
    ----------
        need_check (``bool``, *optional*):
            If set, the country/text fields will not be set, and the fact check must be fetched manually by the client (if it isn't already cached with the key specified in hash) using bundled messages.getFactCheck requests, when the message with the factcheck scrolls into view.

        country (``str``, *optional*):
            A two-letter ISO 3166-1 alpha-2 country code of the country for which the fact-check should be shown.

        text (``str``, *optional*):
            The fact-check.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

    """

    def __init__(
        self,
        *,
        need_check: bool | None = None,
        country: str | None = None,
        text: str | None = None,
        entities: list[types.MessageEntity] | None = None,
    ) -> None:
        super().__init__()

        self.need_check = need_check
        self.country = country
        self.text = text
        self.entities = entities

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        fact_check: raw.types.FactCheck,
        users: dict[int, list[raw.base.User]],
    ) -> FactCheck | None:
        if not fact_check:
            return None

        text_obj = getattr(fact_check, "text", None)
        message = None
        entities = None

        if isinstance(text_obj, raw.types.TextWithEntities):
            entities = (
                types.List(
                    filter(
                        lambda x: x is not None,
                        [
                            types.MessageEntity._parse(client, entity, users)
                            for entity in (text_obj.entities or [])
                        ],
                    ),
                )
                or None
            )
            message = text_obj.text

        return FactCheck(
            need_check=getattr(fact_check, "need_check", None),
            country=getattr(fact_check, "country", None),
            text=message,
            entities=entities,
        )
