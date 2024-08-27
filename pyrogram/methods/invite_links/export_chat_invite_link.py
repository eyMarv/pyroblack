#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils


class ExportChatInviteLink:
    async def export_chat_invite_link(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        subscription_period: int = None,
        subscription_price: int = None,
    ) -> "types.ChatInviteLink":
        """Generate a new primary invite link for a chat; any previously generated primary link is revoked.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        .. note ::
            Each administrator in a chat generates their own invite links. Bots can't use invite links generated by
            other administrators. If you want your bot to work with invite links, it will need to generate its own link
            using this method – after this the link will become available to the bot via the
            :meth:`~pyrogram.Client.get_chat` method. If your bot needs to generate a new invite link replacing its
            previous one, use this method again.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            subscription_period (``int``, *optional*):
                Date when the subscription will expire.
                for now, only 30 days is supported (30*24*60*60).

            subscription_price (``int``, *optional*):
                Subscription price (stars).

        Returns:
            :obj:`~pyrogram.types.ChatInviteLink`: On success, the invite link is returned.

        Example:
            .. code-block:: python

                # Generate a new primary link
                link = await app.export_chat_invite_link(chat_id)
        """
        r = await self.invoke(
            raw.functions.messages.ExportChatInvite(
                peer=await self.resolve_peer(chat_id),
                legacy_revoke_permanent=True,
                subscription_pricing=raw.types.StarsSubscriptionPricing(
                    period=subscription_period, amount=subscription_price
                ),
            )
        )

        return types.ChatInviteLink._parse(self, r)
