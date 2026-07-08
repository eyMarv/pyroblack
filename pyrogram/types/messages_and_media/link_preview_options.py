from typing import Optional

from pyrogram import raw

from ..object import Object


class LinkPreviewOptions(Object):
    """Describes the options used for link preview generation."""

    def __init__(
        self,
        *,
        is_disabled: bool = None,
        url: str = None,
        prefer_small_media: bool = None,
        prefer_large_media: bool = None,
        show_above_text: bool = None
    ):
        super().__init__()

        self.is_disabled = is_disabled
        self.url = url
        self.prefer_small_media = prefer_small_media
        self.prefer_large_media = prefer_large_media
        self.show_above_text = show_above_text

    @staticmethod
    def _parse(
        client,
        media: "raw.types.MessageMediaWebPage",
        url: str = None,
        invert_media: bool = None
    ) -> Optional["LinkPreviewOptions"]:
        if isinstance(media, raw.types.MessageMediaWebPage) and not isinstance(media.webpage, raw.types.WebPageNotModified):
            return LinkPreviewOptions(
                is_disabled=False,
                url=media.webpage.url,
                prefer_small_media=media.force_small_media,
                prefer_large_media=media.force_large_media,
                show_above_text=invert_media,
            )

        if url:
            return LinkPreviewOptions(
                is_disabled=True,
                url=url,
                show_above_text=invert_media,
            )

        return None
