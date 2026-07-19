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


class ViewStories:
    async def view_stories(
        self: pyrogram.Client,
        chat_id: int | str,
        story_id: int | list[int],
    ) -> bool:
        """Increment story views.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            story_id (``int`` | List of ``int``):
                Identifier or list of story identifiers of the target story.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Increment story views
                await app.view_stories(chat_id, 1)

        """
        ids = [story_id] if not isinstance(story_id, list) else story_id

        return await self.invoke(
            raw.functions.stories.IncrementStoryViews(
                peer=await self.resolve_peer(chat_id),
                id=ids,
            ),
        )
