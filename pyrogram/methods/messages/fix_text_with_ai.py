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

from typing import Union

import pyrogram
from pyrogram import raw, types


class FixTextWithAI:
    async def fix_text_with_ai(
        self: "pyrogram.Client",
        text: Union[str, "types.FormattedText"],
    ) -> "types.FormattedText":
        """Fixes text using an AI model.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            text (``str`` | :obj:`~pyrogram.types.FormattedText`):
                The original text.

        Returns
        -------
            :obj:`~pyrogram.types.FormattedText`: On success, information about the fixed text is returned.

        Example:
            .. code-block:: python

                app.fix_text_with_ai(
                    "This statement maay havve feew mistakes"
                )

        """
        if isinstance(text, str):
            text = types.FormattedText(text=text)

        r = await self.invoke(
            raw.functions.messages.ComposeMessageWithAI(
                text=await text.write(self),
                proofread=True,
            ),
        )

        return types.FormattedText._parse(self, r.result_text)
