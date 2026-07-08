import io
from typing import Union

from .input_paid_media import InputPaidMedia


class InputPaidMediaPhoto(InputPaidMedia):
    """The paid media to send is a photo.

    It is intended to be used with :obj:`~pyrogram.Client.send_paid_media`.

    Parameters:
        media (``str`` | :obj:`io.BytesIO`):
            Photo to send.
            Pass a file_id as string to send a photo that exists on the Telegram servers or
            pass a file path as string to upload a new photo that exists on your local machine or
            pass a binary file-like object with its attribute ".name" set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a photo from the Internet.
    """

    def __init__(
        self,
        media: Union[str, "io.BytesIO"]
    ):
        super().__init__(media)
