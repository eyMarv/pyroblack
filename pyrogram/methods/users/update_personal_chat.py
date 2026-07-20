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


class UpdatePersonalChat:
    async def update_personal_chat(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> bool:
        """Update your birthday details.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int``):
                Unique identifier (int) of the target channel.
                You can also use channel public link in form of *t.me/<username>* (str).

        Returns
        -------
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your personal chat
                await app.update_personal_chat(chat_id=-1001234567890)

        """
        chat = await self.resolve_peer(chat_id)
        r = await self.invoke(raw.functions.account.UpdatePersonalChannel(channel=chat))
        return bool(r)
