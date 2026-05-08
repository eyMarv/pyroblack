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

import io
import os
import re
from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from pyrogram.file_id import FileType

from .inline_session import get_session


class EditMessageMedia:
    async def edit_message_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None,
        file_name: str = None,
        invert_media: bool = False,
        business_connection_id: str = None,
    ) -> "types.Message":
        """Edit animation, audio, document, photo or video messages, or replace text with animation, audio, document, photo or video messages.

        If a message is a part of a message album, then it can be edited only to a photo or a video. Otherwise, the
        message type can be changed arbitrarily.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            file_name (``str``, *optional*):
                File name of the media to be sent. Not applicable to photos.
                Defaults to file's path basename.

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.
                for business bots only.

        Returns:
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
        caption_entities = media.caption_entities
        parse_mode = media.parse_mode

        message, entities = None, None

        if caption is not None:
            message, entities = (
                await utils.parse_text_entities(
                    self, caption, parse_mode, caption_entities
                )
            ).values()

        if isinstance(media, types.InputMediaPhoto):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.functions.InputMediaUploadedPhoto(
                            file=await self.save_file(media.media),
                            spoiler=media.has_spoiler,
                        ),
                    )
                )

                media = raw.functions.InputMediaPhoto(
                    id=raw.functions.InputPhoto(
                        id=uploaded_media.photo.id,
                        access_hash=uploaded_media.photo.access_hash,
                        file_reference=uploaded_media.photo.file_reference,
                    ),
                    spoiler=media.has_spoiler,
                )
            elif re.match("^https?://", media.media):
                media = raw.functions.InputMediaPhotoExternal(
                    url=media.media, spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.PHOTO)
        elif isinstance(media, types.InputMediaVideo):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.functions.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "video/mp4",
                            thumb=await self.save_file(media.thumb),
                            spoiler=media.has_spoiler,
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.functions.DocumentAttributeVideo(
                                    supports_streaming=media.supports_streaming or None,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height,
                                ),
                                raw.functions.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media.media)
                                ),
                            ],
                        ),
                    )
                )

                media = raw.functions.InputMediaDocument(
                    id=raw.functions.InputDocument(
                        id=uploaded_media.document.id,
                        access_hash=uploaded_media.document.access_hash,
                        file_reference=uploaded_media.document.file_reference,
                    ),
                    spoiler=media.has_spoiler,
                )
            elif re.match("^https?://", media.media):
                media = raw.functions.InputMediaDocumentExternal(
                    url=media.media, spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.VIDEO)
        elif isinstance(media, types.InputMediaAudio):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.functions.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "audio/mpeg",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.functions.DocumentAttributeAudio(
                                    duration=media.duration,
                                    performer=media.performer,
                                    title=media.title,
                                ),
                                raw.functions.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media.media)
                                ),
                            ],
                        ),
                    )
                )

                media = raw.functions.InputMediaDocument(
                    id=raw.functions.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=media.document.file_reference,
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.functions.InputMediaDocumentExternal(url=media.media)
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.AUDIO)
        elif isinstance(media, types.InputMediaAnimation):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.functions.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "video/mp4",
                            thumb=await self.save_file(media.thumb),
                            spoiler=media.has_spoiler,
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.functions.DocumentAttributeVideo(
                                    supports_streaming=True,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height,
                                ),
                                raw.functions.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media.media)
                                ),
                                raw.functions.DocumentAttributeAnimated(),
                            ],
                        ),
                    )
                )

                media = raw.functions.InputMediaDocument(
                    id=raw.functions.InputDocument(
                        id=uploaded_media.document.id,
                        access_hash=uploaded_media.document.access_hash,
                        file_reference=uploaded_media.document.file_reference,
                    ),
                    spoiler=media.has_spoiler,
                )
            elif re.match("^https?://", media.media):
                media = raw.functions.InputMediaDocumentExternal(
                    url=media.media, spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, FileType.ANIMATION
                )
        elif isinstance(media, types.InputMediaDocument):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.functions.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media)
                            or "application/zip",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.functions.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media.media)
                                )
                            ],
                        ),
                    )
                )

                media = raw.functions.InputMediaDocument(
                    id=raw.functions.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=media.document.file_reference,
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.functions.InputMediaDocumentExternal(url=media.media)
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, FileType.DOCUMENT
                )

        rpc = raw.functions.messages.EditMessage(
            peer=await self.resolve_peer(chat_id),
            id=message_id,
            media=media,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            message=message,
            entities=entities,
            invert_media=invert_media,
        )
        session = None
        business_connection = None
        if business_connection_id:
            business_connection = self.business_user_connection_cache[
                business_connection_id
            ]
            if not business_connection:
                business_connection = await self.get_business_connection(
                    business_connection_id
                )
            session = await get_session(self, business_connection._raw.connection.dc_id)
        if business_connection_id:
            r = await session.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc, connection_id=business_connection_id
                )
            )
            # await session.stop()
        else:
            r = await self.invoke(rpc)

        for i in r.updates:
            if isinstance(
                i, (raw.functions.UpdateEditMessage, raw.functions.UpdateEditChannelMessage)
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                )
            elif isinstance(i, (raw.functions.UpdateBotEditBusinessMessage)):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    business_connection_id=getattr(
                        i, "connection_id", business_connection_id
                    ),
                    replies=0,
                )
