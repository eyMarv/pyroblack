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

"""Import location kept for pyroblack <= 2.7.6.

``PaidMedia`` used to live at ``pyrogram.types.messages_and_media.paid_media``
and combined the star amount with the media list. The rebase split it into the
Bot-API shape under ``pyrogram.types.input_paid_media``: ``PaidMedia`` is now the
abstract base of ``PaidMediaPhoto`` / ``PaidMediaVideo`` / ``PaidMediaPreview``,
and the star amount moved to ``PaidMediaInfo``.

Both names are re-exported here so old import paths resolve. ``PaidMediaInfo``
also keeps ``stars_amount`` / ``extended_media`` properties, so code that read
``message.paid_media.stars_amount`` still works even though ``Message.paid_media``
is now a ``PaidMediaInfo``.
"""

from __future__ import annotations

from pyrogram.types.input_paid_media.paid_media import PaidMedia
from pyrogram.types.input_paid_media.paid_media_info import PaidMediaInfo
from pyrogram.types.input_paid_media.paid_media_photo import PaidMediaPhoto
from pyrogram.types.input_paid_media.paid_media_preview import PaidMediaPreview
from pyrogram.types.input_paid_media.paid_media_video import PaidMediaVideo

__all__ = [
    "PaidMedia",
    "PaidMediaInfo",
    "PaidMediaPhoto",
    "PaidMediaPreview",
    "PaidMediaVideo",
]
