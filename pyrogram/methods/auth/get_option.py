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


class GetOption:
    @staticmethod
    def _parse_tggob_json(obj):
        """Recursively parses Telegram's raw JSON types into native Python types."""
        if isinstance(obj, (raw.types.JsonString, raw.types.JsonNumber)):
            return obj.value
        if isinstance(obj, raw.types.JsonBool):
            return obj.value
        if isinstance(obj, raw.types.JsonNull):
            return None
        if isinstance(obj, raw.types.JsonArray):
            # Recursively parse every item in the array to a Python list
            return [GetOption._parse_tggob_json(item) for item in obj.value]
        if isinstance(obj, raw.types.JsonObject):
            # Recursively parse every key-value pair to a Python dict
            return {
                item.key: GetOption._parse_tggob_json(item.value) for item in obj.value
            }
        # Fallback for base values
        return obj

    async def get_option(
        self: pyrogram.Client,
        name: str,
    ) -> bool | int | str | list | dict | None:
        """Returns the value of an option by its name.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            name (``str``):
                The name of the option.

        Returns
        -------
            ``bool`` | ``int`` | ``str`` | ``list`` | ``dict``: On success, the value of the option is returned.

        """
        app_config = await self.invoke(
            raw.functions.help.GetAppConfig(
                hash=0,
            ),
        )
        option = next(
            (x for x in app_config.config.value if x.key == name),
            None,
        )
        if not option:
            return option
        return self._parse_tggob_json(option.value)
