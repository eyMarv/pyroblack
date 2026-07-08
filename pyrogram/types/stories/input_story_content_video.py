import io
from typing import Union

from .input_story_content import InputStoryContent


class InputStoryContentVideo(InputStoryContent):
    def __init__(
        self,
        video: Union[str, "io.BytesIO"],
        duration: int = 0,
        cover_frame_timestamp: int = 0,
        is_animation: bool = None,
        width: int = 0,
        height: int = 0,
        thumbnail: Union[str, "io.BytesIO"] = None,
        supports_streaming: bool = True,
        file_name: str = None,
    ):
        super().__init__()
        self.video = video
        self.duration = duration
        self.cover_frame_timestamp = cover_frame_timestamp
        self.is_animation = is_animation
        self.width = width
        self.height = height
        self.thumbnail = thumbnail
        self.supports_streaming = supports_streaming
        self.file_name = file_name
