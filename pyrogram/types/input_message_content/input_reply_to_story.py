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


class InputReplyToStory(Object):
    """Contains information about a target replied story.

    Parameters
    ----------
        peer (:obj:`~pyrogram.raw.types.InputPeer`):
            An InputPeer.

        story_id (``int``):
            Unique identifier for the target story.

    """

    def __init__(
        self, *, peer: raw.types.InputPeer = None, story_id: int | None = None
    ) -> None:
        super().__init__()

        self.peer = peer
        self.story_id = story_id

    def write(self):
        return raw.types.InputReplyToStory(
            peer=self.peer,
            story_id=self.story_id,
        ).write()
