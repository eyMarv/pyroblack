from ..object import Object


class ChatHasProtectedContentDisableRequested(Object):
    """Chat `has_protected_content` setting was requested to be disabled."""

    def __init__(self, *, is_expired: bool):
        super().__init__()

        self.is_expired = is_expired

    @staticmethod
    def _parse(action) -> "ChatHasProtectedContentDisableRequested":
        return ChatHasProtectedContentDisableRequested(
            is_expired=bool(action.expired)
        )
