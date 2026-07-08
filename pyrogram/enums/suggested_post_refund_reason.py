from enum import auto

from .auto_name import AutoName


class SuggestedPostRefundReason(AutoName):
    """Suggested post refund reason enumeration used in :obj:`~pyrogram.types.SuggestedPostRefunded`."""

    POST_DELETED = auto()
    PAYMENT_REFUNDED = auto()
