from ..object import Object


class PaidMessagesRefunded(Object):
    """Paid messages were refunded."""

    def __init__(
        self,
        *,
        message_count: int,
        star_count: int
    ):
        super().__init__()

        self.message_count = message_count
        self.star_count = star_count

    @staticmethod
    def _parse(action) -> "PaidMessagesRefunded":
        return PaidMessagesRefunded(
            message_count=action.count,
            star_count=action.stars
        )
