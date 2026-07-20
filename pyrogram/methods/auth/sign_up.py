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

log = logging.getLogger(__name__)


class SignUp:
    async def sign_up(
        self: "pyrogram.Client",
        phone_number: str,
        phone_code_hash: str,
        first_name: str,
        last_name: str = "",
    ) -> "types.User":
        """Register a new user in Telegram.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Code identifier taken from the result of :meth:`~pyrogram.Client.send_code`.

            first_name (``str``):
                New user first name.

            last_name (``str``, *optional*):
                New user last name. Defaults to "" (empty string, no last name).

        Returns
        -------
            :obj:`~pyrogram.types.User`: On success, the new registered user is returned.

        Raises
        ------
            BadRequest: In case the arguments are invalid.
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        """
        phone_number = phone_number.strip(" +")

        r = await self.invoke(
            raw.functions.auth.SignUp(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                phone_code_hash=phone_code_hash,
                no_joined_notifications=self.no_joined_notifications,
            ),
        )

        await self.storage.user_id(r.user.id)
        await self.storage.is_bot(False)

        return types.User._parse(self, r.user)
