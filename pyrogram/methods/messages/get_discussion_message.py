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


class GetDiscussionMessage:
    async def get_discussion_message(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
    ) -> types.Message:
        """Get the first discussion message of a channel post or a discussion thread in a group.

        Reply to the returned message to leave a comment on the linked channel post or to continue
        the discussion thread.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Message id.

        Example:
            .. code-block:: python

                # Get the discussion message
                m = await app.get_discussion_message(channel_id, message_id)

                # Comment to the post by replying
                await m.reply("comment")

        """
        r = await self.invoke(
            raw.functions.messages.GetDiscussionMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
            ),
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        return await types.Message._parse(
            self,
            r.messages[0],
            users,
            chats,
            replies=self.fetch_replies,
        )
