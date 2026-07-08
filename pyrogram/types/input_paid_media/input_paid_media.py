import io
from typing import Union

from ..object import Object


class InputPaidMedia(Object):
    """This object describes the paid media to be sent.

    Currently, it can be one of:

    - :obj:`~pyrogram.types.InputPaidMediaPhoto`
    - :obj:`~pyrogram.types.InputPaidMediaVideo`
    """

    def __init__(
        self,
        media: Union[str, "io.BytesIO"]
    ):
        super().__init__()

        self.media = media
