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
from pyrogram import enums, raw, types


class GetPrivacy:
    async def get_privacy(self: "pyrogram.Client", key: "enums.PrivacyKey"):
        """Get account privacy rules.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            key (:obj:`~pyrogram.enums.PrivacyKey`):
                Privacy key.

        Returns
        -------
            List of :obj:`~pyrogram.types.PrivacyRule`: On success, the list of privacy rules is returned.

        Example:
            .. code-block:: python

                from pyrogram import enums

                await app.get_privacy(enums.PrivacyKey.PHONE_NUMBER)

        """
        r = await self.invoke(raw.functions.account.GetPrivacy(key=key.value()))

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        return types.List(
            types.PrivacyRule._parse(self, rule, users, chats) for rule in r.rules
        )
