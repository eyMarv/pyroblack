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

import asyncio
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, utils

from .input_privacy_rule import InputPrivacyRule

if TYPE_CHECKING:
    from collections.abc import Iterable


class InputPrivacyRuleAllowChats(InputPrivacyRule):
    """Allow only participants of certain chats.

    Parameters
    ----------
        chat_ids (``int`` | ``str`` | Iterable of ``int`` or ``str``):
            Unique identifier (int) or username (str) of the target chat.

    """

    def __init__(
        self,
        chat_ids: int | str | Iterable[int | str],
    ) -> None:
        super().__init__()

        self.chat_ids = chat_ids

    async def write(self, client: pyrogram.Client):
        chats = (
            list(self.chat_ids)
            if not isinstance(self.chat_ids, (int, str))
            else [self.chat_ids]
        )
        chats = await asyncio.gather(*[client.resolve_peer(i) for i in chats])

        return raw.types.InputPrivacyValueAllowChatParticipants(
            chats=[utils.get_peer_id(i) for i in chats],
        )
