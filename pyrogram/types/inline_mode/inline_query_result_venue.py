#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2024 Dan <https://github.com/delivrance>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  This file is part of Pyroblack.
#
#  Pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  Pyroblack is a continuation fork of Pyrogram <https://github.com/pyrogram/pyrogram>
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw, types

from .inline_query_result import InlineQueryResult

log = logging.getLogger(__name__)


class InlineQueryResultVenue(InlineQueryResult):
    """A venue.

    By default, the venue will be sent by the user. Alternatively, you can use *input_message_content* to send a message
    with the specified content instead of the venue.

    Parameters
    ----------
        title (``str``):
            Title for the result.

        address (``str``):
            Address of the venue.

        latitude (``float``):
            Location latitude in degrees.

        longitude (``float``):
            Location longitude in degrees.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        foursquare_id (``str``, *optional*):
            Foursquare identifier of the venue if known.

        foursquare_type (``str``, *optional*):
            Foursquare type of the venue, if known. (For example, “arts_entertainment/default”, “arts_entertainment/aquarium” or “food/icecream”.)

        google_place_id (``str``, *optional*):
            Google Places identifier of the venue.

        google_place_type (``str``, *optional*):
            Google Places type of the venue. (See `supported types <https://developers.google.com/places/web-service/supported_types>`_.)

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent instead of the file.

        thumbnail_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumbnail_width (``int``, *optional*):
            Thumbnail width.

        thumbnail_height (``int``, *optional*):
            Thumbnail height.

    """

    def __init__(
        self,
        title: str,
        address: str,
        latitude: float,
        longitude: float,
        id: str | None = None,
        foursquare_id: str | None = None,
        foursquare_type: str | None = None,
        google_place_id: str | None = None,
        google_place_type: str | None = None,
        reply_markup: types.InlineKeyboardMarkup = None,
        input_message_content: types.InputMessageContent = None,
        thumbnail_url: str | None = None,
        thumbnail_width: int = 0,
        thumbnail_height: int = 0,
        thumb_url: str | None = None,
        thumb_width: int | None = None,
        thumb_height: int | None = None,
    ) -> None:
        if thumb_url and thumbnail_url:
            msg = "Parameters `thumb_url` and `thumbnail_url` are mutually exclusive."
            raise ValueError(
                msg,
            )

        if thumb_url is not None:
            log.warning(
                "This property is deprecated. Please use thumbnail_url instead",
            )
            thumbnail_url = thumb_url

        if thumb_width and thumbnail_width:
            msg = (
                "Parameters `thumb_width` and `thumbnail_width` are mutually exclusive."
            )
            raise ValueError(
                msg,
            )

        if thumb_width is not None:
            log.warning(
                "This property is deprecated. Please use thumbnail_width instead",
            )
            thumbnail_width = thumb_width

        if thumb_height and thumbnail_height:
            msg = (
                "Parameters `thumb_height` and `thumbnail_height` are mutually "
                "exclusive."
            )
            raise ValueError(
                msg,
            )

        if thumb_height is not None:
            log.warning(
                "This property is deprecated. Please use thumbnail_height instead",
            )
            thumbnail_height = thumb_height

        super().__init__("venue", id, input_message_content, reply_markup)

        self.title = title
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type
        self.google_place_id = google_place_id
        self.google_place_type = google_place_type
        self.thumbnail_url = thumbnail_url
        self.thumb_url = thumbnail_url  # <=2.7.2
        self.thumbnail_width = thumbnail_width
        self.thumb_width = thumbnail_width  # <=2.7.2
        self.thumbnail_height = thumbnail_height
        self.thumb_height = thumbnail_height  # <=2.7.2

    async def write(self, client: pyrogram.Client):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaVenue(
                    geo_point=raw.types.InputGeoPoint(
                        lat=self.latitude,
                        long=self.longitude,
                    ),
                    title=self.title,
                    address=self.address,
                    provider=(
                        "foursquare"
                        if self.foursquare_id or self.foursquare_type
                        else "google"
                        if self.google_place_id or self.google_place_type
                        else ""
                    ),
                    venue_id=self.foursquare_id or self.google_place_id or "",
                    venue_type=self.foursquare_type or self.google_place_type or "",
                    reply_markup=await self.reply_markup.write(client)
                    if self.reply_markup
                    else None,
                )
            ),
            thumb=raw.types.InputWebDocument(
                url=self.thumbnail_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[
                    raw.types.DocumentAttributeImageSize(
                        w=self.thumbnail_width,
                        h=self.thumbnail_height,
                    ),
                ],
            )
            if self.thumbnail_url
            else None,
        )
