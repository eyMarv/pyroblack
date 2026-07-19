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

from pyrogram import raw
from pyrogram.types.object import Object


class StoryAreaPosition(Object):
    """This object describes the position of a clickable area within a story.

    Parameters
    ----------
        x_percentage (``float``):
            The abscissa of the area's center, as a percentage of the media width.

        y_percentage (``float``):
            The ordinate of the area's center, as a percentage of the media height.

        width_percentage (``float``):
            The width of the area's rectangle, as a percentage of the media width.

        height_percentage (``float``):
            The height of the area's rectangle, as a percentage of the media height.

        rotation_angle (``float``):
            The clockwise rotation angle of the rectangle, in degrees; 0-360.

        corner_radius_percentage (``float``, *optional*):
            The radius of the rectangle corner rounding, as a percentage of the media width.

    """

    def __init__(
        self,
        x_percentage: float | None = None,
        y_percentage: float | None = None,
        width_percentage: float | None = None,
        height_percentage: float | None = None,
        rotation_angle: float | None = None,
        corner_radius_percentage: float | None = None,
    ) -> None:
        super().__init__()

        self.x_percentage = x_percentage
        self.y_percentage = y_percentage
        self.width_percentage = width_percentage
        self.height_percentage = height_percentage
        self.rotation_angle = rotation_angle
        self.corner_radius_percentage = corner_radius_percentage

    @staticmethod
    def _parse(coordinates: raw.types.MediaAreaCoordinates) -> StoryAreaPosition:
        return StoryAreaPosition(
            x_percentage=coordinates.x,
            y_percentage=coordinates.y,
            width_percentage=coordinates.w,
            height_percentage=coordinates.h,
            rotation_angle=coordinates.rotation,
            corner_radius_percentage=coordinates.radius,
        )

    def write(self):
        return raw.types.MediaAreaCoordinates(
            x=self.x_percentage,
            y=self.y_percentage,
            w=self.width_percentage,
            h=self.height_percentage,
            rotation=self.rotation_angle,
            radius=self.corner_radius_percentage,
        )
