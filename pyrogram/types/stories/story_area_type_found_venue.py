from pyrogram import raw

from .story_area_type import StoryAreaType


class StoryAreaTypeFoundVenue(StoryAreaType):
    def __init__(self, query_id: int = None, result_id: str = None):
        super().__init__()
        self.query_id = query_id
        self.result_id = result_id

    async def write(self, client, coordinates: "raw.types.MediaAreaCoordinates"):
        return raw.types.InputMediaAreaVenue(
            coordinates=coordinates,
            query_id=self.query_id,
            result_id=self.result_id,
        )
