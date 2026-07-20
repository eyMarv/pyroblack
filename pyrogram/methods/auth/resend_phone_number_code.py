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
import re

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class ResendPhoneNumberCode:
    async def resend_phone_number_code(
        self: "pyrogram.Client",
        phone_number: str,
        phone_code_hash: str,
    ) -> "types.SentCode":
        """Re-send the confirmation code using a different type.

        The type of the code to be re-sent is specified in the *next_type* attribute of the
        :obj:`~pyrogram.types.SentCode` object returned by :meth:`send_phone_number_code`.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Confirmation code identifier.

        Returns
        -------
            :obj:`~pyrogram.types.SentCode`: On success, an object containing information on the re-sent confirmation
            code is returned.

        Raises
        ------
            BadRequest: In case the arguments are invalid.

        """
        phone_number = re.sub(r"\D", "", phone_number)

        r = await self.invoke(
            raw.functions.auth.ResendCode(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
            ),
        )

        return types.SentCode._parse(r)

    resend_code = resend_phone_number_code
