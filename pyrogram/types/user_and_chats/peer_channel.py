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

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class PeerChannel(Object):
    """A PeerChannel.

    Parameters
    ----------
        channel_id (``Integer``):
            Id of the channel.

    """

    def __init__(self, *, channel_id: int) -> None:
        super().__init__()

        self.channel_id = channel_id

    @staticmethod
    def _parse(action: "raw.types.PeerChannel") -> "PeerChannel":
        return PeerChannel(channel_id=getattr(action, "channel_id", None))
