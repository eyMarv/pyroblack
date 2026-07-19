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

from pyrogram import raw
from pyrogram.types.object import Object


class VerificationStatus(Object):
    """Contains information about verification status of a chat or a user.

    Parameters
    ----------
        is_verified (``bool``, *optional*):
            True, if this user has been verified by Telegram.

        is_scam (``bool``, *optional*):
            True, if this user has been flagged for scam.

        is_fake (``bool``, *optional*):
            True, if this user has been flagged for impersonation.

        bot_verification_icon_custom_emoji_id (``str``, *optional*):
            Contains information about verification status of a user.

    """

    def __init__(
        self,
        *,
        is_verified: bool | None = None,
        is_scam: bool | None = None,
        is_fake: bool | None = None,
        bot_verification_icon_custom_emoji_id: str | None = None,
    ) -> None:
        super().__init__()

        self.is_verified = is_verified
        self.is_scam = is_scam
        self.is_fake = is_fake
        self.bot_verification_icon_custom_emoji_id = (
            bot_verification_icon_custom_emoji_id
        )

    @staticmethod
    def _parse(
        chat: raw.base.User | raw.base.Chat | raw.base.ChatInvite,
    ) -> VerificationStatus | None:
        if not isinstance(
            chat, (raw.types.User, raw.types.Channel, raw.types.ChatInvite)
        ):
            return None

        bot_verification_icon = None

        if isinstance(chat, raw.types.ChatInvite):
            bot_verification_icon = getattr(chat.bot_verification, "icon", None)
        else:
            bot_verification_icon = chat.bot_verification_icon

        return VerificationStatus(
            is_verified=chat.verified,
            is_scam=chat.scam,
            is_fake=chat.fake,
            bot_verification_icon_custom_emoji_id=str(bot_verification_icon)
            if bot_verification_icon
            else None,
        )
