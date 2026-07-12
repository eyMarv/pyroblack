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

from .on_bot_business_connection import OnBotBusinessConnection
from .on_bot_purchased_paid_media import OnBotPurchasedPaidMedia
from .on_callback_query import OnCallbackQuery
from .on_chat_join_request import OnChatJoinRequest
from .on_chat_member_updated import OnChatMemberUpdated
from .on_chosen_inline_result import OnChosenInlineResult
from .on_deleted_messages import OnDeletedMessages
from .on_disconnect import OnDisconnect
from .on_edited_message import OnEditedMessage
from .on_inline_query import OnInlineQuery
from .on_invoke_err import OnInvokeErr
from .on_message import OnMessage
from .on_poll import OnPoll
from .on_raw_update import OnRawUpdate
from .on_user_status import OnUserStatus
from .on_message_reaction_updated import OnMessageReactionUpdated
from .on_message_reaction_count_updated import OnMessageReactionCountUpdated
from .on_pre_checkout_query import OnPreCheckoutQuery
from .on_shipping_query import OnShippingQuery
from .on_story import OnStory
from .on_managed_bot import OnManagedBot


class Decorators(
    OnMessage,
    OnEditedMessage,
    OnDeletedMessages,
    OnBotBusinessConnection,
    OnMessageReactionUpdated,
    OnMessageReactionCountUpdated,
    OnInlineQuery,
    OnChosenInlineResult,
    OnCallbackQuery,
    OnShippingQuery,
    OnPreCheckoutQuery,
    OnBotPurchasedPaidMedia,
    OnPoll,

    OnChatMemberUpdated,
    OnChatJoinRequest,

    OnDisconnect,
    OnUserStatus,
    OnStory,
    OnManagedBot,
    OnRawUpdate,
    OnInvokeErr,
):
    pass
