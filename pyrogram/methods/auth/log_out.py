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
from pyrogram import raw

log = logging.getLogger(__name__)


class LogOut:
    async def log_out(
        self: "pyrogram.Client",
    ) -> bool:
        r"""Log out from Telegram and delete the *\\*.session* file.

        When you log out, the current client is stopped and the storage session deleted.
        No more API calls can be made until you start the client and re-authorize again.

        .. include:: /_includes/usable-by/users-bots.rst

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        Example:
            .. code-block:: python

                # Log out.
                app.log_out()

        """
        await self.invoke(raw.functions.auth.LogOut())
        await self.stop()
        await self.storage.delete()

        return True
