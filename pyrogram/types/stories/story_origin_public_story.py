from pyrogram import types

from .story_origin import StoryOrigin


class StoryOriginPublicStory(StoryOrigin):
    def __init__(self, *, chat: "types.Chat" = None, story_id: int = None):
        super().__init__()
        self.chat = chat
        self.story_id = story_id
