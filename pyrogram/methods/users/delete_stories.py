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
from pyrogram import raw

if TYPE_CHECKING:
    from collections.abc import Iterable

log = logging.getLogger(__name__)


class DeleteStories:
    async def delete_stories(
        self: pyrogram.Client,
        story_ids: int | Iterable[int],
        chat_id: int | str | None = None,
    ) -> bool:
        """Delete one or more story by using story identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            story_ids (``int`` | Iterable of ``int``):
                Pass a single story identifier or an iterable of story ids (as integers) to get the content of the
                story themselves.

            chat_id (``int``, *optional*):
                Unique identifier (int) or username (str) of the target channel.
                You can also use channel public link in form of *t.me/<username>* (str).

        Returns
        -------
            `bool`: On success, a True is returned.

        Example:
            .. code-block:: python

                # Delete one story
                await app.delete_stories(12345)

                # Delete more than one story (list of stories)
                await app.delete_stories([12345, 12346])

        """
        is_iterable = not isinstance(story_ids, int)
        ids = list(story_ids) if is_iterable else [story_ids]

        if chat_id:
            peer = await self.resolve_peer(chat_id)
        else:
            peer = await self.resolve_peer("me")

        try:
            await self.invoke(raw.functions.stories.DeleteStories(peer=peer, id=ids))
        except Exception:
            return False
        return True
