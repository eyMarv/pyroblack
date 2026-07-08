from typing import Optional

from pyrogram import raw, types

from .story_area_type import StoryAreaType


class StoryAreaTypeSuggestedReaction(StoryAreaType):
    def __init__(self, reaction_type: "types.ReactionType" = None, is_dark: Optional[bool] = None, is_flipped: Optional[bool] = None):
        super().__init__()
        self.reaction_type = reaction_type
        self.is_dark = is_dark
        self.is_flipped = is_flipped

    async def write(self, client, coordinates: "raw.types.MediaAreaCoordinates"):
        return raw.types.MediaAreaSuggestedReaction(
            dark=self.is_dark,
            flipped=self.is_flipped,
            coordinates=coordinates,
            reaction=self.reaction_type.write(),
        )
