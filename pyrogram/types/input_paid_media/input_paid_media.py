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

from typing import TYPE_CHECKING, Union

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import io


class InputPaidMedia(Object):
    """This object describes the paid media to be sent.

    Currently, it can be one of:

    - :obj:`~pyrogram.types.InputPaidMediaPhoto`
    - :obj:`~pyrogram.types.InputPaidMediaVideo`
    """

    def __init__(
        self,
        media: Union[str, "io.BytesIO"],
    ) -> None:
        super().__init__()

        self.media = media
