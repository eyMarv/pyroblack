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

from pyrogram import types
from ..object import Object


class KeyboardButtonRequestManagedBot(Object):
    """This object defines the parameters for the creation of a managed bot.
    Information about the created bot will be shared with the bot using the update managed_bot and a Message with the field ``managed_bot_created``.

    Parameters:
        request_id (``int``):
            Signed 32-bit identifier of the request. Must be unique within the message

        suggested_name (``str``, *optional*):
            Suggested name for the bot.

        suggested_username (``str``, *optional*):
            Suggested username for the bot.

    """
    def __init__(
        self,
        request_id: int,
        suggested_name: str = None,
        suggested_username: str = None,
    ):
        self.request_id = request_id
        self.suggested_name = suggested_name
        self.suggested_username = suggested_username
