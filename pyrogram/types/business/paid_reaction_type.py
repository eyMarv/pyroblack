from ..object import Object
from pyrogram import raw


class PaidReactionType(Object):
    def __init__(self):
        super().__init__()

    async def write(self, client):
        if isinstance(self, PaidReactionTypeChat):
            return self._raw(peer=await client.resolve_peer(self.chat_id))
        return self._raw()

class PaidReactionTypeRegular(PaidReactionType):
    def __init__(self):
        super().__init__()
        self._raw = raw.types.PaidReactionPrivacyDefault

class PaidReactionTypeAnonymous(PaidReactionType):
    def __init__(self):
        super().__init__()
        self._raw = raw.types.PaidReactionPrivacyAnonymous

class PaidReactionTypeChat(PaidReactionType):
    def __init__(self, chat_id: int):
        super().__init__()
        self.chat_id = chat_id
        self._raw = raw.types.PaidReactionPrivacyPeer
