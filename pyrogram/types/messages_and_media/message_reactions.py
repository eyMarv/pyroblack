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


class MessageReactions(Object):
    """Contains information about a message reactions.

    Parameters
    ----------
        reactions (List of :obj:`~pyrogram.types.Reaction`):
            Reactions list.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        reactions: list[types.Reaction] | None = None,
        top_reactors: list | None = None,
    ) -> None:
        super().__init__(client)

        self.reactions = reactions
        # pyroblack <= 2.7.2
        self.top_reactors = top_reactors

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        message_reactions: raw.base.MessageReactions | None = None,
        users: dict | None = None,
        chats: dict | None = None,
    ) -> MessageReactions | None:
        # users/chats accepted for call-site compatibility (send_reaction etc.)
        if not message_reactions:
            return None

        top_reactors = None
        raw_top = getattr(message_reactions, "top_reactors", None) or getattr(
            message_reactions,
            "recent_reactions",
            None,
        )
        if raw_top:
            try:
                top_reactors = types.List(
                    [
                        types.MessageReactor._parse(client, r, users or {}, chats or {})
                        for r in raw_top
                    ]
                )
            except Exception:
                top_reactors = None

        return MessageReactions(
            client=client,
            reactions=[
                types.Reaction._parse_count(client, reaction)
                for reaction in message_reactions.results
            ],
            top_reactors=top_reactors,
        )
