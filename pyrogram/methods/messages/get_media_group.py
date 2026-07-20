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
from pyrogram import types

log = logging.getLogger(__name__)


class GetMediaGroup:
    async def get_media_group(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
    ) -> list[types.Message]:
        """Get the media group a message belongs to.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                The id of one of the messages that belong to the media group.

        Returns
        -------
            List of :obj:`~pyrogram.types.Message`: On success, a list of messages of the media group is returned.

        Raises
        ------
            ValueError:
                In case the passed message_id is negative or equal 0.
                In case target message doesn't belong to a media group.

        """
        if message_id <= 0:
            msg = "Passed message_id is negative or equal to zero."
            raise ValueError(msg)

        # Get messages with id from `id - 9` to `id + 10` to get all possible media group messages.
        messages = await self.get_messages(
            chat_id=chat_id,
            message_ids=list(range(message_id - 9, message_id + 10)),
            replies=0,
        )

        # There can be maximum 10 items in a media group.
        # If/else condition to fix the problem of getting correct `media_group_id` when `message_id` is less than 10.
        media_group_id = (
            messages[9].media_group_id
            if len(messages) == 19
            else messages[message_id - 1].media_group_id
        )
        if media_group_id is None:
            # Get media group id from message with selected message id (https://t.me/kurigram_chat/5/260054)
            media_group_id = next(
                (msg.media_group_id) for msg in messages if msg.id == message_id
            )

        if media_group_id is None:
            msg = "The message doesn't belong to a media group"
            raise ValueError(msg)

        return types.List(
            msg for msg in messages if msg.media_group_id == media_group_id
        )
