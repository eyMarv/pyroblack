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


class AnswerCallbackQuery:
    async def answer_callback_query(
        self: pyrogram.Client,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int = 0,
    ):
        """Send answers to callback queries sent from inline keyboards.
        The answer will be displayed to the user as a notification at the top of the chat screen or as an alert.

        .. include:: /_includes/usable-by/bots.rst

        Parameters
        ----------
            callback_query_id (``str``):
                Unique identifier for the query to be answered.

            text (``str`` *optional*):
                Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.

            show_alert (``bool``, *optional*):
                If true, an alert will be shown by the client instead of a notification at the top of the chat screen.
                Defaults to False.

            url (``str``, *optional*):
                URL that will be opened by the user's client.
                If you have created a Game and accepted the conditions via @Botfather, specify the URL that opens your
                game - note that this will only work if the query comes from a callback_game button.
                Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.

            cache_time (``int``, *optional*):
                The maximum amount of time in seconds that the result of the callback query may be cached client-side.
                Telegram apps will support caching starting in version 3.14. Defaults to 0.

        Returns
        -------
            ``bool``: True, on success.

        Raises
        ------
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        Example:
            .. code-block:: python

                # Answer only (remove the spinning circles)
                await app.answer_callback_query(query_id)

                # Answer without alert
                await app.answer_callback_query(query_id, text=text)

                # Answer with alert
                await app.answer_callback_query(query_id, text=text, show_alert=True)

        """
        return await self.invoke(
            raw.functions.messages.SetBotCallbackAnswer(
                query_id=int(callback_query_id),
                cache_time=cache_time,
                alert=show_alert or None,
                message=text or None,
                url=url or None,
            ),
        )
