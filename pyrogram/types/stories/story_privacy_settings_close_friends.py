import pyrogram
from pyrogram import raw

from .story_privacy_settings import StoryPrivacySettings


class StoryPrivacySettingsCloseFriends(StoryPrivacySettings):
    def __init__(self):
        super().__init__()

    async def write(self, client: "pyrogram.Client"):
        return [raw.types.InputPrivacyValueAllowCloseFriends()]
