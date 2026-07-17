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

from enum import auto

from .auto_name import AutoName


class MessageOriginType(AutoName):
    """Message origin type enumeration used in :obj:`~pyrogram.types.MessageOrigin`."""

    CHANNEL = auto()
    "The message was originally a post in a channel"

    CHAT = auto()
    "The message was originally sent on behalf of a chat"

    HIDDEN_USER = auto()
    "The message was originally sent by a user, which is hidden by their privacy settings"

    IMPORT_INFO = auto()
    "The message was imported with `importMessages <https://t.me/telegram/142>`_"

    # Alias for pyroblack <= 2.7.2
    IMPORT = IMPORT_INFO
    "Deprecated alias of IMPORT_INFO"

    USER = auto()
    "The message was originally sent by a known user"
