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
    from pyrogram import types


class RequestPeerTypeChannel(Object):
    """Object used to request clients to send a channel identifier.

    Parameters
    ----------
        is_creator (``bool``, *optional*):
            If True, show only Channel which user is the owner.

        is_username (``bool``, *optional*):
            If True, show only Channel which has username.

        max (``int``, *optional*):
            Maximum number of channels to be returned.
            default 1.

        is_name_requested (``bool``, *optional*):
            If True, Channel name is requested.
            default True.

        is_username_requested (``bool``, *optional*):
            If True, Channel username is requested.
            default True.

        is_photo_requested (``bool``, *optional*):
            If True, Channel photo is requested.
            default True.

        user_privileges (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
            Privileged actions that an user administrator is able to take.

        bot_privileges (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
            Privileged actions that a bot administrator is able to take.

    """  # TODO user_admin_rights, bot_admin_rights

    def __init__(
        self,
        button_id: int = 0,
        is_creator: bool | None = None,
        is_username: bool | None = None,
        max: int = 1,
        is_name_requested: bool = True,
        is_username_requested: bool = True,
        is_photo_requested: bool = True,
        user_privileges: types.ChatPrivileges = None,
        bot_privileges: types.ChatPrivileges = None,
    ) -> None:
        super().__init__()

        self.is_creator = is_creator
        self.is_username = is_username
        self.max = max
        self.is_name_requested = is_name_requested
        self.is_username_requested = is_username_requested
        self.is_photo_requested = is_photo_requested
        self.user_privileges = user_privileges
        self.bot_privileges = bot_privileges
