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

from pyrogram import raw, types
from ..object import Object
from ..update import Update


class ManagedBotUpdated(Object, Update):
    """This object contains information about the creation or token update of a bot that is managed by the current bot.

    Parameters:
        user (:obj:`~pyrogram.types.User`, *optional*):
            User that created the bot.
        
        bot (:obj:`~pyrogram.types.User`, *optional*):
            Information about the bot. The bot's token can be fetched using the method :obj:`~pyrogram.raw.functions.bots.CreateBot`.

    """

    def __init__(
        self,
        *,
        user: "types.User",
        bot: "types.User",
    ):
        super().__init__()

        self.user = user
        self.bot = bot

    @staticmethod
    def _parse(
        client,
        update: "raw.types.UpdateManagedBot",
        users: dict,
    ) -> "ManagedBotUpdated":
        return ManagedBotUpdated(
            user=types.User._parse(client, users[update.user_id]),
            bot=types.User._parse(client, users[update.bot_id]),
        )
