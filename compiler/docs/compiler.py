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

import ast
import os
import re
import shutil

HOME = "compiler/docs"
DESTINATION = "docs/source/telegram"
PYROGRAM_API_DEST = "docs/source/api"

FUNCTIONS_PATH = "pyrogram/raw/functions"
TYPES_PATH = "pyrogram/raw/types"
BASE_PATH = "pyrogram/raw/base"

FUNCTIONS_BASE = "functions"
TYPES_BASE = "types"
BASE_BASE = "base"


def snek(s: str):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def generate(source_path, base):
    all_entities = {}

    def build(path, level=0):
        last = path.split("/")[-1]

        for i in os.listdir(path):
            try:
                if not i.startswith("__"):
                    build("/".join([path, i]), level=level + 1)
            except NotADirectoryError:
                with open(path + "/" + i, encoding="utf-8") as f:
                    p = ast.parse(f.read())

                for node in ast.walk(p):
                    if isinstance(node, ast.ClassDef):
                        name = node.name
                        break
                else:
                    continue

                full_path = (
                    os.path.basename(path) + "/" + snek(name).replace("_", "-") + ".rst"
                )

                if level:
                    full_path = base + "/" + full_path

                namespace = path.split("/")[-1]
                if namespace in ["base", "types", "functions"]:
                    namespace = ""

                full_name = f"{(namespace + '.') if namespace else ''}{name}"

                os.makedirs(
                    os.path.dirname(DESTINATION + "/" + full_path), exist_ok=True
                )

                with open(DESTINATION + "/" + full_path, "w", encoding="utf-8") as f:
                    f.write(
                        page_template.format(
                            title=full_name,
                            title_markup="=" * len(full_name),
                            full_class_path="pyrogram.raw.{}".format(
                                ".".join(full_path.split("/")[:-1]) + "." + name
                            ),
                        )
                    )

                if last not in all_entities:
                    all_entities[last] = []

                all_entities[last].append(name)

    build(source_path)

    for k, v in sorted(all_entities.items()):
        v = sorted(v)
        entities = []

        for i in v:
            entities.append(f'{i} <{snek(i).replace("_", "-")}>')

        if k != base:
            inner_path = base + "/" + k + "/index" + ".rst"
            module = "pyrogram.raw.{}.{}".format(base, k)
        else:
            for i in sorted(list(all_entities), reverse=True):
                if i != base:
                    entities.insert(0, "{0}/index".format(i))

            inner_path = base + "/index" + ".rst"
            module = "pyrogram.raw.{}".format(base)

        with open(DESTINATION + "/" + inner_path, "w", encoding="utf-8") as f:
            if k == base:
                f.write(":tocdepth: 1\n\n")
                k = "Raw " + k

            f.write(
                toctree.format(
                    title=k.title(),
                    title_markup="=" * len(k),
                    module=module,
                    entities="\n    ".join(entities),
                )
            )

            f.write("\n")


def pyrogram_api():
    def get_title_list(s: str) -> list:
        return [i.strip() for i in [j.strip() for j in s.split("\n") if j] if i]

    # Methods

    categories = dict(
        utilities="""
        Utilities
            start
            stop
            run
            run_sync
            restart
            add_handler
            remove_handler
            stop_transmission
            export_session_string
            set_parse_mode
            ping
        """,
        conversation="""
        Conversation
            ask
            listen
            get_listener_matching_with_data
            get_listener_matching_with_identifier_pattern
            get_many_listeners_matching_with_data
            get_many_listeners_matching_with_identifier_pattern
            register_next_step_handler
            remove_listener
            stop_listener
            stop_listening
            wait_for_callback_query
            wait_for_message
        """,
        messages="""
        Messages
            send_message
            forward_media_group
            forward_messages
            copy_message
            copy_media_group
            send_paid_media
            send_photo
            send_audio
            send_document
            send_invoice
            send_sticker
            send_video
            send_animation
            send_voice
            send_video_note
            send_web_page
            start_bot
            send_media_group
            send_location
            send_venue
            send_contact
            send_cached_media
            send_reaction
            edit_message_text
            edit_message_caption
            edit_message_media
            edit_message_reply_markup
            edit_inline_text
            edit_inline_caption
            edit_inline_media
            edit_inline_reply_markup
            send_chat_action
            send_checklist
            delete_messages
            get_available_effects
            get_messages
            get_message_read_participants
            get_scheduled_messages
            get_stickers
            mark_checklist_tasks_as_done
            get_media_group
            get_chat_history
            get_chat_history_count
            read_chat_history
            send_poll
            view_messages
            vote_poll
            stop_poll
            retract_vote
            send_dice
            search_messages
            search_messages_count
            search_posts
            search_posts_count
            search_global
            search_global_count
            search_global_hashtag_messages
            search_global_hashtag_messages_count
            download_media
            stream_media
            get_discussion_message
            get_discussion_replies
            get_discussion_replies_count
            get_custom_emoji_stickers
            delete_chat_history
            transcribe_audio
            translate_message_text
            translate_text
            delete_chat_history
            add_checklist_tasks
            add_paid_message_reaction
            add_poll_option
            count_public_messages_by_tag
            delete_poll_option
            edit_cached_media
            edit_message_checklist
            get_chat_sponsored_messages
            search_public_messages_by_tag
            send_screenshot_notification
            set_reaction
        """,
        chats="""
        Chats
            join_chat
            leave_chat
            ban_chat_member
            unban_chat_member
            restrict_chat_member
            promote_chat_member
            set_administrator_title
            set_chat_photo
            delete_chat_photo
            delete_folder
            export_folder_link
            update_folder
            set_chat_title
            set_chat_description
            set_chat_permissions
            pin_chat_message
            unpin_chat_message
            unpin_all_chat_messages
            get_chat
            get_chat_member
            get_chat_members
            get_chat_members_count
            get_dialogs
            get_dialogs_count
            get_folders
            get_forum_topics
            get_forum_topics_by_id
            get_forum_topics_count
            set_chat_username
            archive_chats
            unarchive_chats
            add_chat_members
            create_channel
            create_group
            create_supergroup
            delete_channel
            delete_supergroup
            delete_user_history
            set_slow_mode
            mark_chat_unread
            get_chat_event_log
            get_chat_online_count
            get_send_as_chats
            set_send_as_chat
            set_chat_protected_content
            close_forum_topic
            close_general_topic
            create_forum_topic
            delete_forum_topic
            edit_forum_topic
            edit_general_topic
            hide_general_topic
            reopen_forum_topic
            reopen_general_topic
            unhide_general_topic
            join_folder
            leave_folder
            update_color
            update_folder
            get_forum_topic
            get_forum_topic_icon_stickers
            hide_forum_topic
            toggle_forum_topic_is_pinned
            unhide_forum_topic
            get_chat_audios
            get_chat_audios_count
            get_created_chats
            get_direct_messages_topics
            get_direct_messages_topics_by_id
            get_nearby_chats
            search_chats
            set_chat_direct_messages_group
            set_chat_message_auto_delete_time
            transfer_chat_ownership
        """,
        users="""
        Users
            get_me
            get_users
            get_chat_photos
            get_chat_photos_count
            set_profile_photo
            delete_profile_photos
            set_username
            set_birthdate
            set_personal_chat
            update_birthday
            update_personal_chat
            update_profile
            update_status
            block_user
            unblock_user
            get_common_chats
            get_default_emoji_statuses
            set_emoji_status
            delete_account
        """,
        stories="""
        Stories
            can_post_stories
            can_post_story
            copy_story
            delete_stories
            edit_story
            edit_story_caption
            edit_story_media
            edit_story_privacy
            enable_stealth_mode
            export_story_link
            forward_story
            get_all_stories
            get_archived_stories
            get_chat_active_stories
            get_chat_archived_stories
            get_chat_stories
            get_peer_stories
            get_pinned_stories
            get_stories
            get_stories_history
            get_story_views
            hide_chat_stories
            hide_my_story_view
            pin_chat_stories
            post_story
            read_chat_stories
            send_story
            show_chat_stories
            toggle_story_is_posted_to_chat_page
            unpin_chat_stories
            view_stories
        """,
        stickers="""
        Stickers
            add_sticker_to_set
            create_sticker_set
            get_sticker_set
        """,
        invite_links="""
        Invite Links
            get_chat_invite_link
            export_chat_invite_link
            create_chat_invite_link
            edit_chat_invite_link
            revoke_chat_invite_link
            delete_chat_invite_link
            get_chat_invite_link_joiners
            get_chat_invite_link_joiners_count
            get_chat_admin_invite_links
            get_chat_admin_invite_links_count
            get_chat_admins_with_invite_links
            get_chat_join_requests
            delete_chat_admin_invite_links
            approve_chat_join_request
            approve_all_chat_join_requests
            decline_chat_join_request
            decline_all_chat_join_requests
            check_chat_folder_invite_link
        """,
        contacts="""
        Contacts
            add_contact
            delete_contacts
            import_contacts
            get_contacts
            get_contacts_count
            search_contacts
        """,
        payments="""
        Payments
            add_collection_gifts
            apply_gift_code
            buy_gift_upgrade
            check_gift_code
            convert_gift_to_stars
            craft_gift
            create_gift_collection
            delete_gift_collection
            drop_gift_original_details
            edit_star_subscription
            get_available_gifts
            get_chat_gifts
            get_chat_gifts_count
            get_gift_auction_state
            get_gift_collections
            get_gift_upgrade_preview
            get_gift_upgrade_variants
            get_gifts_for_crafting
            get_payment_form
            get_stars_balance
            get_ton_balance
            get_upgraded_gift
            get_upgraded_gift_value_info
            gift_premium_with_stars
            hide_gift
            increase_gift_auction_bid
            place_gift_auction_bid
            process_gift_purchase_offer
            remove_collection_gifts
            reorder_collection_gifts
            reorder_gift_collections
            reuse_star_subscription
            search_gifts_for_resale
            send_gift
            send_gift_purchase_offer
            send_payment_form
            send_resold_gift
            set_gift_collection_name
            set_gift_resale_price
            set_pinned_gifts
            show_gift
            suggest_birthday
            transfer_gift
            upgrade_gift
        """,
        premium="""
        Premium
            apply_boost
            get_boosts
            get_boosts_status
        """,
        phone="""
        Phone
            create_video_chat
            discard_group_call
            get_video_chat_rtmp_url
            invite_group_call_participants
            load_group_call_participants
        """,
        password="""
        Password
            enable_cloud_password
            change_cloud_password
            remove_cloud_password
        """,
        bots="""
        Bots
            get_inline_bot_results
            send_inline_bot_result
            answer_callback_query
            answer_inline_query
            request_callback_answer
            send_game
            set_game_score
            get_game_high_scores
            set_bot_commands
            get_bot_commands
            delete_bot_commands
            set_bot_default_privileges
            get_bot_default_privileges
            set_chat_menu_button
            get_chat_menu_button
            answer_web_app_query
            answer_pre_checkout_query
            answer_shipping_query
            refund_star_payment
            get_bot_info
            set_bot_info
            get_bot_info_description
            set_bot_info_description
            get_bot_info_short_description
            set_bot_info_short_description
            get_bot_name
            set_bot_name
            get_collectible_item_info
            get_owned_bots
            get_similar_bots
            send_message_draft
            send_web_app_custom_request
        """,
        business="""
        Business
            create_business_chat_link
            create_invoice_link
            delete_business_chat_link
            delete_business_messages
            get_business_account_gifts
            get_business_account_star_balance
            get_business_chat_links
            get_business_connection
            get_connected_bots
            get_owned_star_count
            resolve_business_chat_link
            transfer_business_account_stars
            update_business_away_message
            update_business_greeting_message
            update_business_intro
            update_business_location
            update_business_work_hours
        """,
        authorization="""
        Authorization
            connect
            disconnect
            initialize
            terminate
            send_code
            resend_code
            sign_in
            sign_in_bot
            sign_in_qrcode
            sign_up
            get_password_hint
            check_password
            send_recovery_code
            recover_password
            accept_terms_of_service
            log_out
            get_active_sessions
            reset_session
            reset_sessions
        """,
        advanced="""
        Advanced
            invoke
            recover_gaps
            resolve_peer
            save_file
        """,
        account="""
        Account
            add_profile_audio
            get_account_ttl
            get_global_privacy_settings
            get_privacy
            remove_profile_audio
            set_account_ttl
            set_global_privacy_settings
            set_inactive_session_ttl
            set_privacy
            set_profile_audio_position
        """,
    )

    root = PYROGRAM_API_DEST + "/methods"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/methods.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            _, *methods = get_title_list(v)
            fmt_keys.update({k: "\n    ".join("{0} <{0}>".format(m) for m in methods)})

            for method in methods:
                with open(root + "/{}.rst".format(method), "w") as f2:
                    title = "{}()".format(method)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. automethod:: pyrogram.Client.{}()".format(method))

            functions = ["idle", "compose"]

            for func in functions:
                with open(root + "/{}.rst".format(func), "w") as f2:
                    title = "{}()".format(func)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. autofunction:: pyrogram.{}()".format(func))

        f.write(template.format(**fmt_keys))

    # Types

    categories = dict(
        users_chats="""
        Users & Chats
            Birthday
            BusinessInfo
            BusinessMessage
            BusinessRecipients
            BusinessWeeklyOpen
            BusinessWorkingHours
            User
            Username
            Chat
            ChatPreview
            ChatPhoto
            ChatMember
            ChatPermissions
            ChatPrivileges
            ChatInviteLink
            ChatAdminWithInviteLinks
            ChatEvent
            ChatEventFilter
            ChatMemberUpdated
            ChatJoinRequest
            ChatJoinedByRequest
            ChatJoiner
            Dialog
            Folder
            Restriction
            EmojiStatus
            ForumTopic
            PeerUser
            PeerChannel
            BotInfo
            GroupCallMember
            ChatColor
            CollectibleItemInfo
            FoundContacts
            PrivacyRule
        """,
        messages_media="""
        Messages & Media
            Message
            MessageEntity
            MessageOriginChannel
            MessageOriginChat
            MessageOriginHiddenUser
            MessageOriginImport
            MessageOriginUser
            MessageOrigin
            Photo
            Thumbnail
            Audio
            AvailableEffect
            Document
            ExternalReplyInfo
            AlternativeVideo
            Animation
            LabeledPrice
            Video
            Voice
            VideoNote
            Contact
            Location
            Venue
            Sticker
            StickerSet
            Game
            Giveaway
            GiveawayLaunched
            GiveawayResult
            MessageInvoice
            MessageStory
            WebPage
            WebPageEmpty
            WebPagePreview
            TranscribedAudio
            TranslatedText
            TextQuote
            Poll
            PollOption
            Dice
            Reaction
            VideoChatScheduled
            VideoChatStarted
            VideoChatEnded
            VideoChatMembersInvited
            WebAppData
            MessageReactions
            MessageReactor
            ChatReactions
            ForumTopicCreated
            ForumTopicEdited
            ForumTopicClosed
            ForumTopicDeleted
            ForumTopicReopened
            GeneralTopicHidden
            GeneralTopicUnhidden
            Reaction
            ReactionCount
            ReactionType
            MessageReactionUpdated
            MessageReactionCountUpdated
            InputChecklistTask
            CheckedGiftCode
            ChecklistTask
            ChecklistTasksAdded
            ChecklistTasksDone
            Checklist
            SuccessfulPayment
            ExtendedMediaPreview
            PaidMedia
            PaymentForm
            ReadParticipant
            AcceptedGiftTypes
            CraftGiftResult
            Gift
            GiftAttribute
            GiftAuction
            GiftAuctionState
            GiftCode
            GiftCollection
            GiftPurchaseLimit
            GiftResaleParameters
            GiftResalePrice
            GiftUpgradePreview
            GiftUpgradePrice
            GiftUpgradeVariants
            GiftedPremium
            GiftedStars
            GiftedTon
            PremiumGiftCode
            StarAmount
            UpgradedGift
            UpgradedGiftAttributeId
            UpgradedGiftAttributeIdBackdrop
            UpgradedGiftAttributeIdModel
            UpgradedGiftAttributeIdSymbol
            UpgradedGiftAttributeRarity
            UpgradedGiftOriginalDetails
            UpgradedGiftPurchaseOffer
            UpgradedGiftValueInfo
            BoostsStatus
            ChatBoost
            ChatBoostAdded
            MyBoost
        """,
        stories="""
        Stories
            Story
            StoryDeleted
            StoryForwardHeader
            StorySkipped
            StoriesPrivacyRules
            StoryViews
            MediaArea
            MediaAreaChannelPost
            MediaAreaCoordinates
            InputMediaArea
            InputMediaAreaChannelPost
            StoryAreaTypeUniqueGift
            CanPostStoryResultBoostNeeded
        """,
        pyromod="""
        Pyromod
            Identifier
            Listener
        """,
        bot="""
        Bot
            BotAllowed
            BotApp
            BotBusinessConnection
            PaymentInfo
            PaymentRefunded
            ShippingAddress
            SuccessfulPayment
        """,
        bot_keyboards="""
        Bot keyboards
            BotBusinessConnection
            ReplyKeyboardMarkup
            KeyboardButton
            ReplyKeyboardRemove
            InlineKeyboardMarkup
            InlineKeyboardButton
            InlineKeyboardButtonBuy
            RequestPeerTypeChannel
            RequestPeerTypeChat
            RequestPeerTypeUser
            LoginUrl
            ForceReply
            CallbackQuery
            GameHighScore
            CallbackGame
            WebAppInfo
            MenuButton
            MenuButtonCommands
            MenuButtonWebApp
            MenuButtonDefault
            SentWebAppMessage
            PaymentInfo
            PreCheckoutQuery
            ShippingAddress
        """,
        bot_commands="""
        Bot commands
            BotCommand
            BotCommandScope
            BotCommandScopeDefault
            BotCommandScopeAllPrivateChats
            BotCommandScopeAllGroupChats
            BotCommandScopeAllChatAdministrators
            BotCommandScopeChat
            BotCommandScopeChatAdministrators
            BotCommandScopeChatMember
        """,
        input_media="""
        Input Media
            InputMedia
            InputMediaPhoto
            InputMediaVideo
            InputMediaAudio
            InputMediaAnimation
            InputMediaDocument
            InputPhoneContact
        """,
        inline_mode="""
        Inline Mode
            InlineQuery
            InlineQueryResult
            InlineQueryResultCachedAudio
            InlineQueryResultCachedDocument
            InlineQueryResultCachedAnimation
            InlineQueryResultCachedPhoto
            InlineQueryResultCachedSticker
            InlineQueryResultCachedVideo
            InlineQueryResultCachedVoice
            InlineQueryResultArticle
            InlineQueryResultAudio
            InlineQueryResultContact
            InlineQueryResultDocument
            InlineQueryResultAnimation
            InlineQueryResultLocation
            InlineQueryResultPhoto
            InlineQueryResultVenue
            InlineQueryResultVideo
            InlineQueryResultVoice
            ChosenInlineResult
        """,
        pre_checkout_query="""
        PreCheckoutQuery
            PreCheckoutQuery.answer
        """,
        input_message_content="""
        InputMessageContent
            InputMessageContent
            InputReplyToMessage
            InputReplyToMonoforum
            InputReplyToStory
            InputTextMessageContent
            InputLocationMessageContent
            InputVenueMessageContent
            InputContactMessageContent
            InputInvoiceMessageContent
        """,
        authorization="""
        Authorization
            ActiveSession
            ActiveSessions
            LoginToken
            SentCode
            TermsOfService
        """,
        input_privacy_rule="""
        InputPrivacyRule
            InputPrivacyRuleAllowAll
            InputPrivacyRuleAllowContacts
            InputPrivacyRuleAllowPremium
            InputPrivacyRuleAllowUsers
            InputPrivacyRuleAllowChats
            InputPrivacyRuleDisallowAll
            InputPrivacyRuleDisallowContacts
            InputPrivacyRuleDisallowUsers
            InputPrivacyRuleDisallowChats
        """,
    )

    root = PYROGRAM_API_DEST + "/types"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/types.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            _, *types = get_title_list(v)

            fmt_keys.update({k: "\n    ".join(types)})

            # noinspection PyShadowingBuiltins
            for type in types:
                with open(root + "/{}.rst".format(type), "w") as f2:
                    title = "{}".format(type)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. autoclass:: pyrogram.types.{}()\n".format(type))

        f.write(template.format(**fmt_keys))

    # Bound Methods

    categories = dict(
        message="""
        Message
            Message.ask
            Message.click
            Message.delete
            Message.download
            Message.forward
            Message.copy
            Message.pin
            Message.unpin
            Message.edit
            Message.edit_text
            Message.edit_caption
            Message.edit_media
            Message.edit_reply_markup
            Message.reply
            Message.reply_text
            Message.reply_animation
            Message.reply_audio
            Message.reply_cached_media
            Message.reply_chat_action
            Message.reply_contact
            Message.reply_document
            Message.reply_game
            Message.reply_inline_bot_result
            Message.reply_location
            Message.reply_media_group
            Message.reply_photo
            Message.reply_poll
            Message.reply_sticker
            Message.reply_venue
            Message.reply_video
            Message.reply_video_note
            Message.reply_voice
            Message.reply_web_page
            Message.reply_checklist
            Message.get_media_group
            Message.react
            Message.transcribe
            Message.translate
            Message.wait_for_click
            Message.read
            Message.view
            Message.pay
        """,
        chat="""
        Chat
            Chat.ask
            Chat.listen
            Chat.stop_listening
            Chat.archive
            Chat.unarchive
            Chat.set_title
            Chat.set_description
            Chat.set_photo
            Chat.ban_member
            Chat.unban_member
            Chat.restrict_member
            Chat.promote_member
            Chat.get_member
            Chat.get_members
            Chat.add_members
            Chat.join
            Chat.leave
            Chat.mark_unread
            Chat.set_protected_content
            Chat.unpin_all_messages
        """,
        user="""
        User
            User.ask
            User.listen
            User.stop_listening
            User.archive
            User.unarchive
            User.block
            User.unblock
        """,
        story="""
        Story
            Story.delete
            Story.download
            Story.edit
            Story.edit_animation
            Story.edit_caption
            Story.edit_photo
            Story.edit_privacy
            Story.edit_video
            Story.export_link
            Story.forward
            Story.reply_text
            Story.reply_animation
            Story.reply_audio
            Story.reply_cached_media
            Story.reply_media_group
            Story.reply_photo
            Story.reply_sticker
            Story.reply_video
            Story.reply_video_note
            Story.reply_voice
        """,
        callback_query="""
        Callback Query
            CallbackQuery.answer
            CallbackQuery.edit_message_text
            CallbackQuery.edit_message_caption
            CallbackQuery.edit_message_media
            CallbackQuery.edit_message_reply_markup
        """,
        inline_query="""
        InlineQuery
            InlineQuery.answer
        """,
        pre_checkout_query="""
        PreCheckoutQuery
            PreCheckoutQuery.answer
        """,
        chat_join_request="""
        ChatJoinRequest
            ChatJoinRequest.approve
            ChatJoinRequest.decline
        """,
        folder="""
        Folder
            Folder.delete
            Folder.edit
            Folder.include_chat
            Folder.exclude_chat
            Folder.pin_chat
            Folder.remove_chat
            Folder.update_color
            Folder.create_invite_link
        """,
        active_session="""
        ActiveSession
            ActiveSession.reset
        """,
    )

    root = PYROGRAM_API_DEST + "/bound-methods"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/bound-methods.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *bound_methods = get_title_list(v)

            fmt_keys.update(
                {
                    "{}_hlist".format(k): "\n    ".join(
                        "- :meth:`~{}`".format(bm) for bm in bound_methods
                    )
                }
            )

            fmt_keys.update(
                {
                    "{}_toctree".format(k): "\n    ".join(
                        "{} <{}>".format(bm.split(".")[1], bm) for bm in bound_methods
                    )
                }
            )

            # noinspection PyShadowingBuiltins
            for bm in bound_methods:
                with open(root + "/{}.rst".format(bm), "w") as f2:
                    title = "{}()".format(bm)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. automethod:: pyrogram.types.{}()".format(bm))

        f.write(template.format(**fmt_keys))


page_template = None
toctree = None


def start():
    global page_template
    global toctree

    shutil.rmtree(DESTINATION, ignore_errors=True)

    with open(HOME + "/template/page.txt", encoding="utf-8") as f:
        page_template = f.read()

    with open(HOME + "/template/toctree.txt", encoding="utf-8") as f:
        toctree = f.read()

    generate(TYPES_PATH, TYPES_BASE)
    generate(FUNCTIONS_PATH, FUNCTIONS_BASE)
    generate(BASE_PATH, BASE_BASE)
    pyrogram_api()


if "__main__" == __name__:
    FUNCTIONS_PATH = "../../pyrogram/raw/functions"
    TYPES_PATH = "../../pyrogram/raw/types"
    BASE_PATH = "../../pyrogram/raw/base"
    HOME = "."
    DESTINATION = "../../docs/source/telegram"
    PYROGRAM_API_DEST = "../../docs/source/api"

    start()