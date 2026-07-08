from .can_post_story_result import CanPostStoryResult


class CanPostStoryResultActiveStoryLimitExceeded(CanPostStoryResult):
    def __init__(self):
        super().__init__()
