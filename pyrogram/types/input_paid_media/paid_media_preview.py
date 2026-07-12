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

import pyrogram
from pyrogram import types

from ..object import Object
from .paid_media import PaidMedia


class PaidMediaPreview(PaidMedia):
    """The paid media isn't available before the payment.

    Parameters:
        width (``int``, *optional*):
            Media width as defined by the sender.

        height (``int``, *optional*):
            Media height as defined by the sender.

        duration (``int``, *optional*):
            Duration of the media in seconds as defined by the sender.

        minithumbnail (:obj:`~pyrogram.types.StrippedThumbnail`, *optional*):
            Media minithumbnail; may be None.

    """

    def __init__(
        self,
        *,
        width: int = None,
        height: int = None,
        duration: int = None,
        minithumbnail: "types.StrippedThumbnail" = None
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.duration = duration
        self.minithumbnail = minithumbnail
