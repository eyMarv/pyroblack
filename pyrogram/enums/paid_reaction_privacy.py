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

from pyrogram import raw

from .auto_name import AutoName


class PaidReactionPrivacy(AutoName):
    """Reaction privacy type enumeration used in :meth:`~pyrogram.Client.send_paid_reaction`."""

    DEFAULT = raw.types.PaidReactionPrivacyDefault
    "Send default reaction"

    ANONYMOUS = raw.types.PaidReactionPrivacyAnonymous
    "Send anonymous reaction"

    CHAT = raw.types.PaidReactionPrivacyPeer
    "Send reaction as specific chat. You can get all available chats in :meth:`~pyrogram.Client.get_send_as_chats`"
