import pyrogram
from pyrogram import raw

from .story_area_type import StoryAreaType


class StoryAreaTypeLink(StoryAreaType):
    def __init__(self, url: str = None):
        super().__init__()
        self.url = url

    async def write(self, client: "pyrogram.Client", coordinates: "raw.types.MediaAreaCoordinates"):
        return raw.types.MediaAreaUrl(coordinates=coordinates, url=self.url)
