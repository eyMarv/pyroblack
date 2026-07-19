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

import os
from typing import BinaryIO, Callable

import pyrogram
from pyrogram import StopTransmission, enums, raw, types, utils
from pyrogram.errors import FilePartMissing
from pyrogram.file_id import FileId


class EditStoryMedia:
    async def edit_story_media(
        self: pyrogram.Client,
        chat_id: int | str,
        story_id: int,
        media: str | BinaryIO | None = None,
        media_areas: list[types.MediaArea] | None = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: str | BinaryIO | None = None,
        supports_streaming: bool = True,
        file_name: str | None = None,
        caption: str | None = None,
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        music: str | types.Document | None = None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Story:
        """Edit story media.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

            story_id (``int``):
                Story identifier in the chat specified in chat_id.

            media (``str`` | ``BinaryIO``, *optional*):
                Video or photo to send.
                Pass a file_id as string to send a animation that exists on the Telegram servers,
                pass a file path as string to upload a new animation that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            media_areas (List of :obj:`~pyrogram.types.MediaArea`, *optional*):
                List of media areas to edit in the story.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            supports_streaming (``bool``, *optional*):
                Pass True, if the uploaded video is suitable for streaming.

            file_name (``str``, *optional*):
                File name of the story sent.

            caption (``str``, *optional*):
                Story caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Returns
        -------
            :obj:`~pyrogram.types.Story`: On success, the edited story is returned.

        Example:
            .. code-block:: python

                # Replace the current media with a local photo
                await app.edit_story_media(chat_id, story_id, "new_photo.jpg")

                # Replace the current media with a local video
                await app.edit_story_media(chat_id, story_id, "new_video.mp4")

        """
        try:
            if isinstance(media, str):
                if os.path.isfile(media):
                    thumb = await self.save_file(thumb)
                    file = await self.save_file(
                        media, progress=progress, progress_args=progress_args
                    )
                    mime_type = self.guess_mime_type(file.name)
                    if mime_type == "video/mp4":
                        media = raw.types.InputMediaUploadedDocument(
                            mime_type=mime_type,
                            file=file,
                            thumb=thumb,
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    supports_streaming=supports_streaming or None,
                                    duration=duration,
                                    w=width,
                                    h=height,
                                ),
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media)
                                ),
                            ],
                        )
                    else:
                        media = raw.types.InputMediaUploadedPhoto(
                            file=file,
                        )
                else:
                    media = utils.get_input_media_from_file_id(media)
            else:
                thumb = await self.save_file(thumb)
                file = await self.save_file(
                    media, progress=progress, progress_args=progress_args
                )
                mime_type = self.guess_mime_type(file.name)
                if mime_type == "video/mp4":
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=mime_type,
                        file=file,
                        thumb=thumb,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=supports_streaming or None,
                                duration=duration,
                                w=width,
                                h=height,
                            ),
                            raw.types.DocumentAttributeFilename(
                                file_name=file_name or media.name
                            ),
                        ],
                    )
                else:
                    media = raw.types.InputMediaUploadedPhoto(
                        file=file,
                    )

            message, entities = (
                await utils.parse_text_entities(
                    self, caption, parse_mode, caption_entities
                )
            ).values()

            music_doc = None
            if music:
                if isinstance(music, str):
                    decoded = FileId.decode(music)
                    music_doc = raw.types.InputDocument(
                        id=decoded.media_id,
                        access_hash=decoded.access_hash,
                        file_reference=decoded.file_reference,
                    )
                else:
                    music_doc = raw.types.InputDocument(
                        id=music.id,
                        access_hash=music.access_hash,
                        file_reference=music.file_ref,
                    )

            while True:
                try:
                    r = await self.invoke(
                        raw.functions.stories.EditStory(
                            peer=await self.resolve_peer(chat_id),
                            id=story_id,
                            media=media,
                            media_areas=[
                                await area.write(self) for area in (media_areas or [])
                            ]
                            or None,
                            caption=message,
                            entities=entities,
                            privacy_rules=None,
                            music=music_doc,
                        ),
                    )
                except FilePartMissing as e:
                    await self.save_file(media, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(i, raw.types.UpdateStory):
                            return await types.Story._parse(
                                self,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                None,
                                None,
                                i,
                                None,
                                i.peer,
                            )
        except StopTransmission:
            return None
