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


from .copy_media_group import CopyMediaGroup
from .copy_message import CopyMessage
from .delete_chat_history import DeleteChatHistory
from .delete_messages import DeleteMessages
from .download_media import DownloadMedia
from .edit_cached_media import EditCachedMedia
from .edit_inline_caption import EditInlineCaption
from .edit_inline_media import EditInlineMedia
from .edit_inline_reply_markup import EditInlineReplyMarkup
from .edit_inline_text import EditInlineText
from .edit_message_caption import EditMessageCaption
from .edit_message_media import EditMessageMedia
from .edit_message_reply_markup import EditMessageReplyMarkup
from .edit_message_text import EditMessageText
from .forward_media_group import ForwardMediaGroup
from .forward_messages import ForwardMessages
from .get_available_effects import GetAvailableEffects
from .get_chat_history import GetChatHistory
from .get_chat_history_count import GetChatHistoryCount
from .get_custom_emoji_stickers import GetCustomEmojiStickers
from .get_discussion_message import GetDiscussionMessage
from .get_discussion_replies import GetDiscussionReplies
from .get_discussion_replies_count import GetDiscussionRepliesCount
from .get_media_group import GetMediaGroup
from .get_message_read_participants import GetMessageReadParticipants
from .get_messages import GetMessages
from .get_scheduled_messages import GetScheduledMessages
from .read_chat_history import ReadChatHistory
from .retract_vote import RetractVote
from .search_global import SearchGlobal
from .search_global_count import SearchGlobalCount
from .search_global_hashtag_messages import SearchGlobalHashtagMessages
from .search_global_hashtag_messages_count import SearchGlobalHashtagMessagesCount
from .search_messages import SearchMessages
from .search_messages_count import SearchMessagesCount
from .search_posts import SearchPosts
from .search_posts_count import SearchPostsCount
from .send_animation import SendAnimation
from .send_audio import SendAudio
from .send_cached_media import SendCachedMedia
from .send_chat_action import SendChatAction
from .send_contact import SendContact
from .send_dice import SendDice
from .send_document import SendDocument
from .send_invoice import SendInvoice
from .send_location import SendLocation
from .send_media_group import SendMediaGroup
from .send_message import SendMessage
from .send_paid_media import SendPaidMedia
from .send_photo import SendPhoto
from .send_poll import SendPoll
from .add_paid_message_reaction import AddPaidMessageReaction
from .send_reaction import SendReaction
from .set_reaction import SetReaction
from .send_sticker import SendSticker
from .send_venue import SendVenue
from .send_video import SendVideo
from .send_video_note import SendVideoNote
from .send_voice import SendVoice
from .send_web_page import SendWebPage
from .start_bot import StartBot
from .stop_poll import StopPoll
from .stream_media import StreamMedia
from .transcribe_audio import TranscribeAudio
from .view_messages import ViewMessages
from .vote_poll import VotePoll
from .get_chat_sponsored_messages import GetChatSponsoredMessages
from .search_public_messages_by_tag import SearchPublicMessagesByTag
from .count_public_messages_by_tag import CountPublicMessagesByTag
from .translate_text import TranslateText
from .send_screenshot_notification import SendScreenshotNotification
from .send_checklist import SendChecklist
from .edit_message_checklist import EditMessageChecklist
from .mark_checklist_tasks_as_done import MarkChecklistTasksAsDone
from .add_poll_option import AddPollOption
from .delete_poll_option import DeletePollOption
from .approve_suggested_post import ApproveSuggestedPost
from .decline_suggested_post import DeclineSuggestedPost
from .add_to_gifs import AddToGifs
from .read_mentions import ReadMentions
from .read_reactions import ReadReactions
from .summarize_message import SummarizeMessage
from .compose_text_with_ai import ComposeTextWithAI
from .fix_text_with_ai import FixTextWithAI
from .get_main_web_app import GetMainWebApp
from .get_web_app_url import GetWebAppUrl
from .get_web_app_link_url import GetWebAppLinkUrl
from .open_web_app import OpenWebApp
from .get_direct_messages_chat_topic_history import GetDirectMessagesChatTopicHistory
from .delete_direct_messages_chat_topic_history import DeleteDirectMessagesChatTopicHistory
from .set_direct_messages_chat_topic_is_marked_as_unread import SetDirectMessagesChatTopicIsMarkedAsUnread
from .get_user_personal_chat_messages import GetUserPersonalChatMessages
from .send_live_photo import SendLivePhoto
from .send_rich_message import SendRichMessage
from .send_rich_message_draft import SendRichMessageDraft


class Messages(
    CopyMediaGroup,
    CopyMessage,
    DeleteChatHistory,
    DeleteMessages,
    DownloadMedia,
    EditCachedMedia,
    EditInlineCaption,
    EditInlineMedia,
    EditInlineReplyMarkup,
    EditInlineText,
    EditMessageCaption,
    EditMessageMedia,
    EditMessageReplyMarkup,
    EditMessageText,
    ForwardMediaGroup,
    ForwardMessages,
    GetAvailableEffects,
    GetChatHistory,
    GetChatHistoryCount,
    GetCustomEmojiStickers,
    GetDiscussionMessage,
    GetDiscussionReplies,
    GetDiscussionRepliesCount,
    GetMediaGroup,
    GetMessageReadParticipants,
    GetMessages,
    GetScheduledMessages,
    ReadChatHistory,
    RetractVote,
    SearchGlobal,
    SearchGlobalCount,
    SearchGlobalHashtagMessages,
    SearchGlobalHashtagMessagesCount,
    SearchMessages,
    SearchMessagesCount,
    SearchPosts,
    SearchPostsCount,
    SendAnimation,
    SendAudio,
    SendCachedMedia,
    SendChatAction,
    SendContact,
    SendDice,
    SendDocument,
    SendInvoice,
    SendLocation,
    SendMediaGroup,
    SendMessage,
    SendPaidMedia,
    SendPhoto,
    SendPoll,
    AddPaidMessageReaction,
    SendReaction,
    SetReaction,
    SendSticker,
    SendVenue,
    SendVideo,
    SendVideoNote,
    SendVoice,
    SendWebPage,
    StartBot,
    StopPoll,
    StreamMedia,
    TranscribeAudio,
    ViewMessages,
    VotePoll,
    GetChatSponsoredMessages,
    SearchPublicMessagesByTag,
    CountPublicMessagesByTag,
    TranslateText,
    SendScreenshotNotification,
    SendChecklist,
    EditMessageChecklist,
    MarkChecklistTasksAsDone,
    AddPollOption,
    DeletePollOption,
    ApproveSuggestedPost,
    DeclineSuggestedPost,
    AddToGifs,
    ReadMentions,
    ReadReactions,
    SummarizeMessage,
    ComposeTextWithAI,
    FixTextWithAI,
    GetMainWebApp,
    GetWebAppUrl,
    GetWebAppLinkUrl,
    OpenWebApp,
    GetDirectMessagesChatTopicHistory,
    DeleteDirectMessagesChatTopicHistory,
    SetDirectMessagesChatTopicIsMarkedAsUnread,
    GetUserPersonalChatMessages,
    SendLivePhoto,
    SendRichMessage,
    SendRichMessageDraft,
):
    pass
