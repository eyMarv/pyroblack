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
from pyrogram import errors, raw, types


class CanPostStory:
    async def can_post_story(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> types.CanPostStoryResult:
        """Checks whether the current user can post a story on behalf of a chat.

        .. include:: /_includes/usable-by/users.rst

        Requires can_post_stories right for supergroup and channel chats.

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns
        -------
            :obj:`~pyrogram.types.CanPostStoryResult`: On success.

        Example:
            .. code-block:: python

                # Check if you can send story to chat id
                await app.can_post_story(chat_id)

        """
        try:
            r = await self.invoke(
                raw.functions.stories.CanSendStory(
                    peer=await self.resolve_peer(chat_id),
                ),
            )
        except errors.PremiumAccountRequired:
            return types.CanPostStoryResultPremiumNeeded()
        except errors.BoostsRequired:
            return types.CanPostStoryResultBoostNeeded()
        except errors.StoriesTooMuch:
            return types.CanPostStoryResultActiveStoryLimitExceeded()
        except errors.StorySendFloodWeekly as ex:
            return types.CanPostStoryResultWeeklyLimitExceeded(
                retry_after=ex.value,
            )
        except errors.StorySendFloodMonthly as ex:
            return types.CanPostStoryResultMonthlyLimitExceeded(
                retry_after=ex.value,
            )
        except errors.StoryLiveAlready as ex:
            return types.CanPostStoryResultLiveStoryIsActive(
                story_id=ex.value,
            )
        return types.CanPostStoryResultOk(story_count=r.count_remains)
