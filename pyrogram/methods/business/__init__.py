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

from .answer_pre_checkout_query import AnswerPreCheckoutQuery
from .answer_shipping_query import AnswerShippingQuery
from .create_business_chat_link import CreateBusinessChatLink
from .create_invoice_link import CreateInvoiceLink
from .delete_business_chat_link import DeleteBusinessChatLink
from .delete_business_messages import DeleteBusinessMessages
from .get_available_gifts import GetAvailableGifts
from .get_business_account_gifts import GetBusinessAccountGifts
from .get_business_account_star_balance import GetBusinessAccountStarBalance
from .get_business_chat_links import GetBusinessChatLinks
from .get_business_connection import GetBusinessConnection
from .get_collectible_item_info import GetCollectibleItemInfo
from .get_connected_bots import GetConnectedBots
from .get_owned_star_count import GetOwnedStarCount
from .get_payment_form import GetPaymentForm
from .refund_star_payment import RefundStarPayment
from .resolve_business_chat_link import ResolveBusinessChatLink
from .send_invoice import SendInvoice
from .send_payment_form import SendPaymentForm
from .transfer_business_account_stars import TransferBusinessAccountStars
from .update_business_away_message import UpdateBusinessAwayMessage
from .update_business_greeting_message import UpdateBusinessGreetingMessage
from .update_business_intro import UpdateBusinessIntro
from .update_business_location import UpdateBusinessLocation
from .update_business_work_hours import UpdateBusinessWorkHours


class TelegramBusiness(
    AnswerPreCheckoutQuery,
    AnswerShippingQuery,
    CreateInvoiceLink,
    GetBusinessConnection,
    GetCollectibleItemInfo,
    RefundStarPayment,
    SendInvoice,
    GetPaymentForm,
    SendPaymentForm,
    GetAvailableGifts,
    GetOwnedStarCount,
    CreateBusinessChatLink,
    DeleteBusinessChatLink,
    DeleteBusinessMessages,
    GetBusinessAccountGifts,
    GetBusinessAccountStarBalance,
    GetBusinessChatLinks,
    GetConnectedBots,
    ResolveBusinessChatLink,
    TransferBusinessAccountStars,
    UpdateBusinessAwayMessage,
    UpdateBusinessGreetingMessage,
    UpdateBusinessIntro,
    UpdateBusinessLocation,
    UpdateBusinessWorkHours,
):
    pass
