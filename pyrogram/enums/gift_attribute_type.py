from pyrogram import raw

from .auto_name import AutoName


class GiftAttributeType(AutoName):
    """Star gift attribute type enumeration used in :obj:`~pyrogram.types.GiftAttribute`."""

    MODEL = raw.types.StarGiftAttributeModel
    SYMBOL = raw.types.StarGiftAttributePattern
    BACKDROP = raw.types.StarGiftAttributeBackdrop
    ORIGINAL_DETAILS = raw.types.StarGiftAttributeOriginalDetails
