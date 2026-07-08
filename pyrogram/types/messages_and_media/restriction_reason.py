from typing import Optional

from pyrogram import raw

from ..object import Object


class RestrictionReason(Object):
    """Restriction reason."""

    def __init__(
        self,
        *,
        platform: str,
        reason: str,
        text: str
    ):
        super().__init__()

        self.platform = platform
        self.reason = reason
        self.text = text

    @staticmethod
    def _parse(restriction_reason: "raw.types.RestrictionReason") -> Optional["RestrictionReason"]:
        if not restriction_reason:
            return None

        return RestrictionReason(
            platform=restriction_reason.platform,
            reason=restriction_reason.reason,
            text=restriction_reason.text,
        )
