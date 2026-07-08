import io
from typing import Union

from .input_story_content import InputStoryContent


class InputStoryContentPhoto(InputStoryContent):
    def __init__(self, photo: Union[str, "io.BytesIO"], thumbnail: Union[str, "io.BytesIO"] = None):
        super().__init__()
        self.photo = photo
        self.thumbnail = thumbnail
