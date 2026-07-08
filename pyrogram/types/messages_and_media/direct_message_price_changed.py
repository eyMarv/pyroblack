from ..object import Object


class DirectMessagePriceChanged(Object):
    """A price for direct messages was changed in the channel chat."""

    def __init__(
        self,
        *,
        is_enabled: bool,
        paid_message_star_count: int
    ):
        super().__init__()

        self.is_enabled = is_enabled
        self.paid_message_star_count = paid_message_star_count

    @staticmethod
    def _parse(action) -> "DirectMessagePriceChanged":
        return DirectMessagePriceChanged(
            is_enabled=action.broadcast_messages_allowed,
            paid_message_star_count=action.stars
        )
