import pyrogram
from pyrogram import types

from .paid_media import PaidMedia


class PaidMediaPreview(PaidMedia):
    """The paid media isn't available before the payment.

    Parameters:
        width (``int``, *optional*):
            Media width as defined by the sender.

        height (``int``, *optional*):
            Media height as defined by the sender.

        duration (``int``, *optional*):
            Duration of the media in seconds as defined by the sender.

        minithumbnail (:obj:`~pyrogram.types.StrippedThumbnail`, *optional*):
            Media minithumbnail; may be None.
    """

    def __init__(
        self,
        *,
        width: int = None,
        height: int = None,
        duration: int = None,
        minithumbnail: "types.StrippedThumbnail" = None
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.duration = duration
        self.minithumbnail = minithumbnail
