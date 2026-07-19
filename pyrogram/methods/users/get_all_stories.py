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


class GetAllStories:
    async def get_all_stories(
        self: pyrogram.Client,
    ) -> AsyncGenerator[types.Story, None] | None:
        """Get all active stories.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.Story` objects is returned.

        Example:
            .. code-block:: python

                # Get all active story
                async for story in app.get_all_stories():
                    print(story)

        Raises:
            ValueError: In case of invalid arguments.

        """
        rpc = raw.functions.stories.GetAllStories()

        r = await self.invoke(rpc, sleep_threshold=-1)

        for peer_story in r.peer_stories:
            for story in peer_story.stories:
                yield await types.Story._parse(self, story, peer_story.peer)
