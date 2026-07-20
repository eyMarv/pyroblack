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

import logging

import pyrogram
from pyrogram import raw, types

from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputRichMessageContent(InputMessageContent):
    """Content of a rich message to be sent as the result of an inline query.

    Parameters
    ----------
        rich_message (:obj:`pyrogram.types.InputRichMessage`):
            The message to be sent.

    """

    def __init__(
        self,
        rich_message: "types.InputRichMessage",
    ) -> None:
        super().__init__()

        self.rich_message = rich_message

    async def write(self, client: "pyrogram.Client", reply_markup):
        return raw.types.InputBotInlineMessageRichMessage(
            rich_message=self.rich_message.write(),
            reply_markup=await reply_markup.write(client) if reply_markup else None,
        )
