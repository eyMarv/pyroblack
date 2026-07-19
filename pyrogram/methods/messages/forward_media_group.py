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
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from datetime import datetime


class ForwardMediaGroup:
    async def forward_media_group(
        self: pyrogram.Client,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        schedule_date: datetime | None = None,
        hide_sender_name: bool | None = None,
        hide_captions: bool | None = None,
        protect_content: bool | None = None,
    ) -> list[types.Message]:
        """Forward a media group by providing one of the message ids.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the source chat where the original message was sent.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in *from_chat_id*.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            hide_sender_name (``bool``, *optional*):
                If True, the original author of the message will not be shown.

            hide_captions (``bool``, *optional*):
                If True, the original media captions will be removed.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

        Returns
        -------
            List of :obj:`~pyrogram.types.Message`: On success, a list of forwarded messages is returned.

        Example:
            .. code-block:: python

                # Forward a media group
                await app.forward_media_group(to_chat, from_chat, 123)

        """
        message_ids = [
            i.id for i in await self.get_media_group(from_chat_id, message_id)
        ]

        r = await self.invoke(
            raw.functions.messages.ForwardMessages(
                to_peer=await self.resolve_peer(chat_id),
                from_peer=await self.resolve_peer(from_chat_id),
                id=message_ids,
                silent=disable_notification or None,
                random_id=[self.rnd_id() for _ in message_ids],
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                drop_author=hide_sender_name,
                drop_media_captions=hide_captions,
                noforwards=protect_content,
                top_msg_id=message_thread_id,
            ),
        )

        forwarded_messages = []

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage,
                    raw.types.UpdateNewScheduledMessage,
                ),
            ):
                forwarded_messages.append(
                    await types.Message._parse(self, i.message, users, chats),
                )

        return types.List(forwarded_messages)
