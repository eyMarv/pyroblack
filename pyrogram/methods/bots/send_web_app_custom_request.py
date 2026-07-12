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

from typing import Union

import pyrogram
from pyrogram import raw, types


class SendWebAppCustomRequest:
    async def send_web_app_custom_request(
        self: "pyrogram.Client",
        bot_user_id: Union[int, str],
        method: str,
        parameters: str
    ) -> str:
        """Sends a custom request from a Web App.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            bot_user_id (``int`` | ``str``):
                Unique identifier of the inline bot you want to get results from. You can specify
                a @username (str) or a bot ID (int).

            method (``str``):
                The method name.
            
            parameters (``str``):
                JSON-serialized method parameters.

        Returns:
            ``str``: On success, a JSON-serialized result is returned.

        Raises:
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        """

        r = await self.invoke(
            raw.functions.bots.InvokeWebViewCustomMethod(
                bot=await self.resolve_peer(bot_user_id),
                custom_method=method,
                params=raw.types.DataJSON(
                    data=parameters
                )
            )
        )

        return r.data
