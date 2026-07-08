import io
from typing import Optional, Union

from .input_paid_media import InputPaidMedia


class InputPaidMediaVideo(InputPaidMedia):
    """The paid media to send is a video.

    It is intended to be used with :obj:`~pyrogram.Client.send_paid_media`.

    Parameters:
        media (``str`` | :obj:`io.BytesIO`):
            File to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine or
            pass a binary file-like object with its attribute ".name" set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a video from the Internet.

        thumbnail (``str`` | :obj:`io.BytesIO`, *optional*):
            Thumbnail of the video sent.

        width (``int``, *optional*):
            Video width.

        height (``int``, *optional*):
            Video height.

        duration (``int``, *optional*):
            Video duration.

        supports_streaming (``bool``, *optional*):
            Pass True, if the uploaded video is suitable for streaming.

        cover (``str`` | :obj:`io.BytesIO`, *optional*):
            Cover for the video in the message.

        start_timestamp (``int``, *optional*):
            Timestamp from which the video playing must start, in seconds.
    """

    def __init__(
        self,
        media: Union[str, "io.BytesIO"],
        thumbnail: Union[str, "io.BytesIO"] = None,
        width: int = 0,
        height: int = 0,
        duration: int = 0,
        supports_streaming: bool = True,
        cover: Optional[Union[str, "io.BytesIO"]] = None,
        start_timestamp: int = None
    ):
        super().__init__(media)

        self.thumbnail = thumbnail
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming
        self.cover = cover
        self.start_timestamp = start_timestamp
