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

from ..object import Object

from pyrogram import raw


class LoginToken(Object):
    """Contains info on a login token.

    Parameters:
        token (``str``):
            The login token.

        expires (``int``):
            The expiration date of the token in UNIX format.
    """

    def __init__(self, *, token: str, expires: int):
        super().__init__()

        self.token = token
        self.expires = expires

    @staticmethod
    def _parse(login_token: "raw.base.LoginToken") -> "LoginToken":
        return LoginToken(
            token=login_token.token,
            expires=login_token.expires,
        )
