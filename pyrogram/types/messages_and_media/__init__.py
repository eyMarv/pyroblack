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

from .animation import Animation
from .audio import Audio
from .contact import Contact
from .contact_registered import ContactRegistered
from .dice import Dice
from .direct_messages_topic import DirectMessagesTopic
from .document import Document
from .game import Game
from .location import ChatLocation, Location
from .message import Message
from .message_entity import MessageEntity
from .photo import Photo
from .poll import Poll
from .poll_answer import PollAnswer
from .poll_option import PollOption
from .reaction import (
    Reaction,
    ReactionType,
    ReactionTypeEmoji,
    ReactionTypeCustomEmoji,
    ReactionTypePaid,
    ReactionCount
)
from .sponsored_message import SponsoredMessage
from .gift import Gift
from .upgraded_gift import UpgradedGift
from .sticker import Sticker
from .stripped_thumbnail import StrippedThumbnail
from .thumbnail import Thumbnail
from .venue import Venue
from .video import Video
from .video_quality import VideoQuality
from .video_note import VideoNote
from .voice import Voice
from .web_app_data import WebAppData
from .web_page import WebPage
from .message_reactions import MessageReactions
from .message_reaction_updated import MessageReactionUpdated
from .message_reaction_count_updated import MessageReactionCountUpdated
from .chat_boost_added import ChatBoostAdded
from .payment_form import PaymentForm
from .giveaway import Giveaway
from .giveaway_created import GiveawayCreated
from .giveaway_completed import GiveawayCompleted
from .giveaway_winners import GiveawayWinners
from .gift_code import GiftCode
from .gifted_premium import GiftedPremium
from .gifted_stars import GiftedStars
from .message_effect import MessageEffect
from .screenshot_taken import ScreenshotTaken
from .formatted_text import FormattedText
from .message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
from .write_access_allowed import WriteAccessAllowed
from .paid_message_price_changed import PaidMessagePriceChanged
from .paid_messages_refunded import PaidMessagesRefunded
from .checklist import Checklist
from .checklist_task import ChecklistTask
from .checklist_tasks_added import ChecklistTasksAdded
from .checklist_tasks_done import ChecklistTasksDone
from .direct_message_price_changed import DirectMessagePriceChanged
from .chat_owner_left import ChatOwnerLeft
from .chat_owner_changed import ChatOwnerChanged
from .chat_has_protected_content_toggled import ChatHasProtectedContentToggled
from .chat_has_protected_content_disable_requested import ChatHasProtectedContentDisableRequested
from .poll_option_added import PollOptionAdded
from .poll_option_deleted import PollOptionDeleted

from .gift_attribute import GiftAttribute
from .gift_auction import GiftAuction
from .gift_auction_state import GiftAuctionState
from .gift_collection import GiftCollection
from .gift_purchase_limit import GiftPurchaseLimit
from .gift_resale_parameters import GiftResaleParameters
from .gift_resale_price import GiftResalePrice
from .gift_upgrade_preview import GiftUpgradePreview
from .gift_upgrade_price import GiftUpgradePrice
from .gift_upgrade_variants import GiftUpgradeVariants
from .gifted_ton import GiftedTon
from .giveaway_prize_stars import GiveawayPrizeStars
from .my_boost import MyBoost
from .premium_gift_code import PremiumGiftCode
from .star_amount import StarAmount
from .boosts_status import BoostsStatus
from .chat_boost import ChatBoost
from .craft_gift_result import CraftGiftResult
from .upgraded_gift_attribute_id import UpgradedGiftAttributeId
from .upgraded_gift_attribute_id_backdrop import UpgradedGiftAttributeIdBackdrop
from .upgraded_gift_attribute_id_model import UpgradedGiftAttributeIdModel
from .upgraded_gift_attribute_id_symbol import UpgradedGiftAttributeIdSymbol
from .upgraded_gift_attribute_rarity import UpgradedGiftAttributeRarity
from .upgraded_gift_original_details import UpgradedGiftOriginalDetails
from .upgraded_gift_purchase_offer import UpgradedGiftPurchaseOffer
from .upgraded_gift_value_info import UpgradedGiftValueInfo

from .fact_check import FactCheck
from .live_photo import LivePhoto
from .mask_position import MaskPosition
from .paid_reactor import PaidReactor
from .rich_message import RichMessage
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

__all__ = [
    "Animation",
    "Audio",
    "ChatBoostAdded",
    "Contact",
    "ContactRegistered",
    "Dice",
    "Document",
    "Game",
    "PaymentForm",
    "GiftCode",
    "GiftedPremium",
    "GiftedStars",
    "Giveaway",
    "GiveawayCreated",
    "GiveawayCompleted",
    "GiveawayWinners",
    "ChatLocation",
    "Location",
    "Message",  # TODO
    "MessageAutoDeleteTimerChanged",
    "MessageEffect",
    "MessageEntity",
    "MessageReactionCountUpdated",
    "MessageReactionUpdated",
    "MessageReactions",
    "Photo",
    "Reaction",
    "ReactionCount",
    "ReactionType",
    "ReactionTypeEmoji",
    "ReactionTypeCustomEmoji",
    "ReactionTypePaid",
    "Thumbnail",
    "StrippedThumbnail",
    "Poll",
    "PollAnswer",
    "PollOption",
    "SponsoredMessage",
    "Gift",
    "UpgradedGift",
    "Sticker",
    "Venue",
    "Video",
    "VideoNote",
    "VideoQuality",
    "Voice",
    "WebAppData",
    "WebPage",
    "WriteAccessAllowed",
    "ScreenshotTaken",
    "FormattedText",
    "PaidMessagePriceChanged",
    "PaidMessagesRefunded",
    "Checklist",
    "ChecklistTask",
    "ChecklistTasksAdded",
    "ChecklistTasksDone",
    "DirectMessagePriceChanged",
    "DirectMessagesTopic",
    "ChatOwnerLeft",
    "ChatOwnerChanged",
    "ChatHasProtectedContentToggled",
    "ChatHasProtectedContentDisableRequested",
    "PollOptionAdded",
    "PollOptionDeleted",
    "GiftAttribute",
    "GiftAuction",
    "GiftAuctionState",
    "GiftCollection",
    "GiftPurchaseLimit",
    "GiftResaleParameters",
    "GiftResalePrice",
    "GiftUpgradePreview",
    "GiftUpgradePrice",
    "GiftUpgradeVariants",
    "GiftedTon",
    "GiveawayPrizeStars",
    "MyBoost",
    "PremiumGiftCode",
    "StarAmount",
    "BoostsStatus",
    "ChatBoost",
    "CraftGiftResult",
    "UpgradedGiftAttributeId",
    "UpgradedGiftAttributeIdBackdrop",
    "UpgradedGiftAttributeIdModel",
    "UpgradedGiftAttributeIdSymbol",
    "UpgradedGiftAttributeRarity",
    "UpgradedGiftOriginalDetails",
    "UpgradedGiftPurchaseOffer",
    "UpgradedGiftValueInfo",
    "FactCheck",
    "LivePhoto",
    "MaskPosition",
    "PaidReactor",
    "RichMessage",
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
]
