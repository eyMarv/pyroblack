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

"""Supergroup and channel setting toggles ported from wzgram and kurigram.

Each of these wraps a single ``channels.*`` RPC that pyroblack already generates
but did not expose from the high-level client. They follow the house convention
for a state-changing chat method: return the generated service
:obj:`~pyrogram.types.Message` when Telegram sends one, otherwise ``True``.
"""

from __future__ import annotations

import pyrogram
from pyrogram import raw, types


async def _invoke_and_parse(
    client: pyrogram.Client,
    query,
) -> types.Message | bool:
    """Invoke *query* and return the service message it generated, else True."""
    r = await client.invoke(query)

    for update in r.updates:
        if isinstance(
            update,
            (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage),
        ):
            return await types.Message._parse(
                client,
                update.message,
                {i.id: i for i in r.users},
                {i.id: i for i in r.chats},
                replies=client.fetch_replies,
            )

    return True


class ToggleAntiSpam:
    async def toggle_anti_spam(
        self: pyrogram.Client,
        chat_id: int | str,
        enabled: bool = True,
    ) -> types.Message | bool:
        """Enable or disable the native anti-spam filter in a supergroup.

        Requires the ``can_delete_messages`` administrator right, and the
        supergroup must have at least ``telegram_antispam_group_size_min``
        members.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            enabled (``bool``, *optional*):
                Pass True to enable the filter, False to disable it.
                Defaults to True.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: The generated service
            message, or True when Telegram did not send one.

        Example:
            .. code-block:: python

                await app.toggle_anti_spam(chat_id)

        """
        return await _invoke_and_parse(
            self,
            raw.functions.channels.ToggleAntiSpam(
                channel=await self.resolve_peer(chat_id),
                enabled=enabled,
            ),
        )


class ToggleSignatures:
    async def toggle_signatures(
        self: pyrogram.Client,
        chat_id: int | str,
        signatures_enabled: bool = True,
        profiles_enabled: bool | None = None,
    ) -> types.Message | bool:
        """Enable or disable author signatures on channel posts.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target channel.

            signatures_enabled (``bool``, *optional*):
                Pass True to show the author's name on each post.
                Defaults to True.

            profiles_enabled (``bool``, *optional*):
                Pass True to also link the signature to the author's profile.
                Only meaningful when *signatures_enabled* is True.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: The generated service
            message, or True when Telegram did not send one.

        Example:
            .. code-block:: python

                await app.toggle_signatures(chat_id, True, profiles_enabled=True)

        """
        return await _invoke_and_parse(
            self,
            raw.functions.channels.ToggleSignatures(
                channel=await self.resolve_peer(chat_id),
                signatures_enabled=signatures_enabled,
                profiles_enabled=profiles_enabled,
            ),
        )


class TogglePreHistoryHidden:
    async def toggle_pre_history_hidden(
        self: pyrogram.Client,
        chat_id: int | str,
        enabled: bool = True,
    ) -> types.Message | bool:
        """Hide or show the message history for members who join later.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            enabled (``bool``, *optional*):
                Pass True to hide the history from new members.
                Defaults to True.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: The generated service
            message, or True when Telegram did not send one.

        Example:
            .. code-block:: python

                await app.toggle_pre_history_hidden(chat_id)

        """
        return await _invoke_and_parse(
            self,
            raw.functions.channels.TogglePreHistoryHidden(
                channel=await self.resolve_peer(chat_id),
                enabled=enabled,
            ),
        )


class ToggleParticipantsHidden:
    async def toggle_participants_hidden(
        self: pyrogram.Client,
        chat_id: int | str,
        enabled: bool = True,
    ) -> types.Message | bool:
        """Hide or show the member list of a supergroup.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            enabled (``bool``, *optional*):
                Pass True to hide the member list. Defaults to True.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: The generated service
            message, or True when Telegram did not send one.

        Example:
            .. code-block:: python

                await app.toggle_participants_hidden(chat_id)

        """
        return await _invoke_and_parse(
            self,
            raw.functions.channels.ToggleParticipantsHidden(
                channel=await self.resolve_peer(chat_id),
                enabled=enabled,
            ),
        )


class ToggleViewForumAsMessages:
    async def toggle_view_forum_as_messages(
        self: pyrogram.Client,
        chat_id: int | str,
        enabled: bool = True,
    ) -> types.Message | bool:
        """Show a forum as a flat message list instead of a topic list.

        This is a per-account display preference, not a chat setting.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target forum.

            enabled (``bool``, *optional*):
                Pass True to view the forum as messages. Defaults to True.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: The generated service
            message, or True when Telegram did not send one.

        Example:
            .. code-block:: python

                await app.toggle_view_forum_as_messages(chat_id)

        """
        return await _invoke_and_parse(
            self,
            raw.functions.channels.ToggleViewForumAsMessages(
                channel=await self.resolve_peer(chat_id),
                enabled=enabled,
            ),
        )


class ToggleAutoTranslation:
    async def toggle_auto_translation(
        self: pyrogram.Client,
        chat_id: int | str,
        enabled: bool = True,
    ) -> types.Message | bool:
        """Enable or disable automatic translation of posts in a channel.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target channel.

            enabled (``bool``, *optional*):
                Pass True to enable automatic translation. Defaults to True.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: The generated service
            message, or True when Telegram did not send one.

        Example:
            .. code-block:: python

                await app.toggle_auto_translation(chat_id)

        """
        return await _invoke_and_parse(
            self,
            raw.functions.channels.ToggleAutotranslation(
                channel=await self.resolve_peer(chat_id),
                enabled=enabled,
            ),
        )


class RestrictSponsoredMessages:
    async def restrict_sponsored_messages(
        self: pyrogram.Client,
        chat_id: int | str,
        restricted: bool = True,
    ) -> types.Message | bool:
        """Turn sponsored messages off in a channel you own.

        Requires the channel to have enough boosts.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target channel.

            restricted (``bool``, *optional*):
                Pass True to stop showing sponsored messages.
                Defaults to True.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: The generated service
            message, or True when Telegram did not send one.

        Example:
            .. code-block:: python

                await app.restrict_sponsored_messages(chat_id)

        """
        return await _invoke_and_parse(
            self,
            raw.functions.channels.RestrictSponsoredMessages(
                channel=await self.resolve_peer(chat_id),
                restricted=restricted,
            ),
        )


class ChatToggles(
    RestrictSponsoredMessages,
    ToggleAntiSpam,
    ToggleAutoTranslation,
    ToggleParticipantsHidden,
    TogglePreHistoryHidden,
    ToggleSignatures,
    ToggleViewForumAsMessages,
):
    pass
