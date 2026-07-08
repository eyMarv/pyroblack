from typing import Union

import pyrogram
from pyrogram import raw, types

from ..object import Object


class PaidMedia(Object):
    """This object describes paid media.

    Currently, it can be one of:

    - :obj:`~pyrogram.types.PaidMediaPreview`
    - :obj:`~pyrogram.types.PaidMediaPhoto`
    - :obj:`~pyrogram.types.PaidMediaVideo`
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        extended_media: Union[
            "raw.types.MessageExtendedMediaPreview",
            "raw.types.MessageExtendedMedia",
        ],
    ) -> "PaidMedia":
        if isinstance(extended_media, raw.types.MessageExtendedMediaPreview):
            return types.PaidMediaPreview(
                width=getattr(extended_media, "w", None),
                height=getattr(extended_media, "h", None),
                duration=getattr(extended_media, "video_duration", None),
                minithumbnail=types.StrippedThumbnail(
                    client=client,
                    data=getattr(getattr(extended_media, "thumb", None), "bytes", None),
                ) if getattr(extended_media, "thumb", None) else None,
            )

        if isinstance(extended_media, raw.types.MessageExtendedMedia):
            media = extended_media.media
            has_media_spoiler = getattr(media, "spoiler", None)
            ttl_seconds = getattr(media, "ttl_seconds", None)

            if isinstance(media, raw.types.MessageMediaPhoto):
                photo = types.Photo._parse(client, media.photo, ttl_seconds)
                return types.PaidMediaPhoto(photo=photo)

            if isinstance(media, raw.types.MessageMediaDocument):
                document = media.document

                if isinstance(document, raw.types.Document):
                    attributes = {type(i): i for i in document.attributes}
                    file_name = getattr(
                        attributes.get(raw.types.DocumentAttributeFilename, None),
                        "file_name",
                        None,
                    )

                    if raw.types.DocumentAttributeVideo in attributes:
                        video_attributes = attributes[raw.types.DocumentAttributeVideo]

                        if not video_attributes.round_message:
                            video = types.Video._parse(
                                client,
                                document,
                                video_attributes,
                                file_name,
                                ttl_seconds,
                                getattr(media, "video_cover", None),
                                getattr(media, "video_timestamp", None),
                            )

                            return types.PaidMediaVideo(video=video)

        return None
