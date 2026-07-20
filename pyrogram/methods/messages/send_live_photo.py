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

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, BinaryIO, Callable

import pyrogram
from pyrogram import StopTransmission, enums, raw, types, utils
from pyrogram.errors import FilePartMissing

if TYPE_CHECKING:
    from datetime import datetime

log = logging.getLogger(__name__)


class SendLivePhoto:
    async def send_live_photo(
        self: pyrogram.Client,
        chat_id: int | str,
        live_photo: str | BinaryIO,
        photo: str | BinaryIO,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        has_spoiler: bool | None = None,
        width: int = 0,
        height: int = 0,
        disable_notification: bool | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        effect_id: int | None = None,
        show_caption_above_media: bool | None = None,
        reply_parameters: types.ReplyParameters = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        business_connection_id: str | None = None,
        allow_paid_broadcast: bool | None = None,
        paid_message_star_count: int | None = None,
        suggested_post_parameters: types.SuggestedPostParameters = None,
        reply_markup: types.InlineKeyboardMarkup
        | types.ReplyKeyboardMarkup
        | types.ReplyKeyboardRemove
        | types.ForceReply = None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message | None:
        """Send a live photo.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            live_photo (``str`` | ``BinaryIO``):
                Live photo video to send.
                The video must be no longer than 10 seconds and must not exceed 10 MB in size.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet,
                pass a file path as string to upload a new video that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            photo (``str`` | ``BinaryIO``):
                The static photo to send.
                Pass a file_id as string to send a photo that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a photo from the Internet,
                pass a file path as string to upload a new photo that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            caption (``str``, *optional*):
                Photo caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the photo needs to be covered with a spoiler animation.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                For forums only.

            direct_messages_topic_id (``int``, *optional*):
                Unique identifier of the topic in a channel direct messages chat administered by the current user.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Describes reply parameters for the message that is being sent.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            suggested_post_parameters (:obj:`~pyrogram.types.SuggestedPostParameters`, *optional*):
                Information about the suggested post.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``None``: On success, the sent live photo message is returned, otherwise, in
            case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned.

        """
        peer = await self.resolve_peer(chat_id)

        if direct_messages_topic_id:
            _, reply_parameters = utils._get_reply_to_message_quote_ids(
                reply_parameters=reply_parameters,
                direct_messages_topic_id=direct_messages_topic_id,
            )

        reply_to = await utils._get_reply_message_parameters(
            self,
            message_thread_id,
            reply_parameters,
        )

        try:
            while True:
                try:
                    media = await types.InputMediaLivePhoto(
                        media=live_photo,
                        photo=photo,
                        caption=caption,
                        parse_mode=parse_mode,
                        caption_entities=caption_entities,
                        has_spoiler=has_spoiler,
                        show_caption_above_media=show_caption_above_media,
                    ).write(
                        self,
                        chat_id=chat_id,
                        width=width,
                        height=height,
                        progress=progress,
                        progress_args=progress_args,
                    )

                    if isinstance(media, tuple):
                        media, invert_media = media
                    else:
                        invert_media = show_caption_above_media

                    text_entities = await utils.parse_text_entities(
                        self,
                        caption,
                        parse_mode,
                        caption_entities,
                    )
                    message = ""
                    entities = None
                    if isinstance(text_entities, dict):
                        message = text_entities.get("message", "")
                        entities = text_entities.get("entities")

                    rpc = raw.functions.messages.SendMedia(
                        peer=peer,
                        media=media,
                        silent=disable_notification or None,
                        invert_media=invert_media,
                        reply_to=reply_to,
                        random_id=self.rnd_id(),
                        schedule_date=utils.datetime_to_timestamp(schedule_date),
                        noforwards=protect_content,
                        allow_paid_floodskip=allow_paid_broadcast,
                        allow_paid_stars=paid_message_star_count,
                        suggested_post=suggested_post_parameters.write()
                        if suggested_post_parameters
                        else None,
                        reply_markup=await reply_markup.write(self)
                        if reply_markup
                        else None,
                        effect=effect_id,
                        message=message,
                        entities=entities,
                    )

                    if business_connection_id:
                        r = await self.invoke(
                            raw.functions.InvokeWithBusinessConnection(
                                query=rpc,
                                connection_id=business_connection_id,
                            ),
                        )
                    else:
                        r = await self.invoke(rpc)
                except FilePartMissing as e:
                    await self.save_file(live_photo, file_id=None, file_part=e.value)
                else:
                    messages = await utils.parse_messages(client=self, messages=r)
                    return messages[0] if messages else None
        except StopTransmission:
            return None
