#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

import logging
from typing import List, Optional, Union

import pyrogram
from pyrogram import enums, raw, utils, types

log = logging.getLogger(__name__)


class SendInvoice:
    async def send_invoice(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        title: str,
        description: str,
        payload: Union[str, bytes],
        currency: str,
        prices: List["types.LabeledPrice"],
        message_thread_id: Optional[int] = None,
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[int] = None,
        reply_parameters: Optional["types.ReplyParameters"] = None,
        allow_paid_broadcast: Optional[bool] = None,
        direct_messages_topic_id: Optional[int] = None,
        suggested_post_parameters: Optional["types.SuggestedPostParameters"] = None,
        subscription_expiration_date: Optional[int] = None,
        reply_markup: Optional[
            Union[
                "types.InlineKeyboardMarkup",
                "types.ReplyKeyboardMarkup",
                "types.ReplyKeyboardRemove",
                "types.ForceReply"
            ]
        ] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: Optional[List["types.MessageEntity"]] = None,

        reply_to_message_id: Optional[int] = None,
    ) -> "types.Message":
        """Use this method to send invoices.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            title (``str``):
                Product name, 1-32 characters.

            description (``str``):
                Product description, 1-255 characters.

            payload (``str`` | ``bytes``):
                Bot-defined invoice payload, 1-128 bytes.

            currency (``str``):
                Three-letter ISO 4217 currency code.

            prices (List of :obj:`~pyrogram.types.LabeledPrice`):
                Price breakdown.

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Describes reply parameters for the message that is being sent.

            provider_token (``str``, *optional*):
                Payment provider token.

            max_tip_amount (``int``, *optional*):
                The maximum accepted amount for tips.

            suggested_tip_amounts (List of ``int``, *optional*):
                An array of suggested amounts of tips.

            start_parameter (``str``, *optional*):
                Unique deep-linking parameter.

            provider_data (``str``, *optional*):
                JSON-serialized data about the invoice.

            photo_url (``str``, *optional*):
                URL of the product photo for the invoice.

            photo_size (``int``, *optional*):
                Photo size in bytes.

            photo_width (``int``, *optional*):
                Photo width.

            photo_height (``int``, *optional*):
                Photo height.

            need_name (``bool``, *optional*):
                Pass True if you require the user's full name.

            need_phone_number (``bool``, *optional*):
                Pass True if you require the user's phone number.

            need_email (``bool``, *optional*):
                Pass True if you require the user's email address.

            need_shipping_address (``bool``, *optional*):
                Pass True if you require the user's shipping address.

            send_phone_number_to_provider (``bool``, *optional*):
                Pass True if the user's phone number should be sent to the provider.

            send_email_to_provider (``bool``, *optional*):
                Pass True if the user's email address should be sent to the provider.

            is_flexible (``bool``, *optional*):
                Pass True if the final price depends on the shipping method.

            disable_notification (``bool``, *optional*):
                Sends the message silently.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect.

            allow_paid_broadcast (``bool``, *optional*):
                Allow paid broadcast.

            direct_messages_topic_id (``int``, *optional*):
                Unique identifier of the topic in a channel direct messages chat.

            suggested_post_parameters (:obj:`~pyrogram.types.SuggestedPostParameters`, *optional*):
                Information about the suggested post.

            subscription_expiration_date (``int``, *optional*):
                Expiration date of the subscription.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                Additional interface options.

            caption (``str``, *optional*):
                Document caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                Parse mode for the caption.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities in the caption.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent invoice message is returned.
        """
        if reply_to_message_id is not None:
            log.warning(
                "`reply_to_message_id` is deprecated and will be removed in future updates. Use `reply_parameters` instead."
            )

            reply_parameters = types.ReplyParameters(
                message_id=reply_to_message_id
            )

        media = raw.types.InputMediaInvoice(
            title=title,
            description=description,
            photo=raw.types.InputWebDocument(
                url=photo_url,
                mime_type="image/jpg",
                size=photo_size,
                attributes=[
                    raw.types.DocumentAttributeImageSize(
                        w=photo_width,
                        h=photo_height
                    )
                ]
            ) if photo_url else None,
            invoice=raw.types.Invoice(
                currency=currency,
                prices=[i.write() for i in prices],
                test=self.test_mode,
                name_requested=need_name,
                phone_requested=need_phone_number,
                email_requested=need_email,
                shipping_address_requested=need_shipping_address,
                flexible=is_flexible,
                phone_to_provider=send_phone_number_to_provider,
                email_to_provider=send_email_to_provider,
                max_tip_amount=max_tip_amount,
                suggested_tip_amounts=suggested_tip_amounts,
                recurring=True if subscription_expiration_date is not None else None,
                subscription_period=subscription_expiration_date
            ),
            payload=payload.encode() if isinstance(payload, str) else payload,
            provider=provider_token,
            provider_data=raw.types.DataJSON(
                data=provider_data if provider_data else "{}"
            ),
            start_param=start_parameter
        )

        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=media,
            silent=disable_notification or None,
            reply_to=await utils.get_reply_to(
                self,
                reply_parameters,
                message_thread_id,
                direct_messages_topic_id=direct_messages_topic_id
            ),
            random_id=self.rnd_id(),
            noforwards=protect_content,
            allow_paid_floodskip=allow_paid_broadcast,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            effect=message_effect_id,
            suggested_post=suggested_post_parameters.write() if suggested_post_parameters else None,
            **await utils.parse_text_entities(self, caption, parse_mode, caption_entities)
        )

        r = await self.invoke(rpc)

        messages = await utils.parse_messages(client=self, messages=r)

        return messages[0] if messages else None
