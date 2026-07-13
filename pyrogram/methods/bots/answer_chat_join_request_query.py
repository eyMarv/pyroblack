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

import pyrogram
from pyrogram import enums, raw


class AnswerChatJoinRequestQuery:
    async def answer_chat_join_request_query(
        self: "pyrogram.Client",
        chat_join_request_query_id: str,
        result: "enums.ChatJoinRequestQueryResult",
    ) -> bool:
        """Use this method to process a received chat join request query.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_join_request_query_id (``str``):
                Unique identifier of the join request query.

            result (:obj:`~pyrogram.enums.ChatJoinRequestQueryResult`):
                Result of the query.

        Returns:
            ``bool``: On success True is returned.
        """
        return await self.invoke(
            raw.functions.bots.SetJoinChatResults(
                query_id=int(chat_join_request_query_id), result=result.value()
            )
        )
