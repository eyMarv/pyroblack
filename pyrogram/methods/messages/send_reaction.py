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

from typing import List, Union

import pyrogram
from pyrogram import raw


class SendReaction:
    async def send_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int = None,
        story_id: int = None,
        emoji: Union[int, str, List[Union[int, str]]] = None,
        big: bool = False,
        add_to_recent: bool = False,
    ) -> bool:
        """Send a reaction to a message or story.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``, *optional*):
                Identifier of the message.

            story_id (``int``, *optional*):
                Identifier of the story.

            emoji (``int`` | ``str`` | List of ``int`` | ``str``, *optional*):
                Reaction emoji.
                Pass None as emoji (default) to retract the reaction.
                Pass list of int or str to react with multiple emojis on messages.

            big (``bool``, *optional*):
                Pass True to show a bigger and longer reaction for messages.

            add_to_recent (``bool``, *optional*):
                Pass True to add the reaction to the recent reactions list.

        Returns:
            ``bool``: On success, True is returned.
        """
        if isinstance(emoji, list):
            reaction = [
                raw.types.ReactionCustomEmoji(document_id=i)
                if isinstance(i, int)
                else raw.types.ReactionEmoji(emoticon=i)
                for i in emoji
            ] if emoji else None
        else:
            reaction = (
                [raw.types.ReactionCustomEmoji(document_id=emoji)]
                if isinstance(emoji, int)
                else ([raw.types.ReactionEmoji(emoticon=emoji)] if emoji else None)
            )

        if message_id is not None:
            await self.invoke(
                raw.functions.messages.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    reaction=reaction,
                    big=big,
                    add_to_recent=add_to_recent,
                )
            )
            return True

        if story_id is not None:
            await self.invoke(
                raw.functions.stories.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    story_id=story_id,
                    reaction=(reaction[0] if reaction else raw.types.ReactionEmpty()),
                    add_to_recent=add_to_recent,
                )
            )
            return True

        raise ValueError("You need to pass one of message_id or story_id")
