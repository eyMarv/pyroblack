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
from pyrogram import raw, types


class GetBotDefaultPrivileges:
    async def get_bot_default_privileges(
        self: pyrogram.Client,
        for_channels: bool | None = None,
    ) -> types.ChatPrivileges | None:
        """Get the current default privileges of the bot.

        .. include:: /_includes/usable-by/bots.rst

        Parameters
        ----------
            for_channels (``bool``, *optional*):
                Pass True to get default privileges of the bot in channels. Otherwise, default privileges of the bot
                for groups and supergroups will be returned.

        Returns
        -------
            ``bool``: On success, True is returned.

        Raises
        ------
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        Example:
            .. code-block:: python

                privileges = await app.get_bot_default_privileges()

        """
        bot_info = await self.invoke(
            raw.functions.users.GetFullUser(
                id=raw.types.InputUserSelf(),
            ),
        )

        field = (
            "bot_broadcast_admin_rights" if for_channels else "bot_group_admin_rights"
        )

        admin_rights = getattr(bot_info.full_user, field)

        return types.ChatPrivileges._parse(admin_rights) if admin_rights else None
