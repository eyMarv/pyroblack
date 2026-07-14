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

from datetime import datetime, timezone
from typing import Union

import pyrogram
from pyrogram import raw, utils


class UpdateChatNotifications:
    async def update_chat_notifications(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        mute: bool = None,
        mute_until: datetime = None,
        stories_muted: bool = None,
        stories_hide_sender: bool = None,
        show_previews: bool = None
    ) -> bool:
        """Update the notification settings for the selected chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            mute (``bool``, *optional*):
                Pass True if you want to mute chat.

            mute_until (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unmuted. Works only if the mute
                parameter is set to True. Defaults to forever.

            stories_muted (``bool``, *optional*):
                Pass True to mute story notifications from this chat.

            stories_hide_sender (``bool``, *optional*):
                Pass True to hide the sender name in story notifications.

            show_previews (``bool``, *optional*):
                Pass True to show message text in notifications.

        Returns:
            ``bool``: True on success, False otherwise.

        Example:
            .. code-block:: python

                # Mute a chat permanently
                await app.update_chat_notifications(chat_id, mute=True)

                # Mute a chat for 10 minutes
                await app.update_chat_notifications(
                    chat_id,
                    mute=True,
                    mute_until=datetime.timedelta(minutes=10)
                )

                # Unmute a chat
                await app.update_chat_notifications(chat_id, mute=False)
        """
        if not mute_until:
            # Forever when muted; zero when unmuted (pyroblack has no utils.max_datetime)
            mute_until = (
                datetime.fromtimestamp(0x7FFFFFFF, timezone.utc)
                if mute
                else utils.zero_datetime()
            )

        r = await self.invoke(
            raw.functions.account.UpdateNotifySettings(
                peer=raw.types.InputNotifyPeer(peer=await self.resolve_peer(chat_id)),
                settings=raw.types.InputPeerNotifySettings(
                    show_previews=show_previews,
                    silent=mute,
                    mute_until=utils.datetime_to_timestamp(mute_until),
                    stories_muted=stories_muted,
                    stories_hide_sender=stories_hide_sender,
                )
            )
        )

        return r
