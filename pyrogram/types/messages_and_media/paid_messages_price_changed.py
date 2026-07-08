from ..object import Object


class PaidMessagesPriceChanged(Object):
    """A price for paid messages was changed in the supergroup chat."""

    def __init__(
        self,
        *,
        paid_message_star_count: int
    ):
        super().__init__()

        self.paid_message_star_count = paid_message_star_count

    @staticmethod
    def _parse(action) -> "PaidMessagesPriceChanged":
        return PaidMessagesPriceChanged(
            paid_message_star_count=action.stars
        )
