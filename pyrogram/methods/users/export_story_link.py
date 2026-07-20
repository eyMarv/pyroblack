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

import logging

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class ExportStoryLink:
    async def export_story_link(
        self: pyrogram.Client,
        chat_id: int | str,
        story_id: int,
    ) -> types.ExportedStoryLink:
        """Get one story link from an user by using story identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user/channel.
                For your personal story you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

            story_id (``int``):
                Pass a single story identifier of story (as integers).

        Returns
        -------
            :obj:`~pyrogram.types.ExportedStoryLink`: a single story link is returned.

        Example:
            .. code-block:: python

                # Get story link
                await app.export_story_link(chat_id, 12345)

        Raises
        ------
            ValueError: In case of invalid arguments.

        """
        peer = await self.resolve_peer(chat_id)

        rpc = raw.functions.stories.ExportStoryLink(peer=peer, id=story_id)

        r = await self.invoke(rpc, sleep_threshold=-1)

        return types.ExportedStoryLink._parse(r)
