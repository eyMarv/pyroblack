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
from .auction_bid import AuctionBid
from .auction_round import AuctionRound
from .auction_state import AuctionState, AuctionStateActive, AuctionStateFinished
from .checked_gift_code import CheckedGiftCode
from .checklist_task import ChecklistTask
from .checklist_tasks_added import ChecklistTasksAdded
from .checklist_tasks_done import ChecklistTasksDone
from .checklist import Checklist
from .available_effect import AvailableEffect
from .chat_boost import ChatBoost
from .chat_boost_updated import ChatBoostUpdated
from .chat_has_protected_content_disable_requested import ChatHasProtectedContentDisableRequested
from .chat_has_protected_content_toggled import ChatHasProtectedContentToggled
from .chat_owner_changed import ChatOwnerChanged
from .chat_owner_left import ChatOwnerLeft
from .chat_theme import ChatTheme
from .contact import Contact
from .contact_registered import ContactRegistered
from .dice import Dice
from .direct_message_price_changed import DirectMessagePriceChanged
from .direct_messages_topic import DirectMessagesTopic
from .document import Document
from .external_reply_info import ExternalReplyInfo
from .exported_story_link import ExportedStoryLink
from .extended_media_preview import ExtendedMediaPreview
from .fact_check import FactCheck
from .formatted_text import FormattedText
from .game import Game
from .giveaway import Giveaway
from .giveaway_completed import GiveawayCompleted
from .giveaway_created import GiveawayCreated
from .input_checklist_task import InputChecklistTask
from .input_checklist import InputChecklist
from .giveaway_launched import GiveawayLaunched
from .giveaway_prize_stars import GiveawayPrizeStars
from .giveaway_result import GiveawayResult
from .labeled_price import LabeledPrice
from .link_preview_options import LinkPreviewOptions
from .location import Location
from .managed_bot_created import ManagedBotCreated
from .media_area import MediaArea
from .media_area_channel_post import MediaAreaChannelPost
from .media_area_coordinates import MediaAreaCoordinates
from .message import Message
from .message_entity import MessageEntity
from .message_reaction_count_updated import MessageReactionCountUpdated
from .message_reaction_updated import MessageReactionUpdated
from .message_effect import MessageEffect
from .message_reactor import MessageReactor
from .message_reactions import MessageReactions
from .my_boost import MyBoost
from .boosts_status import BoostsStatus
from .message_story import MessageStory
from .message_invoice import MessageInvoice
from .paid_media import PaidMedia
from .paid_media_purchased import PaidMediaPurchased
from .paid_messages_price_changed import PaidMessagesPriceChanged
from .paid_messages_refunded import PaidMessagesRefunded
from .payment_form import PaymentForm
from .payment_option import PaymentOption
from .payment_result import PaymentResult
from .premium_gift_code import PremiumGiftCode
from .message_origin import MessageOrigin
from .message_origin_channel import MessageOriginChannel
from .message_origin_chat import MessageOriginChat
from .message_origin_hidden_user import MessageOriginHiddenUser
from .message_origin_import import MessageOriginImport
from .message_origin_user import MessageOriginUser
from .photo import Photo
from .poll import Poll
from .poll_option_added import PollOptionAdded
from .poll_option_deleted import PollOptionDeleted
from .poll_option import PollOption
from .input_poll_option import InputPollOption
from .proximity_alert_triggered import ProximityAlertTriggered
from .reaction import Reaction
from .reaction_count import ReactionCount
from .reaction_type import ReactionType
from .read_participant import ReadParticipant
from .reply_parameters import ReplyParameters
from .restriction_reason import RestrictionReason
from .saved_credentials import SavedCredentials
from .sponsored_message import SponsoredMessage
from .sticker import Sticker
from .stickerset import StickerSet
from .suggested_post_approval_failed import SuggestedPostApprovalFailed
from .suggested_post_approved import SuggestedPostApproved
from .suggested_post_declined import SuggestedPostDeclined
from .stories_privacy_rules import StoriesPrivacyRules
from .story import Story
from .story_deleted import StoryDeleted
from .story_forward_header import StoryForwardHeader
from .story_skipped import StorySkipped
from .story_views import StoryViews
from .story_view import StoryView
from .suggested_post_info import SuggestedPostInfo
from .suggested_post_paid import SuggestedPostPaid
from .suggested_post_parameters import SuggestedPostParameters
from .suggested_post_price import SuggestedPostPrice, SuggestedPostPriceStar, SuggestedPostPriceTon
from .suggested_post_refunded import SuggestedPostRefunded
from .screenshot_taken import ScreenshotTaken
from .stripped_thumbnail import StrippedThumbnail
from .thumbnail import Thumbnail
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .video_quality import VideoQuality
from .voice import Voice
from .web_app_data import WebAppData
from .write_access_allowed import WriteAccessAllowed
from .gift_code import GiftCode
from .gift_resale_price import GiftResalePrice, GiftResalePriceStar, GiftResalePriceTon
from .gift_purchase_limit import GiftPurchaseLimit
from .gift_attribute import GiftAttribute
from .gift_auction import GiftAuction
from .gift_auction_state import GiftAuctionState
from .gift import Gift
from .gift_collection import GiftCollection
from .gift_upgrade_price import GiftUpgradePrice
from .gift_upgrade_preview import GiftUpgradePreview
from .gift_upgrade_variants import GiftUpgradeVariants
from .gifted_premium import GiftedPremium
from .gifted_stars import GiftedStars
from .gifted_ton import GiftedTon
from .gift_resale_parameters import GiftResaleParameters
from .upgraded_gift_attribute_rarity import (
    UpgradedGiftAttributeRarity,
    UpgradedGiftAttributeRarityEpic,
    UpgradedGiftAttributeRarityLegendary,
    UpgradedGiftAttributeRarityPerMille,
    UpgradedGiftAttributeRarityRare,
    UpgradedGiftAttributeRarityUncommon,
)
from .upgraded_gift_attribute_id_backdrop import UpgradedGiftAttributeIdBackdrop
from .upgraded_gift_attribute_id_model import UpgradedGiftAttributeIdModel
from .upgraded_gift_attribute_id_symbol import UpgradedGiftAttributeIdSymbol
from .upgraded_gift_attribute_id import UpgradedGiftAttributeId
from .upgraded_gift import UpgradedGift
from .upgraded_gift_value_info import UpgradedGiftValueInfo
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
    "AuctionBid",
    "AuctionRound",
    "AuctionState",
    "AuctionStateActive",
    "AuctionStateFinished",
    "AvailableEffect",
    "Contact",
    "CheckedGiftCode",
    "ChecklistTask",
    "ChecklistTasksAdded",
    "ChecklistTasksDone",
    "Checklist",
    "InputChecklistTask",
    "InputChecklist",
    "ChatBoost",
    "ChatBoostUpdated",
    "ChatHasProtectedContentDisableRequested",
    "ChatHasProtectedContentToggled",
    "ChatOwnerChanged",
    "ChatOwnerLeft",
    "ChatTheme",
    "ContactRegistered",
    "DirectMessagePriceChanged",
    "DirectMessagesTopic",
    "Document",
    "ExternalReplyInfo",
    "ExtendedMediaPreview",
    "FactCheck",
    "FormattedText",
    "Game",
    "Giveaway",
    "GiveawayCompleted",
    "GiveawayCreated",
    "GiveawayLaunched",
    "GiveawayPrizeStars",
    "GiveawayResult",
    "GiftCode",
    "GiftResalePrice",
    "GiftResalePriceStar",
    "GiftResalePriceTon",
    "GiftPurchaseLimit",
    "GiftAttribute",
    "GiftAuction",
    "GiftAuctionState",
    "Gift",
    "GiftCollection",
    "GiftUpgradePrice",
    "GiftUpgradePreview",
    "GiftUpgradeVariants",
    "GiftedPremium",
    "GiftedStars",
    "GiftedTon",
    "GiftResaleParameters",
    "UpgradedGiftAttributeRarity",
    "UpgradedGiftAttributeRarityEpic",
    "UpgradedGiftAttributeRarityLegendary",
    "UpgradedGiftAttributeRarityPerMille",
    "UpgradedGiftAttributeRarityRare",
    "UpgradedGiftAttributeRarityUncommon",
    "UpgradedGiftAttributeIdBackdrop",
    "UpgradedGiftAttributeIdModel",
    "UpgradedGiftAttributeIdSymbol",
    "UpgradedGiftAttributeId",
    "UpgradedGift",
    "UpgradedGiftValueInfo",
    "LabeledPrice",
    "LinkPreviewOptions",
    "Location",
    "ManagedBotCreated",
    "MediaArea",
    "MediaAreaChannelPost",
    "MediaAreaCoordinates",
    "Message",
    "MessageEffect",
    "MessageEntity",
    "MessageOrigin",
    "MessageOriginChannel",
    "MessageOriginChat",
    "MessageOriginHiddenUser",
    "MessageOriginImport",
    "MessageOriginUser",
    "PaidMedia",
    "PaidMediaPurchased",
    "PaymentForm",
    "PaymentOption",
    "PaymentResult",
    "PremiumGiftCode",
    "Photo",
    "Thumbnail",
    "StrippedThumbnail",
    "Poll",
    "PollOptionAdded",
    "PollOptionDeleted",
    "PollOption",
    "InputPollOption",
    "SponsoredMessage",
    "Sticker",
    "StickerSet",
    "Venue",
    "Video",
    "VideoNote",
    "VideoQuality",
    "Voice",
    "WebPage",
    "WebPageEmpty",
    "WebPagePreview",
    "Dice",
    "Reaction",
    "WebAppData",
    "WriteAccessAllowed",
    "MessageInvoice",
    "MessageReactions",
    "MyBoost",
    "BoostsStatus",
    "PaidMessagesPriceChanged",
    "PaidMessagesRefunded",
    "ProximityAlertTriggered",
    "ReactionCount",
    "ReactionType",
    "MessageReactionUpdated",
    "MessageReactionCountUpdated",
    "MessageReactor",
    "MessageStory",
    "ReadParticipant",
    "ReplyParameters",
    "RestrictionReason",
    "SavedCredentials",
    "SuggestedPostApprovalFailed",
    "SuggestedPostApproved",
    "SuggestedPostDeclined",
    "Story",
    "StoryDeleted",
    "StorySkipped",
    "StoryViews",
    "StoryView",
    "StoryForwardHeader",
    "SuggestedPostInfo",
    "SuggestedPostPaid",
    "SuggestedPostParameters",
    "SuggestedPostPrice",
    "SuggestedPostPriceStar",
    "SuggestedPostPriceTon",
    "SuggestedPostRefunded",
    "ScreenshotTaken",
    "StoriesPrivacyRules",
    "ExportedStoryLink",
    "TranscribedAudio",
    "TranslatedText",
    "TextQuote",
]
