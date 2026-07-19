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

from typing import TYPE_CHECKING, Callable

import pyrogram
from pyrogram.types import Identifier, Listener

if TYPE_CHECKING:
    from pyrogram.filters import Filter


class RegisterNextStepHandler:
    def register_next_step_handler(
        self: pyrogram.Client,
        callback: Callable,
        filters: Filter | None = None,
        listener_type: pyrogram.enums.ListenerTypes = pyrogram.enums.ListenerTypes.MESSAGE,
        unallowed_click_alert: bool = True,
        chat_id: int | str | list[int | str] | None = None,
        user_id: int | str | list[int | str] | None = None,
        message_id: int | list[int] | None = None,
        inline_message_id: str | list[str] | None = None,
    ) -> None:
        """Registers a listener with a callback to be called when the listener is fulfilled.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            callback (``Callable``):
                The callback to call when the listener is fulfilled.

            chat_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``, *optional*):
                The chat ID to listen for.

            user_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``, *optional*):
                The user ID to listen for.

            filters (:obj:`~pyrogram.filters`, *optional*):
                A filter to check the incoming message against.

            listener_type (:obj:`~pyrogram.enums.ListenerTypes`, *optional*):
                The type of listener to listen for.
                Default to Message.

            unallowed_click_alert (``bool``, *optional*):
                Whether to alert the user if they click a button that doesn’t match the filters.
                Default to True.

            message_id (``int``, *optional*):
                The message ID to listen for.

            inline_message_id (``str``, *optional*):
                The inline message ID to listen for.

        """
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

        listener = Listener(
            callback=callback,
            filters=filters,
            unallowed_click_alert=unallowed_click_alert,
            identifier=pattern,
            listener_type=listener_type,
        )

        self.listeners[listener_type].append(listener)
