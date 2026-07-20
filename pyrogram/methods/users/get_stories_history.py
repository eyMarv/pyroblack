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
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

log = logging.getLogger(__name__)


class GetUserStoriesHistory:
    async def get_stories_history(
        self: pyrogram.Client,
        chat_id: int | None = None,
        limit: int = 0,
        offset_id: int = 0,
    ) -> AsyncGenerator[types.Story, None] | None:
        """Get stories history.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int``, *optional*):
                Unique identifier (int) of the target channel.
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

            limit (``int``, *optional*):
                Limits the number of stories to be retrieved.
                By default, no limit is applied and all stories are returned.

            offset_id (``int``, *optional*):
                Identifier of the first story to be returned.

        Returns
        -------
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.Story` objects is returned.

        Example:
            .. code-block:: python

                # Get story history
                async for story in app.get_stories_history():
                    print(story)

        Raises
        ------
            ValueError: In case of invalid arguments.

        """
        if chat_id:
            peer = await self.resolve_peer(chat_id)
        else:
            peer = await self.resolve_peer("me")

        rpc = raw.functions.stories.GetStoriesArchive(
            peer=peer,
            offset_id=offset_id,
            limit=limit,
        )

        r = await self.invoke(rpc, sleep_threshold=-1)

        for story in r.stories:
            yield await types.Story._parse(self, story, peer)
