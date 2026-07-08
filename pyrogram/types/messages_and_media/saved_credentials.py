from pyrogram import raw

from ..object import Object


class SavedCredentials(Object):
    """Contains information about saved payment credentials."""

    def __init__(
        self,
        *,
        id: str,
        title: str
    ):
        super().__init__()

        self.id = id
        self.title = title

    @staticmethod
    def _parse(credential: "raw.base.PaymentSavedCredentials") -> "SavedCredentials":
        return SavedCredentials(
            id=credential.id,
            title=credential.title,
        )
