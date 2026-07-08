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
from pyrogram import raw, types


class SetReaction:
    async def set_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int = None,
        story_id: int = None,
        reaction: List["types.ReactionType"] = None,
        is_big: bool = False,
        add_to_recent: bool = True,
    ) -> "types.MessageReactions":
        raw_reactions = []
        if not reaction:
            raw_reactions = [raw.types.ReactionEmpty()]
        else:
            for r in reaction:
                if isinstance(r, types.ReactionType) and getattr(r, 'type', None) == 'paid':
                    raise ValueError('This type of reaction is not supported using this method')
                raw_reactions.append(r.write())

        if message_id is not None:
            r = await self.invoke(
                raw.functions.messages.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    reaction=raw_reactions,
                    big=is_big,
                    add_to_recent=add_to_recent,
                )
            )
            for i in r.updates:
                if isinstance(i, raw.types.UpdateMessageReactions):
                    return types.MessageReactions._parse(self, i.reactions)
            return r

        if story_id is not None:
            r = await self.invoke(
                raw.functions.stories.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    story_id=story_id,
                    reaction=raw_reactions[0],
                    add_to_recent=add_to_recent,
                )
            )
            return r

        raise ValueError('You need to pass one of message_id OR story_id!')
