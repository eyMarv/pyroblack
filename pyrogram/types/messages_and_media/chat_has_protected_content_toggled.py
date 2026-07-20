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
from pyrogram.types.object import Object


class ChatHasProtectedContentToggled(Object):
    """Describes a service message about a chat ``has_protected_content`` setting was changed or request to change it was rejected.

    Parameters
    ----------
        request_message_id (``int``):
            Identifier of the message with the request to change the setting; can be an identifier of a deleted message or 0.

        old_has_protected_content (``bool``):
            Previous value of the setting.

        new_has_protected_content (``bool``):
            New value of the setting.

    """

    def __init__(
        self,
        *,
        request_message_id: int | None = None,
        old_has_protected_content: bool | None = None,
        new_has_protected_content: bool | None = None,
    ) -> None:
        super().__init__()

        self.request_message_id = request_message_id
        self.old_has_protected_content = old_has_protected_content
        self.new_has_protected_content = new_has_protected_content

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        message: raw.types.MessageService,
    ) -> ChatHasProtectedContentToggled:
        action: raw.types.MessageActionNoForwardsToggle = message.action
        if isinstance(action, raw.types.MessageActionNoForwardsToggle):
            return ChatHasProtectedContentToggled(
                request_message_id=message.id,
                old_has_protected_content=action.prev_value,
                new_has_protected_content=action.new_value,
            )
        return None
