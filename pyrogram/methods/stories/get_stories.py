from typing import Iterable, Union

import pyrogram
from pyrogram import raw, types, utils


class GetStories:
    async def get_stories(
        self: "pyrogram.Client",
        story_poster_chat_id: Union[int, str],
        story_ids: Union[int, Iterable[int]],
    ):
        is_iterable = utils.is_list_like(story_ids)
        ids = list(story_ids) if is_iterable else [story_ids]

        peer = await self.resolve_peer(story_poster_chat_id)
        r = await self.invoke(
            raw.functions.stories.GetStoriesByID(
                peer=peer,
                id=ids,
            )
        )

        stories = []
        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        for story in r.stories:
            stories.append(
                await types.Story._parse(
                    self,
                    story,
                    peer,
                    users,
                    chats,
                )
            )

        return types.List(stories) if is_iterable else stories[0] if stories else None
