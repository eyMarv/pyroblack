import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class StoryArea(Object):
    def __init__(self, position: "types.StoryAreaPosition" = None, type: "types.StoryAreaType" = None):
        super().__init__()
        self.position = position
        self.type = type

    @staticmethod
    def _parse(client: "pyrogram.Client", area: "raw.base.MediaArea") -> "StoryArea":
        story_area_type = None
        if isinstance(area, raw.types.MediaAreaGeoPoint):
            story_area_type = types.StoryAreaTypeLocation(
                latitude=area.geo.lat,
                longitude=area.geo.long,
                horizontal_accuracy=area.geo.accuracy_radius,
                address=types.LocationAddress(
                    country_code=area.address.country_iso2,
                    state=area.address.state,
                    city=area.address.city,
                    street=area.address.street,
                ) if area.address else None,
            )
        elif isinstance(area, raw.types.MediaAreaSuggestedReaction):
            story_area_type = types.StoryAreaTypeSuggestedReaction(
                reaction_type=types.ReactionType._parse(client, area.reaction),
                is_dark=area.dark,
                is_flipped=area.flipped,
            )
        elif isinstance(area, raw.types.MediaAreaChannelPost):
            story_area_type = types.StoryAreaTypeMessage(
                chat_id=utils.get_channel_id(area.channel_id),
                message_id=area.msg_id,
            )
        elif isinstance(area, raw.types.MediaAreaUrl):
            story_area_type = types.StoryAreaTypeLink(url=area.url)
        elif isinstance(area, raw.types.MediaAreaWeather):
            story_area_type = types.StoryAreaTypeWeather(
                temperature=area.temperature_c,
                emoji=area.emoji,
                background_color=area.color,
            )
        elif isinstance(area, raw.types.MediaAreaStarGift):
            story_area_type = types.StoryAreaTypeUniqueGift(name=area.slug)
        return StoryArea(
            position=types.StoryAreaPosition._parse(area.coordinates),
            type=story_area_type,
        )

    def write(self, client: "pyrogram.Client"):
        coordinates = self.position.write()
        return self.type.write(client, coordinates)
