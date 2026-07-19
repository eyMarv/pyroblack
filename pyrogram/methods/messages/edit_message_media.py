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

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

from .inline_session import get_session

if TYPE_CHECKING:
    from datetime import datetime


class EditMessageMedia:
    async def edit_message_media(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        media: types.InputMedia,
        reply_markup: types.InlineKeyboardMarkup = None,
        schedule_date: datetime | None = None,
        business_connection_id: str | None = None,
        **kwargs,
    ) -> types.Message:
        """Edit animation, audio, document, photo or video messages, or to add media to text messages.

        If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo or a video otherwise. Otherwise, the
        message type can be changed arbitrarily.

        Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message to be edited was sent

        Returns
        -------
            :obj:`~pyrogram.types.Message`: On success, the edited message is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio

                # Replace the current media with a local photo
                await app.edit_message_media(chat_id, message_id,
                    InputMediaPhoto("new_photo.jpg"))

                # Replace the current media with a local video
                await app.edit_message_media(chat_id, message_id,
                    InputMediaVideo("new_video.mp4"))

                # Replace the current media with a local audio
                await app.edit_message_media(chat_id, message_id,
                    InputMediaAudio("new_audio.mp3"))

        """
        caption = media.caption
        parse_mode = media.parse_mode
        caption_entities = media.caption_entities

        message, entities = None, None

        if caption is not None:
            message, entities = (
                await utils.parse_text_entities(
                    self, caption, parse_mode, caption_entities
                )
            ).values()

        if media is not None and not isinstance(
            media,
            (
                types.InputMediaPhoto,
                types.InputMediaVideo,
                types.InputMediaAudio,
                types.InputMediaAnimation,
                types.InputMediaDocument,
            ),
        ):
            msg = f"Unsupported media type: {type(media)}"
            raise ValueError(msg)

        raw_media, _show_caption_above_media = await media.write(
            client=self,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
        )

        rpc = raw.functions.messages.EditMessage(
            peer=await self.resolve_peer(chat_id),
            id=message_id,
            media=raw_media,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            message=message,
            entities=entities,
            invert_media=_show_caption_above_media,
            schedule_date=utils.datetime_to_timestamp(schedule_date),
        )
        session = None
        business_connection = None
        if business_connection_id:
            business_connection = self.business_user_connection_cache[
                business_connection_id
            ]
            if business_connection is None:
                business_connection = await self.get_business_connection(
                    business_connection_id
                )
            session = await get_session(
                self,
                business_connection._raw.connection.dc_id,
            )
        if business_connection_id:
            r = await session.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc,
                    connection_id=business_connection_id,
                ),
            )
            # await session.stop()
        else:
            r = await self.invoke(rpc)

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateEditMessage,
                    raw.types.UpdateEditChannelMessage,
                    raw.types.UpdateNewScheduledMessage,
                ),
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                    replies=self.fetch_replies,
                )
            if isinstance(
                i,
                (raw.types.UpdateBotEditBusinessMessage),
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    business_connection_id=getattr(
                        i, "connection_id", business_connection_id
                    ),
                    raw_reply_to_message=i.reply_to_message,
                    replies=0,
                )
        return None
