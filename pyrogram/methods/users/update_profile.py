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


class UpdateProfile:
    async def update_profile(
        self: pyrogram.Client,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        bio: str | None = None,
    ) -> bool:
        """Update your profile details such as first name, last name and bio.

        You can omit the parameters you don't want to change.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            first_name (``str``, *optional*):
                The new first name; 1-64 characters.

            last_name (``str``, *optional*):
                The new last name; 1-64 characters.
                Pass "" (empty string) to remove it.

            bio (``str``, *optional*):
                Changes the bio of the current user.
                Max ``intro_description_length_limit`` characters without line feeds.
                Pass "" (empty string) to remove it.

        Returns
        -------
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your first name only
                await app.update_profile(first_name="Pyrogram")

                # Update first name and bio
                await app.update_profile(first_name="Pyrogram", bio="https://github.com/TelegramPlayground/pyrogram")

                # Remove the last name
                await app.update_profile(last_name="")

        """
        return bool(
            await self.invoke(
                raw.functions.account.UpdateProfile(
                    first_name=first_name,
                    last_name=last_name,
                    about=bio,
                ),
            ),
        )
