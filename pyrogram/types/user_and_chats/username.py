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

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class Username(Object):
    """Describes usernames assigned to a user, a supergroup, or a channel.

    Parameters
    ----------
        username (``str``):
            User's or chat's username.
        is_editable (``bool``, *optional*):
            True, if the username is editable.
        is_active (``bool``, *optional*):
            True, if the username is active.

    """

    def __init__(
        self,
        *,
        username: str,
        is_editable: bool | None = None,
        is_active: bool | None = None,
        **kwargs,
    ) -> None:
        super().__init__()

        self.username = username
        self.is_editable = is_editable
        self.is_active = is_active
        # pyroblack <= 2.7.2 short names
        self.editable = is_editable
        self.active = is_active

    @staticmethod
    def _parse(username: raw.types.Username) -> Username:
        return Username(
            username=username.username,
            is_editable=username.editable,
            is_active=username.active,
        )
