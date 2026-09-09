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

"""Decorator names used by the other Pyrogram forks.

kurigram, wzgram and DzGram spell several decorators without pyroblack's ``bot_``
infix, and use ``on_message_reaction`` where pyroblack has
``on_message_reaction_updated``. Porting a bot between forks otherwise fails at
import time with ``AttributeError``.

Each alias below is the *same function object* as the pyroblack decorator it
points at, so the two names register the identical handler — there is no second
code path to keep in sync.
"""

from __future__ import annotations

from .on_bot_business_connect import OnBotBusinessConnect
from .on_bot_business_connection import OnBotBusinessConnection
from .on_bot_business_message import OnBotBusinessMessage
from .on_bot_purchased_paid_media import OnBotPurchasedPaidMedia
from .on_deleted_bot_business_messages import OnDeletedBotBusinessMessages
from .on_edited_bot_business_message import OnEditedBotBusinessMessage
from .on_message_reaction_count_updated import OnMessageReactionCountUpdated
from .on_message_reaction_updated import OnMessageReactionUpdated


class ForkDecoratorAliases:
    """Alternative decorator spellings from the other forks."""

    # kurigram / wzgram / DzGram
    on_business_message = OnBotBusinessMessage.on_bot_business_message
    on_business_connection = OnBotBusinessConnection.on_bot_business_connection
    on_business_connect = OnBotBusinessConnect.on_bot_business_connect
    on_edited_business_message = (
        OnEditedBotBusinessMessage.on_edited_bot_business_message
    )
    on_deleted_business_messages = (
        OnDeletedBotBusinessMessages.on_deleted_bot_business_messages
    )
    on_purchased_paid_media = OnBotPurchasedPaidMedia.on_bot_purchased_paid_media
    on_message_reaction = OnMessageReactionUpdated.on_message_reaction_updated
    on_message_reaction_count = (
        OnMessageReactionCountUpdated.on_message_reaction_count_updated
    )
