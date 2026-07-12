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

from typing import Optional

from pyrogram import raw, types
from ..object import Object


class BotAllowed(Object):
    """Contains information about a allowed bot.

    Parameters:
        attach_menu (``bool``, *optional*):
            True, if the bot can attach to menu.

        from_request (``bool``, *optional*):
            True, if the bot is allowed from request.

        domain (``str``, *optional*):
            The domain of the bot.

        app (:obj:`~pyrogram.types.BotApp`, *optional*):
            The app of the bot.
    """

    def __init__(
        self,
        *,
        attach_menu: Optional[bool] = None,
        from_request: Optional[bool] = None,
        domain: Optional[str] = None,
        app: Optional["types.BotApp"] = None,
    ):
        super().__init__()

        self.attach_menu = attach_menu
        self.from_request = from_request
        self.domain = domain
        self.app = app

    @staticmethod
    def _parse(
        client: "pyrogram.Client", bot_allowed: "raw.types.BotAllowed"
    ) -> "BotAllowed":
        bot_app = getattr(bot_allowed, "app", None)
        return BotAllowed(
            attach_menu=getattr(bot_allowed, "attach_menu", None),
            from_request=getattr(bot_allowed, "from_request", None),
            domain=getattr(bot_allowed, "domain", None),
            app=types.BotApp._parse(client, bot_app) if bot_app is not None else None,
        )
