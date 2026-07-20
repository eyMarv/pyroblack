#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2024 Dan <https://github.com/delivrance>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  This file is part of Pyroblack.
#
#  Pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  Pyroblack is a continuation fork of Pyrogram <https://github.com/pyrogram/pyrogram>
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyroblack.  If not, see <http://www.gnu.org/licenses/>.

# Story class lives in types.stories; re-export here for v2.7.2 import paths
from pyrogram.types.stories.story import Story

from .alternative_video import AlternativeVideo
from .animation import Animation
from .audio import Audio
from .available_effect import AvailableEffect
from .boosts_status import BoostsStatus
from .chat_boost import ChatBoost
from .chat_boost_added import ChatBoostAdded
from .chat_has_protected_content_disable_requested import (
    ChatHasProtectedContentDisableRequested,
)
from .chat_has_protected_content_toggled import ChatHasProtectedContentToggled
from .chat_owner_changed import ChatOwnerChanged
from .chat_owner_left import ChatOwnerLeft
from .checked_gift_code import CheckedGiftCode
from .checklist import Checklist
from .checklist_task import ChecklistTask
from .checklist_tasks_added import ChecklistTasksAdded
from .checklist_tasks_done import ChecklistTasksDone
from .contact import Contact
from .contact_registered import ContactRegistered
from .craft_gift_result import CraftGiftResult
from .dice import Dice
from .direct_message_price_changed import DirectMessagePriceChanged
from .direct_messages_topic import DirectMessagesTopic
from .document import Document
from .exported_story_link import ExportedStoryLink
from .extended_media_preview import ExtendedMediaPreview
from .external_reply_info import ExternalReplyInfo
from .fact_check import FactCheck
from .formatted_text import FormattedText
from .game import Game
from .gift import Gift
from .gift_attribute import GiftAttribute
from .gift_auction import GiftAuction
from .gift_auction_state import GiftAuctionState
from .gift_code import GiftCode
from .gift_collection import GiftCollection
from .gift_purchase_limit import GiftPurchaseLimit
from .gift_resale_parameters import GiftResaleParameters
from .gift_resale_price import GiftResalePrice
from .gift_upgrade_preview import GiftUpgradePreview
from .gift_upgrade_price import GiftUpgradePrice
from .gift_upgrade_variants import GiftUpgradeVariants
from .gifted_premium import GiftedPremium
from .gifted_stars import GiftedStars
from .gifted_ton import GiftedTon
from .giveaway import Giveaway
from .giveaway_completed import GiveawayCompleted
from .giveaway_created import GiveawayCreated
from .giveaway_launched import GiveawayLaunched
from .giveaway_prize_stars import GiveawayPrizeStars
from .giveaway_result import GiveawayResult
from .giveaway_winners import GiveawayWinners
from .labeled_price import LabeledPrice
from .live_photo import LivePhoto
from .location import ChatLocation, Location
from .mask_position import MaskPosition
from .media_area import MediaArea
from .media_area_channel_post import MediaAreaChannelPost
from .media_area_coordinates import MediaAreaCoordinates
from .message import Message
from .message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
from .message_effect import MessageEffect
from .message_entity import MessageEntity
from .message_invoice import MessageInvoice
from .message_origin import MessageOrigin
from .message_origin_channel import MessageOriginChannel
from .message_origin_chat import MessageOriginChat
from .message_origin_hidden_user import MessageOriginHiddenUser
from .message_origin_import import MessageOriginImport
from .message_origin_user import MessageOriginUser
from .message_reaction_count_updated import MessageReactionCountUpdated
from .message_reaction_updated import MessageReactionUpdated
from .message_reactions import MessageReactions
from .message_reactor import MessageReactor
from .message_story import MessageStory
from .my_boost import MyBoost
from .paid_message_price_changed import PaidMessagePriceChanged
from .paid_messages_refunded import PaidMessagesRefunded
from .paid_reactor import PaidReactor
from .payment_form import PaymentForm
from .photo import Photo
from .poll import Poll
from .poll_answer import PollAnswer
from .poll_option import PollOption
from .poll_option_added import PollOptionAdded
from .poll_option_deleted import PollOptionDeleted
from .premium_gift_code import PremiumGiftCode
from .reaction import (
    Reaction,
    ReactionCount,
    ReactionType,
    ReactionTypeCustomEmoji,
    ReactionTypeEmoji,
    ReactionTypePaid,
)
from .read_participant import ReadParticipant
from .rich_block import (
    RichBlock,
    RichBlockAnchor,
    RichBlockAnimation,
    RichBlockAudio,
    RichBlockBlockQuotation,
    RichBlockCaption,
    RichBlockCollage,
    RichBlockDetails,
    RichBlockDivider,
    RichBlockFooter,
    RichBlockList,
    RichBlockListItem,
    RichBlockMap,
    RichBlockMathematicalExpression,
    RichBlockParagraph,
    RichBlockPhoto,
    RichBlockPreformatted,
    RichBlockPullQuotation,
    RichBlockSectionHeading,
    RichBlockSlideshow,
    RichBlockTable,
    RichBlockTableCell,
    RichBlockThinking,
    RichBlockUnsupported,
    RichBlockVideo,
    RichBlockVoiceNote,
)
from .rich_message import RichMessage
from .rich_text import (
    RichText,
    RichTextAnchor,
    RichTextAnchorLink,
    RichTextBankCardNumber,
    RichTextBold,
    RichTextBotCommand,
    RichTextCashtag,
    RichTextCode,
    RichTextCustomEmoji,
    RichTextDateTime,
    RichTextEmailAddress,
    RichTextHashtag,
    RichTextItalic,
    RichTextMarked,
    RichTextMathematicalExpression,
    RichTextMention,
    RichTextPhoneNumber,
    RichTextReference,
    RichTextReferenceLink,
    RichTextSpoiler,
    RichTextStrikethrough,
    RichTextSubscript,
    RichTextSuperscript,
    RichTextTextMention,
    RichTextUnderline,
    RichTextUrl,
)
from .screenshot_taken import ScreenshotTaken
from .sponsored_message import SponsoredMessage
from .star_amount import StarAmount
from .sticker import Sticker
from .stickerset import StickerSet
from .stories_privacy_rules import StoriesPrivacyRules
from .story_deleted import StoryDeleted
from .story_forward_header import StoryForwardHeader
from .story_skipped import StorySkipped
from .story_views import StoryViews
from .stripped_thumbnail import StrippedThumbnail
from .suggested_post_approval_failed import SuggestedPostApprovalFailed
from .suggested_post_approved import SuggestedPostApproved
from .suggested_post_declined import SuggestedPostDeclined
from .suggested_post_info import SuggestedPostInfo
from .suggested_post_paid import SuggestedPostPaid
from .suggested_post_parameters import SuggestedPostParameters
from .suggested_post_price import (
    SuggestedPostPrice,
    SuggestedPostPriceStar,
    SuggestedPostPriceTon,
)
from .suggested_post_refunded import SuggestedPostRefunded
from .text_quote import TextQuote
from .thumbnail import Thumbnail
from .transcribed_audio import TranscribedAudio
from .translated_text import TranslatedText
from .upgraded_gift import UpgradedGift
from .upgraded_gift_attribute_id import UpgradedGiftAttributeId
from .upgraded_gift_attribute_id_backdrop import UpgradedGiftAttributeIdBackdrop
from .upgraded_gift_attribute_id_model import UpgradedGiftAttributeIdModel
from .upgraded_gift_attribute_id_symbol import UpgradedGiftAttributeIdSymbol
from .upgraded_gift_attribute_rarity import UpgradedGiftAttributeRarity
from .upgraded_gift_original_details import UpgradedGiftOriginalDetails
from .upgraded_gift_purchase_offer import UpgradedGiftPurchaseOffer
from .upgraded_gift_value_info import UpgradedGiftValueInfo
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .video_quality import VideoQuality
from .voice import Voice
from .web_app_data import WebAppData
from .web_page import WebPage
from .web_page_empty import WebPageEmpty
from .web_page_preview import WebPagePreview
from .write_access_allowed import WriteAccessAllowed

__all__ = [
    "AlternativeVideo",
    "Animation",
    "Audio",
    "AvailableEffect",
    "BoostsStatus",
    "ChatBoost",
    "ChatBoostAdded",
    "ChatHasProtectedContentDisableRequested",
    "ChatHasProtectedContentToggled",
    "ChatLocation",
    "ChatOwnerChanged",
    "ChatOwnerLeft",
    "CheckedGiftCode",
    "Checklist",
    "ChecklistTask",
    "ChecklistTasksAdded",
    "ChecklistTasksDone",
    "Contact",
    "ContactRegistered",
    "CraftGiftResult",
    "Dice",
    "DirectMessagePriceChanged",
    "DirectMessagesTopic",
    "Document",
    "ExportedStoryLink",
    "ExtendedMediaPreview",
    "ExternalReplyInfo",
    "FactCheck",
    "FormattedText",
    "Game",
    "Gift",
    "GiftAttribute",
    "GiftAuction",
    "GiftAuctionState",
    "GiftCode",
    "GiftCollection",
    "GiftPurchaseLimit",
    "GiftResaleParameters",
    "GiftResalePrice",
    "GiftUpgradePreview",
    "GiftUpgradePrice",
    "GiftUpgradeVariants",
    "GiftedPremium",
    "GiftedStars",
    "GiftedTon",
    "Giveaway",
    "GiveawayCompleted",
    "GiveawayCreated",
    "GiveawayLaunched",
    "GiveawayPrizeStars",
    "GiveawayResult",
    "GiveawayWinners",
    "LabeledPrice",
    "LivePhoto",
    "Location",
    "MaskPosition",
    "MediaArea",
    "MediaAreaChannelPost",
    "MediaAreaCoordinates",
    "Message",  # TODO
    "MessageAutoDeleteTimerChanged",
    "MessageEffect",
    "MessageEntity",
    "MessageInvoice",
    "MessageOrigin",
    "MessageOriginChannel",
    "MessageOriginChat",
    "MessageOriginHiddenUser",
    "MessageOriginImport",
    "MessageOriginUser",
    "MessageReactionCountUpdated",
    "MessageReactionUpdated",
    "MessageReactions",
    "MessageReactor",
    "MessageStory",
    "MyBoost",
    "PaidMessagePriceChanged",
    "PaidMessagesRefunded",
    "PaidReactor",
    "PaymentForm",
    "Photo",
    "Poll",
    "PollAnswer",
    "PollOption",
    "PollOptionAdded",
    "PollOptionDeleted",
    "PremiumGiftCode",
    "Reaction",
    "ReactionCount",
    "ReactionType",
    "ReactionTypeCustomEmoji",
    "ReactionTypeEmoji",
    "ReactionTypePaid",
    "ReadParticipant",
    "RichBlock",
    "RichBlockAnchor",
    "RichBlockAnimation",
    "RichBlockAudio",
    "RichBlockBlockQuotation",
    "RichBlockCaption",
    "RichBlockCollage",
    "RichBlockDetails",
    "RichBlockDivider",
    "RichBlockFooter",
    "RichBlockList",
    "RichBlockListItem",
    "RichBlockMap",
    "RichBlockMathematicalExpression",
    "RichBlockParagraph",
    "RichBlockPhoto",
    "RichBlockPreformatted",
    "RichBlockPullQuotation",
    "RichBlockSectionHeading",
    "RichBlockSlideshow",
    "RichBlockTable",
    "RichBlockTableCell",
    "RichBlockThinking",
    "RichBlockUnsupported",
    "RichBlockVideo",
    "RichBlockVoiceNote",
    "RichMessage",
    "RichText",
    "RichTextAnchor",
    "RichTextAnchorLink",
    "RichTextBankCardNumber",
    "RichTextBold",
    "RichTextBotCommand",
    "RichTextCashtag",
    "RichTextCode",
    "RichTextCustomEmoji",
    "RichTextDateTime",
    "RichTextEmailAddress",
    "RichTextHashtag",
    "RichTextItalic",
    "RichTextMarked",
    "RichTextMathematicalExpression",
    "RichTextMention",
    "RichTextPhoneNumber",
    "RichTextReference",
    "RichTextReferenceLink",
    "RichTextSpoiler",
    "RichTextStrikethrough",
    "RichTextSubscript",
    "RichTextSuperscript",
    "RichTextTextMention",
    "RichTextUnderline",
    "RichTextUrl",
    "ScreenshotTaken",
    "SponsoredMessage",
    "StarAmount",
    "Sticker",
    "Sticker",
    "StickerSet",
    "StoriesPrivacyRules",
    "Story",
    "StoryDeleted",
    "StoryForwardHeader",
    "StorySkipped",
    "StoryViews",
    "StrippedThumbnail",
    "SuggestedPostApprovalFailed",
    "SuggestedPostApproved",
    "SuggestedPostDeclined",
    "SuggestedPostInfo",
    "SuggestedPostPaid",
    "SuggestedPostParameters",
    "SuggestedPostPrice",
    "SuggestedPostPriceStar",
    "SuggestedPostPriceTon",
    "SuggestedPostRefunded",
    "TextQuote",
    "Thumbnail",
    "TranscribedAudio",
    "TranslatedText",
    "UpgradedGift",
    "UpgradedGiftAttributeId",
    "UpgradedGiftAttributeIdBackdrop",
    "UpgradedGiftAttributeIdModel",
    "UpgradedGiftAttributeIdSymbol",
    "UpgradedGiftAttributeRarity",
    "UpgradedGiftOriginalDetails",
    "UpgradedGiftPurchaseOffer",
    "UpgradedGiftValueInfo",
    "Venue",
    "Video",
    "VideoNote",
    "VideoQuality",
    "Voice",
    "WebAppData",
    "WebPage",
    "WebPageEmpty",
    "WebPagePreview",
    "WriteAccessAllowed",
]
