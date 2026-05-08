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

from typing import List, Optional

from pyrogram import raw, types
from ..object import Object


class PrivacyRule(Object):
    """A privacy rule.

    Parameters:
        allow_all (``bool``, *optional*):
            Allow all users.

        allow_chats (``bool``, *optional*):
            Allow only participants of certain chats.

        allow_contacts (``bool``, *optional*):
            Allow contacts only

        allow_premium (``bool``, *optional*):
            Allow only users with a Premium subscription, currently only usable for :obj:`~pyrogram.enums.PrivacyKey.CHAT_INVITE`.

        allow_users (``bool``, *optional*):
            Allow only participants of certain users.

        users (List of :obj:`~pyrogram.types.User`, *optional*):
            List of users.

        chats (List of :obj:`~pyrogram.types.Chat`, *optional*):
            List of chats.
    """

    def __init__(
        self,
        *,
        allow_all: Optional[bool] = None,
        allow_chats: Optional[bool] = None,
        allow_contacts: Optional[bool] = None,
        allow_premium: Optional[bool] = None,
        allow_users: Optional[bool] = None,
        users: Optional[List["types.User"]] = None,
        chats: Optional[List["types.Chat"]] = None,
    ):
        super().__init__(None)

        self.allow_all = allow_all
        self.allow_chats = allow_chats
        self.allow_contacts = allow_contacts
        self.allow_premium = allow_premium
        self.allow_users = allow_users
        self.users = users
        self.chats = chats

    @staticmethod
    def _parse(client, rule: "raw.base.PrivacyRule", users, chats) -> "PrivacyRule":
        parsed_users = None
        parsed_chats = None

        if isinstance(
            rule,
            (raw.functions.PrivacyValueAllowUsers, raw.functions.PrivacyValueDisallowUsers),
        ):
            parsed_users = types.List(
                types.User._parse(client, users.get(i)) for i in rule.users
            )

        if isinstance(
            rule,
            (
                raw.functions.PrivacyValueAllowChatParticipants,
                raw.functions.PrivacyValueDisallowChatParticipants,
            ),
        ):
            parsed_chats = types.List(
                types.Chat._parse_chat(client, chats.get(i)) for i in rule.chats
            )

        return PrivacyRule(
            allow_all=(
                True
                if isinstance(rule, raw.functions.PrivacyValueAllowAll)
                else (
                    False
                    if isinstance(rule, raw.functions.PrivacyValueDisallowAll)
                    else None
                )
            ),
            allow_chats=(
                True
                if isinstance(rule, raw.functions.PrivacyValueAllowChatParticipants)
                else (
                    False
                    if isinstance(rule, raw.functions.PrivacyValueDisallowChatParticipants)
                    else None
                )
            ),
            allow_contacts=(
                True
                if isinstance(rule, raw.functions.PrivacyValueAllowContacts)
                else (
                    False
                    if isinstance(rule, raw.functions.PrivacyValueDisallowContacts)
                    else None
                )
            ),
            allow_premium=(
                True if isinstance(rule, raw.functions.PrivacyValueAllowPremium) else None
            ),
            allow_users=(
                True
                if isinstance(rule, raw.functions.PrivacyValueAllowUsers)
                else (
                    False
                    if isinstance(rule, raw.functions.PrivacyValueDisallowUsers)
                    else None
                )
            ),
            users=parsed_users or None,
            chats=parsed_chats or None,
        )
