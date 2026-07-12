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

from typing import Optional

import pyrogram
from pyrogram import types, raw

from .story_area_type import StoryAreaType


class StoryAreaTypeFoundVenue(StoryAreaType):
    """This object describes an area pointing to a venue found by the FOURSQUARE bot. Currently, a story can have up to 10 venue areas.

    Parameters:
        query_id (``int``):
            Identifier of the inline query, used to find the venue.

        result_id (``str``):
            Identifier of the inline query result.

    """

    def __init__(
        self,
        query_id: int = None,
        result_id: str = None,
    ):
        super().__init__()

        self.query_id = query_id
        self.result_id = result_id

    async def write(
        self,
        client: "pyrogram.Client",
        coordinates: "raw.types.MediaAreaCoordinates"
    ):
        return raw.types.InputMediaAreaVenue(
            coordinates=coordinates,
            query_id=self.query_id,
            result_id=self.result_id,
        )
