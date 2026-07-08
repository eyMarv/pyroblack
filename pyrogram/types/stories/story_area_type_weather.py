import pyrogram
from pyrogram import raw

from .story_area_type import StoryAreaType


class StoryAreaTypeWeather(StoryAreaType):
    def __init__(self, temperature: float = None, emoji: str = None, background_color: int = None):
        super().__init__()
        self.temperature = temperature
        self.emoji = emoji
        self.background_color = background_color

    async def write(self, client: "pyrogram.Client", coordinates: "raw.types.MediaAreaCoordinates"):
        return raw.types.MediaAreaWeather(
            coordinates=coordinates,
            emoji=self.emoji,
            temperature_c=self.temperature,
            color=self.background_color,
        )
