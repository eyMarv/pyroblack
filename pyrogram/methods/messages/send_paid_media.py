#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

import os
import re

from datetime import datetime
from pymediainfo import MediaInfo
from typing import Union, List, Optional

import pyrogram
from pyrogram import raw, utils, enums
from pyrogram import types
from pyrogram.file_id import FileType


class SendPaidMedia:
    async def send_paid_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        stars_amount: int,
        media: List[
            Union[
                "types.InputMediaAnimation",
                "types.InputMediaPhoto",
                "types.InputMediaVideo",
                "types.InputPaidMediaPhoto",
                "types.InputPaidMediaVideo",
            ]
        ],
        business_connection_id: str = None,
        caption: str = "",
        caption_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        disable_notification: bool = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        invert_media: bool = None,
        payload: str = None,
    ) -> "types.Message":
        """Send paid media.
        Only for channels.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel (in the format @channelusername).

            stars_amount (``int``):
                Amount of stars.

            media (List of :obj:`~pyrogram.types.InputMediaAnimation` | :obj:`~pyrogram.types.InputMediaPhoto` | :obj:`~pyrogram.types.InputMediaVideo` | :obj:`~pyrogram.types.InputPaidMediaPhoto` | :obj:`~pyrogram.types.InputPaidMediaVideo`):
                A list of media to send.

            business_connection_id (``str``, *optional*):
                Unique identifier for the target business connection.
                for business bots only.

            caption (``str``, *optional*):
                Media caption, 0-1024 characters.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                Special entities that appear in the caption, which can be specified instead of parse_mode.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.

            disable_notification (``bool``, *optional*):
                Sends the message silently. Users will receive a notification with no sound.

            schedule_date (:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent. Pass a :obj:`~datetime.datetime` object.

            protect_content (``bool``, *optional*):
                Protect content from being forwarded.

            invert_media (``bool``, *optional*):
                Invert the media.

            payload (``str``, *optional*):
                Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.

        Example:
            .. code-block:: python

                app.send_paid_media(
                    chat_id="pyrogram",
                    stars_amount=100,
                    media=[
                        types.InputMediaPhoto("/path/to/photo.jpg"),
                        types.InputMediaVideo("video_file_id")
                    ],
                    caption="This is a paid media message."
                )
        """
        multi_media = []
        peer = await self.resolve_peer(chat_id)

        for i in media:
            if isinstance(i, (types.InputMediaPhoto, types.InputPaidMediaPhoto)):
                has_spoiler = getattr(i, "has_spoiler", None)
                if isinstance(i.media, str):
                    if os.path.isfile(i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=peer,
                                media=raw.types.InputMediaUploadedPhoto(
                                    file=await self.save_file(i.media),
                                    spoiler=has_spoiler,
                                ),
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                            spoiler=has_spoiler,
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=peer,
                                media=raw.types.InputMediaPhotoExternal(
                                    url=i.media, spoiler=has_spoiler
                                ),
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                            spoiler=has_spoiler,
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.PHOTO, has_spoiler=has_spoiler
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=peer,
                            media=raw.types.InputMediaUploadedPhoto(
                                file=await self.save_file(i.media),
                                spoiler=has_spoiler,
                            ),
                        )
                    )

                    media = raw.types.InputMediaPhoto(
                        id=raw.types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash,
                            file_reference=media.photo.file_reference,
                        ),
                        spoiler=has_spoiler,
                    )
            elif isinstance(
                i,
                (
                    types.InputMediaVideo,
                    types.InputMediaAnimation,
                    types.InputPaidMediaVideo,
                ),
            ):
                has_spoiler = getattr(i, "has_spoiler", None)
                thumb = getattr(i, "thumb", None)
                if thumb is None:
                    thumb = getattr(i, "thumbnail", None)

                video_cover = None
                cover = getattr(i, "cover", None)
                if cover is not None:
                    if isinstance(cover, str):
                        if os.path.isfile(cover):
                            cover_media = await self.invoke(
                                raw.functions.messages.UploadMedia(
                                    peer=peer,
                                    media=raw.types.InputMediaUploadedPhoto(
                                        file=await self.save_file(cover),
                                    ),
                                )
                            )
                            video_cover = raw.types.InputPhoto(
                                id=cover_media.photo.id,
                                access_hash=cover_media.photo.access_hash,
                                file_reference=cover_media.photo.file_reference,
                            )
                        elif re.match("^https?://", cover):
                            cover_media = await self.invoke(
                                raw.functions.messages.UploadMedia(
                                    peer=peer,
                                    media=raw.types.InputMediaPhotoExternal(
                                        url=cover,
                                    ),
                                )
                            )
                            video_cover = raw.types.InputPhoto(
                                id=cover_media.photo.id,
                                access_hash=cover_media.photo.access_hash,
                                file_reference=cover_media.photo.file_reference,
                            )
                        else:
                            video_cover = utils.get_input_media_from_file_id(
                                cover,
                                FileType.PHOTO,
                            ).id
                    else:
                        cover_media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=peer,
                                media=raw.types.InputMediaUploadedPhoto(
                                    file=await self.save_file(cover),
                                ),
                            )
                        )
                        video_cover = raw.types.InputPhoto(
                            id=cover_media.photo.id,
                            access_hash=cover_media.photo.access_hash,
                            file_reference=cover_media.photo.file_reference,
                        )

                start_timestamp = getattr(i, "start_timestamp", None)
                if isinstance(i.media, str):
                    is_animation = False
                    if os.path.isfile(i.media):
                        try:
                            video_info = MediaInfo.parse(i.media)
                        except OSError:
                            is_animation = isinstance(i, types.InputMediaAnimation)
                        else:
                            if not any(
                                track.track_type == "Audio" for track in video_info.tracks
                            ):
                                is_animation = True
                        attributes = [
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=(
                                    True
                                    if is_animation
                                    else (i.supports_streaming or None)
                                ),
                                duration=i.duration,
                                w=i.width,
                                h=i.height,
                            ),
                            raw.types.DocumentAttributeFilename(
                                file_name=os.path.basename(i.media)
                            ),
                        ]
                        if is_animation:
                            attributes.append(raw.types.DocumentAttributeAnimated())
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=peer,
                                media=raw.types.InputMediaUploadedDocument(
                                    file=await self.save_file(i.media),
                                    thumb=await self.save_file(thumb),
                                    spoiler=has_spoiler,
                                    mime_type=self.guess_mime_type(i.media)
                                    or "video/mp4",
                                    nosound_video=is_animation,
                                    attributes=attributes,
                                    video_cover=video_cover,
                                    video_timestamp=start_timestamp,
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                            spoiler=has_spoiler,
                            video_cover=video_cover,
                            video_timestamp=start_timestamp,
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=peer,
                                media=raw.types.InputMediaDocumentExternal(
                                    url=i.media,
                                    spoiler=has_spoiler,
                                    video_cover=video_cover,
                                    video_timestamp=start_timestamp,
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                            spoiler=has_spoiler,
                            video_cover=video_cover,
                            video_timestamp=start_timestamp,
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.VIDEO, has_spoiler=has_spoiler
                        )
                        media.video_cover = video_cover
                        media.video_timestamp = start_timestamp
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=peer,
                            media=raw.types.InputMediaUploadedDocument(
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(thumb),
                                spoiler=has_spoiler,
                                mime_type=self.guess_mime_type(
                                    getattr(i.media, "name", "video.mp4")
                                )
                                or "video/mp4",
                                attributes=[
                                    raw.types.DocumentAttributeVideo(
                                        supports_streaming=i.supports_streaming or None,
                                        duration=i.duration,
                                        w=i.width,
                                        h=i.height,
                                    ),
                                    raw.types.DocumentAttributeFilename(
                                        file_name=getattr(i.media, "name", "video.mp4")
                                    ),
                                ],
                                video_cover=video_cover,
                                video_timestamp=start_timestamp,
                            ),
                        )
                    )

                    media = raw.types.InputMediaDocument(
                        id=raw.types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference,
                        ),
                        spoiler=has_spoiler,
                        video_cover=video_cover,
                        video_timestamp=start_timestamp,
                    )
            else:
                raise ValueError(
                    f"{i.__class__.__name__} is not a supported type for send_paid_media"
                )
            multi_media.append(media)

        rpc = raw.functions.messages.SendMedia(
            peer=peer,
            media=raw.types.InputMediaPaidMedia(
                stars_amount=stars_amount,
                extended_media=multi_media,
                payload=payload,
            ),
            silent=disable_notification or None,
            random_id=self.rnd_id(),
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            invert_media=invert_media,
            **await utils.parse_text_entities(
                self, caption, parse_mode, caption_entities
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

        return await utils.parse_messages(
            self,
            raw.types.messages.Messages(
                messages=[
                    m.message
                    for m in filter(
                        lambda u: isinstance(
                            u,
                            (
                                raw.types.UpdateNewMessage,
                                raw.types.UpdateNewChannelMessage,
                                raw.types.UpdateNewScheduledMessage,
                                raw.types.UpdateBotNewBusinessMessage,
                            ),
                        ),
                        r.updates,
                    )
                ],
                users=r.users,
                chats=r.chats,
            ),
        )
