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

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class BotInfo(Object):
    """A bot Information.

    Parameters
    ----------
        name (``str``):
            The bot name.

        about (``str``):
            The bot bio.

        description (``str``):
            Description of the bot;

        privacy_policy_url (``str``, *optional*):
            Privacy policy URL of the bot.

    """

    def __init__(
        self,
        name: str,
        about: str,
        description: str,
        privacy_policy_url: str | None = None,
    ) -> None:
        super().__init__()

        self.name = name
        self.about = about
        self.description = description
        self.privacy_policy_url = privacy_policy_url

    @staticmethod
    def _parse(bot_info: raw.types.bots.BotInfo) -> BotInfo:
        return BotInfo(
            name=getattr(bot_info, "name", None),
            about=getattr(bot_info, "about", None),
            description=getattr(bot_info, "description", None),
            privacy_policy_url=getattr(bot_info, "privacy_policy_url", None),
        )
