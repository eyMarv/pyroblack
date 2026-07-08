from pyrogram import raw

from .story_area_type import StoryAreaType


class StoryAreaTypeUniqueGift(StoryAreaType):
    def __init__(self, name: str = None):
        super().__init__()
        self.name = name

    async def write(self, client, coordinates: "raw.types.MediaAreaCoordinates"):
        return raw.types.MediaAreaStarGift(coordinates=coordinates, slug=self.name)
