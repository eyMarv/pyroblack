import pyrogram
from pyrogram import types

from .paid_media import PaidMedia


class PaidMediaVideo(PaidMedia):
    """The paid media is a video.

    Parameters:
        video (:obj:`~pyrogram.types.Video`):
            The video.
    """

    def __init__(
        self,
        *,
        video: "types.Video" = None
    ):
        super().__init__()

        self.video = video
