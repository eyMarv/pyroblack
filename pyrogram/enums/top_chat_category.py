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


class TopChatCategory(AutoName):
    """Represents the categories of chats for which a list of frequently used chats can be retrieved.
    Used in :meth:`~pyrogram.Client.get_top_chats`.
    """

    USERS = auto()
    "A category containing frequently used private chats with non-bot users"

    BOTS = auto()
    "A category containing frequently used private chats with bot users"

    GROUPS = auto()
    "A category containing frequently used basic groups and supergroups"

    CHANNELS = auto()
    "A category containing frequently used channels"

    INLINE_BOTS = auto()
    "A category containing frequently used chats with inline bots sorted by their usage in inline mode"

    GUEST_BOTS = auto()
    "A category containing frequently used chats with bots, which were used as guest bots"

    WEB_APP_BOTS = auto()
    "A category containing frequently used chats with bots, which Web Apps were opened"

    CALLS = auto()
    "A category containing frequently used chats used for calls"

    FORWARD_CHATS = auto()
    "A category containing frequently used chats used to forward messages"
