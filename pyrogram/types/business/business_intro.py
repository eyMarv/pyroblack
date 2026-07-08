from pyrogram import raw, types
from ..object import Object


class BusinessIntro(Object):
    def __init__(self, *, title: str = None, message: str = None, sticker: "types.Sticker" = None):
        super().__init__()
        self.title = title
        self.message = message
        self.sticker = sticker

    @staticmethod
    async def _parse(client, business_intro: "raw.types.BusinessIntro") -> "BusinessIntro":
        doc = getattr(business_intro, "sticker", None)
        sticker = None
        if doc and isinstance(doc, raw.types.Document):
            attributes = {type(i): i for i in doc.attributes}
            sticker = await types.Sticker._parse(client, doc, attributes)
        return BusinessIntro(
            title=getattr(business_intro, "title", None),
            message=getattr(business_intro, "description", None),
            sticker=sticker,
        )
