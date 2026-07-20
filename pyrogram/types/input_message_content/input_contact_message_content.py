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

import logging

import pyrogram
from pyrogram import raw

from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputContactMessageContent(InputMessageContent):
    """Content of a contact message to be sent as the result of an inline query.

    Parameters
    ----------
        phone_number (``str``):
            Phone number of the user.

        first_name (``str``):
            First name of the user; 1-64 characters.

        last_name (``str``, *optional*):
            Last name of the user; 0-64 characters.

        vcard (``str``, *optional*):
            Additional data about the user in a form of `vCard <https://en.wikipedia.org/wiki/VCard>`_; 0-2048 bytes in length.

    """

    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: str | None = None,
        vcard: str | None = None,
    ) -> None:
        super().__init__()

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard

    async def write(self, client: pyrogram.Client, reply_markup):
        return raw.types.InputBotInlineMessageMediaContact(
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            vcard=self.vcard,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
        )
