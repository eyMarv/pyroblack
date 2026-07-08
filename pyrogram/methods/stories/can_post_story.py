from typing import Union

import pyrogram
from pyrogram import errors, raw, types


class CanPostStory:
    async def can_post_story(self: "pyrogram.Client", chat_id: Union[int, str]) -> "types.CanPostStoryResult":
        try:
            r = await self.invoke(raw.functions.stories.CanSendStory(peer=await self.resolve_peer(chat_id)))
        except errors.PremiumAccountRequired:
            return types.CanPostStoryResultPremiumNeeded()
        except errors.BoostsRequired:
            return types.CanPostStoryResultBoostNeeded()
        except errors.StoriesTooMuch:
            return types.CanPostStoryResultActiveStoryLimitExceeded()
        except errors.StorySendFloodWeekly as ex:
            return types.CanPostStoryResultWeeklyLimitExceeded(retry_after=ex.value)
        except errors.StorySendFloodMonthly as ex:
            return types.CanPostStoryResultMonthlyLimitExceeded(retry_after=ex.value)
        except errors.StoryLiveAlready as ex:
            return types.CanPostStoryResultLiveStoryIsActive(story_id=ex.value)
        return types.CanPostStoryResultOk(story_count=r.count_remains)
