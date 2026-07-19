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

from typing import TYPE_CHECKING

from pyrogram.session import Session

if TYPE_CHECKING:
    import pyrogram


class Connect:
    async def connect(
        self: "pyrogram.Client",
    ) -> bool:
        """Connect the client to Telegram servers.

        Returns:
            ``bool``: On success, in case the passed-in session is authorized, True is returned. Otherwise, in case
            the session needs to be authorized, False is returned.

        Raises:
            ConnectionError: In case you try to connect an already connected client.

        """
        if self.is_connected:
            msg = "Client is already connected"
            raise ConnectionError(msg)

        await self.load_session()

        self.session = Session(
            self,
            await self.storage.dc_id(),
            await self.storage.auth_key(),
            await self.storage.test_mode(),
        )

        await self.session.start()

        self.is_connected = True

        return bool(await self.storage.user_id())
