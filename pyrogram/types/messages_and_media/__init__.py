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

from .alternative_video import AlternativeVideo
from .animation import Animation
from .audio import Audio
from .checked_gift_code import CheckedGiftCode
from .checklist_task import ChecklistTask
from .checklist_tasks_added import ChecklistTasksAdded
from .checklist_tasks_done import ChecklistTasksDone
from .checklist import Checklist
from .available_effect import AvailableEffect
from .contact import Contact
from .dice import Dice
from .document import Document
from .external_reply_info import ExternalReplyInfo
from .exported_story_link import ExportedStoryLink
from .extended_media_preview import ExtendedMediaPreview
from .game import Game
from .giveaway import Giveaway
from .input_checklist_task import InputChecklistTask
from .giveaway_launched import GiveawayLaunched
from .giveaway_result import GiveawayResult
from .labeled_price import LabeledPrice
from .location import Location
from .media_area import MediaArea
from .media_area_channel_post import MediaAreaChannelPost
from .media_area_coordinates import MediaAreaCoordinates
from .message import Message
from .message_entity import MessageEntity
from .message_reaction_count_updated import MessageReactionCountUpdated
from .message_reaction_updated import MessageReactionUpdated
from .message_reactor import MessageReactor
from .message_reactions import MessageReactions
from .message_story import MessageStory
from .message_invoice import MessageInvoice
from .paid_media import PaidMedia
from .payment_form import PaymentForm
from .message_origin import MessageOrigin
from .message_origin_channel import MessageOriginChannel
from .message_origin_chat import MessageOriginChat
from .message_origin_hidden_user import MessageOriginHiddenUser
from .message_origin_import import MessageOriginImport
from .message_origin_user import MessageOriginUser
from .photo import Photo
from .poll import Poll
from .poll_option import PollOption
from .reaction import Reaction
from .reaction_count import ReactionCount
from .reaction_type import ReactionType
from .read_participant import ReadParticipant
from .sticker import Sticker
from .stickerset import StickerSet
from .stories_privacy_rules import StoriesPrivacyRules
from .story import Story
from .story_deleted import StoryDeleted
from .story_forward_header import StoryForwardHeader
from .story_skipped import StorySkipped
from .story_views import StoryViews
from .stripped_thumbnail import StrippedThumbnail
from .thumbnail import Thumbnail
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .voice import Voice
from .web_app_data import WebAppData
from .gift_code import GiftCode
from .web_page import WebPage
from .web_page_empty import WebPageEmpty
from .web_page_preview import WebPagePreview
from .transcribed_audio import TranscribedAudio
from .translated_text import TranslatedText
from .text_quote import TextQuote

__all__ = [
    "AlternativeVideo",
    "Animation",
    "Audio",
    "AvailableEffect",
    "Contact",
    "CheckedGiftCode",
    "ChecklistTask",
    "ChecklistTasksAdded",
    "ChecklistTasksDone",
    "Checklist",
    "Document",
    "ExternalReplyInfo",
    "ExtendedMediaPreview",
    "Game",
    "Giveaway",
    "GiveawayLaunched",
    "GiveawayResult",
    "GiftCode",
    "LabeledPrice",
    "Location",
    "MediaArea",
    "MediaAreaChannelPost",
    "MediaAreaCoordinates",
    "Message",
    "MessageEntity",
    "MessageOrigin",
    "MessageOriginChannel",
    "MessageOriginChat",
    "MessageOriginHiddenUser",
    "MessageOriginImport",
    "MessageOriginUser",
    "PaidMedia",
    "PaymentForm",
    "Photo",
    "Thumbnail",
    "StrippedThumbnail",
    "Poll",
    "PollOption",
    "Sticker",
    "StickerSet",
    "Venue",
    "Video",
    "VideoNote",
    "Voice",
    "WebPage",
    "WebPageEmpty",
    "WebPagePreview",
    "Dice",
    "Reaction",
    "WebAppData",
    "MessageInvoice",
    "MessageReactions",
    "ReactionCount",
    "ReactionType",
    "MessageReactionUpdated",
    "MessageReactionCountUpdated",
    "MessageReactor",
    "MessageStory",
    "ReadParticipant",
    "Story",
    "StoryDeleted",
    "StorySkipped",
    "StoryViews",
    "StoryForwardHeader",
    "StoriesPrivacyRules",
    "ExportedStoryLink",
    "TranscribedAudio",
    "TranslatedText",
    "TextQuote",
]
