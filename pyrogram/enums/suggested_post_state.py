from enum import auto

from .auto_name import AutoName


class SuggestedPostState(AutoName):
    """Suggested post state enumeration used in :obj:`~pyrogram.types.SuggestedPostInfo`."""

    PENDING = auto()
    APPROVED = auto()
    DECLINED = auto()
