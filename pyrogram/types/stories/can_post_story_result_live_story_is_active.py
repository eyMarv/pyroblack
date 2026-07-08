from .can_post_story_result import CanPostStoryResult


class CanPostStoryResultLiveStoryIsActive(CanPostStoryResult):
    def __init__(self, story_id: int):
        super().__init__()
        self.story_id = story_id
