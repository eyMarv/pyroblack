from .can_post_story_result import CanPostStoryResult


class CanPostStoryResultOk(CanPostStoryResult):
    def __init__(self, story_count: int = None):
        super().__init__()
        self.story_count = story_count
