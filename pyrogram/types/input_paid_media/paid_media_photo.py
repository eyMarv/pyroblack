import pyrogram
from pyrogram import types

from .paid_media import PaidMedia


class PaidMediaPhoto(PaidMedia):
    """The paid media is a photo.

    Parameters:
        photo (:obj:`~pyrogram.types.Photo`):
            The photo.
    """

    def __init__(
        self,
        *,
        photo: "types.Photo" = None
    ):
        super().__init__()

        self.photo = photo
