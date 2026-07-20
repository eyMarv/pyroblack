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
from pyrogram.types import Identifier


class StopListening:
    async def stop_listening(
        self: pyrogram.Client,
        listener_type: pyrogram.enums.ListenerTypes = pyrogram.enums.ListenerTypes.MESSAGE,
        chat_id: int | str | list[int | str] | None = None,
        user_id: int | str | list[int | str] | None = None,
        message_id: int | list[int] | None = None,
        inline_message_id: str | list[str] | None = None,
    ) -> None:
        """Stops all listeners that match the given identifier pattern.

        .. include:: /_includes/usable-by/users-bots.rst

        Uses :meth:`~pyrogram.Client.get_many_listeners_matching_with_identifier_pattern`.

        Parameters
        ----------
            listener_type (:obj:`~pyrogram.enums.ListenerTypes`, *optional*):
                The type of listener to stop listening for.
                Default to Message.

            chat_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``, *optional*):
                The user ID to stop listening for.

            message_id (``int``, *optional*):
                The message ID to stop listening for.

            inline_message_id (``str``, *optional*):
                The inline message ID to stop listening for.

        """
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        listeners = self.get_many_listeners_matching_with_identifier_pattern(
            pattern,
            listener_type,
        )

        for listener in listeners:
            await self.stop_listener(listener)
