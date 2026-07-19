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

from typing import Optional

from pyrogram import raw, types
from pyrogram.types.object import Object


class BotVerification(Object):
    """Information about bot verification.

    Parameters
    ----------
        bot (:obj:`~pyrogram.types.User`):
            Bot that is verified this user.

        custom_emoji_id (``str``):
            Custom emoji icon identifier.

        description (``int``, *optional*):
            Additional description about the verification.

    """

    def __init__(
        self,
        *,
        bot: int,
        custom_emoji_id: str,
        description: str,
    ) -> None:
        self.bot = bot
        self.custom_emoji_id = custom_emoji_id
        self.description = description

    @staticmethod
    def _parse(
        client,
        verification: "raw.types.BotVerification",
        users,
    ) -> Optional["BotVerification"]:
        if not verification:
            return None

        return BotVerification(
            bot=types.User._parse(client, users.get(verification.bot_id)),
            custom_emoji_id=str(verification.icon),
            description=verification.description,
        )
