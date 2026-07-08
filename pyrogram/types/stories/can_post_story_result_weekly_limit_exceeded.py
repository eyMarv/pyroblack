from .can_post_story_result import CanPostStoryResult


class CanPostStoryResultWeeklyLimitExceeded(CanPostStoryResult):
    def __init__(self, retry_after: int):
        super().__init__()
        self.retry_after = retry_after
