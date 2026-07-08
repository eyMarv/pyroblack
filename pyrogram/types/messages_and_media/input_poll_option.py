#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types

from ..object import Object


class InputPollOption(Object):
    """This object contains information about one answer option in a poll to be sent.

    Parameters:
        text (``str`` | :obj:`~pyrogram.types.FormattedText`):
            Option text, 1-100 characters.
    """

    def __init__(
        self,
        *,
        text: Union[str, "types.FormattedText"],
    ):
        super().__init__()

        self.text = text

    async def write(self, client: "pyrogram.Client") -> "raw.types.InputPollAnswer":
        if isinstance(self.text, str):
            self.text = types.FormattedText(text=self.text)

        return raw.types.InputPollAnswer(
            text=await self.text.write(client),
        )
