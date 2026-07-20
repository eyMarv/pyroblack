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

import pyrogram
from pyrogram import raw, types

from .story_area_type import StoryAreaType


class StoryAreaTypeSuggestedReaction(StoryAreaType):
    """This object describes a story area pointing to a suggested reaction. Currently, a story can have up to 5 suggested reaction areas.

    Parameters
    ----------
        reaction_type (:obj:`~pyrogram.types.ReactionType`):
            Type of the reaction.

        is_dark (``bool``, *optional*):
            Pass True if the reaction area has a dark background.

        is_flipped (``bool``, *optional*):
            Pass True if reaction area corner is flipped.

    """

    def __init__(
        self,
        reaction_type: types.ReactionType = None,
        is_dark: bool | None = None,
        is_flipped: bool | None = None,
    ) -> None:
        super().__init__()

        self.reaction_type = reaction_type
        self.is_dark = is_dark
        self.is_flipped = is_flipped

    async def write(
        self,
        client: pyrogram.Client,
        coordinates: raw.types.MediaAreaCoordinates,
    ):
        return raw.types.MediaAreaSuggestedReaction(
            dark=self.is_dark,
            flipped=self.is_flipped,
            coordinates=coordinates,
            reaction=self.reaction_type.write(client),
        )
