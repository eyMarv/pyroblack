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
from pyrogram import enums, raw


class SetMainProfileTab:
    async def set_main_profile_tab(
        self: pyrogram.Client,
        chat_id: int | str,
        main_profile_tab: enums.ProfileTab,
    ) -> bool:
        """Changes the main profile tab of the user or channel.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

            main_profile_tab (:obj:`~pyrogram.enums.ProfileTab`):
                The new value of the main profile tab.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Set user main profile tab to "Posts"
                await app.set_main_profile_tab("me", main_profile_tab=enums.ProfileTab.POSTS)

                # Set channel main profile tab to "Gifts"
                await app.set_main_profile_tab("kurigram_news", main_profile_tab=enums.ProfileTab.GIFTS)

        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerSelf):
            r = await self.invoke(
                raw.functions.account.SetMainProfileTab(
                    tab=main_profile_tab.value(),
                ),
            )
        else:
            r = await self.invoke(
                raw.functions.channels.SetMainProfileTab(
                    channel=peer,
                    tab=main_profile_tab.value(),
                ),
            )

        return r
