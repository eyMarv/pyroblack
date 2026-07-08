#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from typing import AsyncGenerator

import pyrogram
from pyrogram import raw, types, utils


class SearchPublicMessagesByTag:
    async def search_public_messages_by_tag(
        self: "pyrogram.Client",
        tag: str = "",
        offset_id: int = 0,
        offset_date: datetime = utils.zero_datetime(),
        limit: int = 0,
    ) -> AsyncGenerator["types.Message", None]:
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        offset_peer = raw.types.InputPeerEmpty()

        while True:
            messages = await utils.parse_messages(
                self,
                await self.invoke(
                    raw.functions.channels.SearchPosts(
                        hashtag=tag,
                        offset_rate=utils.datetime_to_timestamp(offset_date),
                        offset_peer=offset_peer,
                        offset_id=offset_id,
                        limit=limit,
                    ),
                    sleep_threshold=60,
                ),
                replies=0,
            )

            if not messages:
                return

            last = messages[-1]
            offset_date = utils.datetime_to_timestamp(last.date)
            offset_peer = await self.resolve_peer(last.chat.id)
            offset_id = last.id

            for message in messages:
                yield message
                current += 1
                if current >= total:
                    return
