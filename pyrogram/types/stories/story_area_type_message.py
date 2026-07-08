from typing import Union

import pyrogram
from pyrogram import raw

from .story_area_type import StoryAreaType


class StoryAreaTypeMessage(StoryAreaType):
    def __init__(self, chat_id: Union[int, str] = None, message_id: int = None):
        super().__init__()
        self.chat_id = chat_id
        self.message_id = message_id

    async def write(self, client: "pyrogram.Client", coordinates: "raw.types.MediaAreaCoordinates"):
        return raw.types.InputMediaAreaChannelPost(
            coordinates=coordinates,
            channel=await client.resolve_peer(self.chat_id),
            msg_id=self.message_id,
        )
