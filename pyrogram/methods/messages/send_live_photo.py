#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os
from datetime import datetime
from typing import List, Optional, Union
import re

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType


class SendLivePhoto:
    async def send_live_photo(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        photo: Union[str, "types.InputMediaPhoto"],
        video: Optional[str] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        reply_parameters: Optional["types.ReplyParameters"] = None,
        schedule_date: Optional[datetime] = None,
        protect_content: Optional[bool] = None,
        business_connection_id: Optional[str] = None,
    ) -> "types.Message":
        """Send a live photo (motion photo).

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            photo (``str`` | :obj:`~pyrogram.types.InputMediaPhoto`):
                Photo to send. Pass a file path, file_id, URL, or InputMediaPhoto.

            video (``str``, *optional*):
                Short video clip to accompany the live photo.

            caption (``str``, *optional*):
                Photo caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                Text parse mode.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                Special entities for the caption.

            disable_notification (``bool``, *optional*):
                Sends the message silently.

            message_thread_id (``int``, *optional*):
                Target message thread identifier for forum topics.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Reply parameters.

            schedule_date (:obj:`~datetime.datetime`, *optional*):
                Scheduled send date.

            protect_content (``bool``, *optional*):
                Protect from forwarding and saving.

            business_connection_id (``str``, *optional*):
                Business connection identifier.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message.
        """
        caption, caption_entities = (
            await utils.parse_text_entities(self, caption, parse_mode, caption_entities)
        ).values()

        if isinstance(photo, types.InputMediaPhoto):
            if os.path.isfile(photo.media):
                media = raw.types.InputMediaUploadedPhoto(
                    file=await self.save_file(photo.media),
                    live_photo=True,
                    video=await self.save_file(video) if video else None,
                )
            elif re.match("^https?://", photo.media):
                media = raw.types.InputMediaPhotoExternal(url=photo.media)
            else:
                media = utils.get_input_media_from_file_id(photo.media, FileType.PHOTO)
                if hasattr(media, 'id'):
                    media = raw.types.InputMediaPhoto(id=media.id, live_photo=True)
        elif isinstance(photo, str):
            if os.path.isfile(photo):
                media = raw.types.InputMediaUploadedPhoto(
                    file=await self.save_file(photo),
                    live_photo=True,
                    video=await self.save_file(video) if video else None,
                )
            elif re.match("^https?://", photo):
                media = raw.types.InputMediaPhotoExternal(url=photo)
            else:
                media = utils.get_input_media_from_file_id(photo, FileType.PHOTO)
                if hasattr(media, 'id'):
                    media = raw.types.InputMediaPhoto(id=media.id, live_photo=True)
        else:
            media = raw.types.InputMediaUploadedPhoto(
                file=await self.save_file(photo),
                live_photo=True,
                video=await self.save_file(video) if video else None,
            )

        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=media,
            message=caption,
            entities=caption_entities,
            silent=disable_notification or None,
            random_id=self.rnd_id(),
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            reply_to=await utils._get_reply_message_parameters(
                self, message_thread_id, reply_parameters
            ),
        )

        if business_connection_id is not None:
            r = await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    connection_id=business_connection_id, query=rpc
                )
            )
        else:
            r = await self.invoke(rpc, sleep_threshold=60)

        return await utils.parse_messages(self, r)
