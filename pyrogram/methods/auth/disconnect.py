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

if TYPE_CHECKING:
    import pyrogram


class Disconnect:
    async def disconnect(
        self: "pyrogram.Client",
    ) -> None:
        """Disconnect the client from Telegram servers.

        Raises:
            ConnectionError: In case you try to disconnect an already disconnected client or in case you try to disconnect a client that needs to be terminated first.

        """
        if not self.is_connected:
            msg = "Client is already disconnected"
            raise ConnectionError(msg)

        if self.is_initialized:
            msg = "Can't disconnect an initialized client"
            raise ConnectionError(msg)

        await self.session.stop()
        await self.storage.close()
        self.is_connected = False
