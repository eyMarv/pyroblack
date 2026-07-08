from .story_origin import StoryOrigin


class StoryOriginHiddenUser(StoryOrigin):
    def __init__(self, *, poster_name: str = None):
        super().__init__()
        self.poster_name = poster_name
