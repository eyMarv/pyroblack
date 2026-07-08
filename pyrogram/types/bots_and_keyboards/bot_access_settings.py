#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram import raw

from ..object import Object


class BotAccessSettings(Object):
    """This object represents bot access settings for a managed bot.

    Parameters:
        can_be_accessed_by_mentioned_users (``bool``, *optional*):
            Whether the bot can be accessed by mentioned users.

        can_be_accessed_everywhere (``bool``, *optional*):
            Whether the bot can be accessed in all chats.

        can_be_accessed_in_all_groups (``bool``, *optional*):
            Whether the bot can be accessed in all groups.

        conversation_commands (``bool``, *optional*):
            Whether the bot can receive conversation commands.
    """

    def __init__(
        self,
        *,
        can_be_accessed_by_mentioned_users: bool = None,
        can_be_accessed_everywhere: bool = None,
        can_be_accessed_in_all_groups: bool = None,
        conversation_commands: bool = None,
        deep_linking: bool = None,
        bot_reference: str = None,
    ):
        super().__init__()

        self.can_be_accessed_by_mentioned_users = can_be_accessed_by_mentioned_users
        self.can_be_accessed_everywhere = can_be_accessed_everywhere
        self.can_be_accessed_in_all_groups = can_be_accessed_in_all_groups
        self.conversation_commands = conversation_commands
        self.deep_linking = deep_linking
        self.bot_reference = bot_reference

    @staticmethod
    def _parse(settings: "raw.types.BotAccessSettings") -> "BotAccessSettings":
        return BotAccessSettings(
            can_be_accessed_by_mentioned_users=settings.can_be_accessed_by_mentioned_users,
            can_be_accessed_everywhere=settings.can_be_accessed_everywhere,
            can_be_accessed_in_all_groups=settings.can_be_accessed_in_all_groups,
            conversation_commands=settings.conversation_commands,
            deep_linking=settings.deep_linking,
            bot_reference=settings.bot_reference,
        )
