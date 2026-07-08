from pyrogram import raw

from ..object import Object


class WriteAccessAllowed(Object):
    """Represents a service message about a user allowing a bot to write messages."""

    def __init__(
        self,
        *,
        from_request: bool = None,
        web_app_name: str = None,
        from_attachment_menu: bool = None,
    ):
        super().__init__()

        self.from_request = from_request
        self.web_app_name = web_app_name
        self.from_attachment_menu = from_attachment_menu

    @staticmethod
    def _parse(action: "raw.types.MessageActionBotAllowed"):
        return WriteAccessAllowed(
            from_request=getattr(action, "from_request", None),
            web_app_name=getattr(getattr(action, "app", None), "short_name", None),
            from_attachment_menu=getattr(action, "attach_menu", None),
        )
