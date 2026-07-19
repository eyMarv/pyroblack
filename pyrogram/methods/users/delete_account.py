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

import pyrogram
from pyrogram import raw
from pyrogram.utils import compute_password_check


class DeleteAccount:
    async def delete_account(
        self: pyrogram.Client,
        reason: str = "",
        password: str | None = None,
    ) -> bool:
        """Deletes the account of the current user, deleting all information associated with the user from the server.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            reason (``str``, *optional*):
                The reason why the account was deleted.

            password (``str``, *optional*):
                The 2-step verification password of the current user. If the current user isn't authorized, then an empty string can be passed and account deletion can be canceled within one week.

        Returns
        -------
            `bool`: True On success.

        Example:
            .. code-block:: python

                await app.delete_account(reason, password)

        """
        r = await self.invoke(
            raw.functions.account.DeleteAccount(
                reason=reason,
                password=compute_password_check(
                    await self.invoke(raw.functions.account.GetPassword()),
                    password,
                )
                if password
                else None,
            ),
        )

        return bool(r)
