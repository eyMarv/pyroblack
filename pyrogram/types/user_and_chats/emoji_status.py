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

import pyrogram
from pyrogram import raw, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class EmojiStatus(Object):
    """A user emoji status.

    Parameters
    ----------
        custom_emoji_id (``str``):
            Custom emoji id.

        until_date (:py:obj:`~datetime.datetime`, *optional*):
            Valid until date.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        custom_emoji_id: str,
        until_date: datetime | None = None,
        _raw: raw.base.EmojiStatus = None,
    ) -> None:
        super().__init__(client)

        self.custom_emoji_id = custom_emoji_id
        self.until_date = until_date
        self._raw = _raw

    @staticmethod
    def _parse(client, emoji_status: raw.base.EmojiStatus) -> EmojiStatus | None:
        if isinstance(emoji_status, raw.types.EmojiStatus):
            return EmojiStatus(
                client=client,
                custom_emoji_id=str(emoji_status.document_id),
                until_date=utils.timestamp_to_datetime(emoji_status.until),
                _raw=emoji_status,
            )

        if isinstance(emoji_status, raw.types.EmojiStatusCollectible):
            return EmojiStatus(
                client=client,
                custom_emoji_id=str(emoji_status.document_id),
                until_date=utils.timestamp_to_datetime(emoji_status.until),
                _raw=emoji_status,
            )

        return None

    def write(self):
        if self.until_date:
            return raw.types.EmojiStatusUntil(
                document_id=int(self.custom_emoji_id),
                until=utils.datetime_to_timestamp(self.until_date),
            )

        return raw.types.EmojiStatus(
            document_id=int(self.custom_emoji_id),
        )
