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

import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class SendRecoveryCode:
    async def send_recovery_code(
        self: "pyrogram.Client",
    ) -> str:
        """Send a code to your email to recover your password.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``str``: On success, the hidden email pattern is returned and a recovery code is sent to that email.

        Raises:
            BadRequest: In case no recovery email was set up.

        """
        return (
            await self.invoke(
                raw.functions.auth.RequestPasswordRecovery(),
            )
        ).email_pattern
