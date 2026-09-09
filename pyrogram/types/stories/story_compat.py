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

"""pyroblack <= 2.7.6 surface for :class:`~pyrogram.types.Story`.

The rebase replaced ``pyrogram.types.messages_and_media.story.Story`` with the
Bot-API-shaped ``pyrogram.types.stories.story.Story``. The new class dropped
nineteen bound methods (``reply_*``, ``edit_*``, ``delete``, ``forward``,
``export_link``) and renamed most attributes, so every v2.7.6 application that
touched a story broke.

:class:`LegacyStoryMixin` puts that surface back on top of the current class.
Attributes are read-only properties derived from the new fields, and the bound
methods delegate to the current ``Client`` methods, so there is one
implementation of each operation rather than two.

Known limitations, all documented on the members themselves:

* ``media_areas`` yields :class:`~pyrogram.types.StoryArea` objects rather than
  the old :class:`~pyrogram.types.MediaArea` ones — the server field was
  restructured, not just renamed.
* ``from_user`` / ``sender_chat`` both yield a :class:`~pyrogram.types.Chat`.
  ``.id``, ``.username``, ``.first_name`` and ``.last_name`` resolve as before,
  but ``User``-only fields (``is_premium``, ``status``, …) do not.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO

from pyrogram import enums, raw, types

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime


def _legacy_privacy_settings(
    privacy: enums.StoriesPrivacyRules | enums.StoryPrivacy | None,
    allowed_users: list[int | str] | None,
    denied_users: list[int | str] | None,
    *,
    public: bool | None = None,
    contacts: bool | None = None,
    close_friends: bool | None = None,
    selected_contacts: bool | None = None,
) -> types.StoryPrivacySettings | None:
    """Translate the v2.7.6 privacy fields into a :class:`StoryPrivacySettings`.

    v2.7.6 described story privacy two ways: an enum plus two flat user lists
    (``send_story``/``edit_story``), and four booleans on the parsed ``Story``.
    The current API models both as one of four ``StoryPrivacySettings*`` objects.
    """
    if close_friends:
        return types.StoryPrivacySettingsCloseFriends()
    if contacts:
        return types.StoryPrivacySettingsContacts(except_user_ids=denied_users or None)
    if selected_contacts:
        return types.StoryPrivacySettingsSelectedUsers(user_ids=allowed_users or None)
    if public:
        return types.StoryPrivacySettingsEveryone(except_user_ids=denied_users or None)

    if privacy is None and not allowed_users and not denied_users:
        return None

    name = getattr(privacy, "name", None)

    if name == "CLOSE_FRIENDS":
        return types.StoryPrivacySettingsCloseFriends()
    if name == "CONTACTS":
        return types.StoryPrivacySettingsContacts(except_user_ids=denied_users or None)
    if name in ("PRIVATE", "SELECTED_USERS"):
        return types.StoryPrivacySettingsSelectedUsers(user_ids=allowed_users or None)
    if name == "NO_CONTACTS":
        # v2.7.6 mapped NO_CONTACTS onto "everyone except my contacts". There is
        # no single settings object for that, so fall back to the closest one:
        # everyone, minus whoever was explicitly denied.
        return types.StoryPrivacySettingsEveryone(except_user_ids=denied_users or None)

    # PUBLIC and the "only lists given" case
    return types.StoryPrivacySettingsEveryone(except_user_ids=denied_users or None)


def _legacy_content(
    animation: str | BinaryIO | None = None,
    photo: str | BinaryIO | None = None,
    video: str | BinaryIO | None = None,
) -> types.InputStoryContent | None:
    """Translate the v2.7.6 ``animation``/``photo``/``video`` trio into content.

    ``edit_story`` used to take the three media kinds as separate keyword
    arguments; it now takes a single :class:`InputStoryContent`.
    """
    if photo is not None:
        return types.InputStoryContentPhoto(photo=photo)
    if video is not None:
        return types.InputStoryContentVideo(video=video)
    if animation is not None:
        # A v2.7.6 story "animation" is a soundless MP4, which is what
        # InputStoryContentVideo(is_animation=True) describes.
        return types.InputStoryContentVideo(video=animation, is_animation=True)
    return None


class LegacyStoryMixin:
    """The v2.7.6 ``Story`` attributes and bound methods."""

    # ------------------------------------------------------------------
    # Attributes
    # ------------------------------------------------------------------

    @property
    def raw(self):
        """Deprecated alias of ``_raw``."""
        return self._raw

    @property
    def from_user(self) -> types.Chat | None:
        """Poster of the story, when it is a user.

        v2.7.6 exposed a :obj:`~pyrogram.types.User` here. The current class
        keeps a single :attr:`chat` for both cases, so this returns that
        ``Chat``: ``.id``/``.username``/``.first_name``/``.last_name`` behave as
        before, ``User``-only fields do not exist.
        """
        if self.chat is not None and self.chat.type in (
            enums.ChatType.PRIVATE,
            enums.ChatType.BOT,
        ):
            return self.chat
        return None

    @property
    def sender_chat(self) -> types.Chat | None:
        """Poster of the story, when it is a group or channel."""
        if self.chat is not None and self.chat.type not in (
            enums.ChatType.PRIVATE,
            enums.ChatType.BOT,
        ):
            return self.chat
        return None

    @property
    def media_areas(self) -> list[types.StoryArea] | None:
        """Deprecated alias of :attr:`areas`.

        Note the element type changed from :obj:`~pyrogram.types.MediaArea` to
        :obj:`~pyrogram.types.StoryArea` along with the server field.
        """
        return self.areas

    @property
    def animation(self) -> types.Animation | None:
        """Story animation, when the media is a soundless MP4.

        The current parser routes every document story into :attr:`video`; this
        re-reads the raw story item to tell an animation apart, matching what
        v2.7.6 reported.
        """
        media = getattr(self._raw, "media", None)
        if not isinstance(media, raw.types.MessageMediaDocument):
            return None

        document = getattr(media, "document", None)
        if document is None:
            return None

        attributes = {type(i): i for i in document.attributes}
        if raw.types.DocumentAttributeAnimated not in attributes:
            return None

        return types.Animation._parse(
            self._client,
            document,
            attributes.get(raw.types.DocumentAttributeVideo),
            None,
        )

    @property
    def forward_from(self) -> types.StoryRepostInfo | None:
        """Deprecated alias of :attr:`repost_info`."""
        return self.repost_info

    @property
    def privacy(self) -> enums.StoryPrivacy | None:
        """Story privacy as the v2.7.6 :obj:`~pyrogram.enums.StoryPrivacy` enum."""
        settings = self.privacy_settings
        if settings is None:
            return None
        if isinstance(settings, types.StoryPrivacySettingsCloseFriends):
            return enums.StoryPrivacy.CLOSE_FRIENDS
        if isinstance(settings, types.StoryPrivacySettingsContacts):
            return enums.StoryPrivacy.CONTACTS
        if isinstance(settings, types.StoryPrivacySettingsSelectedUsers):
            return enums.StoryPrivacy.PRIVATE
        return enums.StoryPrivacy.PUBLIC

    @property
    def public(self) -> bool | None:
        """Whether the story is visible to everyone."""
        if self.privacy_settings is None:
            return None
        return isinstance(self.privacy_settings, types.StoryPrivacySettingsEveryone)

    @property
    def contacts(self) -> bool | None:
        """Whether the story is visible to contacts only."""
        if self.privacy_settings is None:
            return None
        return isinstance(self.privacy_settings, types.StoryPrivacySettingsContacts)

    @property
    def close_friends(self) -> bool | None:
        """Whether the story is visible to close friends only."""
        if self.privacy_settings is None:
            return None
        return isinstance(self.privacy_settings, types.StoryPrivacySettingsCloseFriends)

    @property
    def selected_contacts(self) -> bool | None:
        """Whether the story is visible to a hand-picked list of users."""
        if self.privacy_settings is None:
            return None
        return isinstance(
            self.privacy_settings, types.StoryPrivacySettingsSelectedUsers
        )

    @property
    def allowed_users(self) -> list[int | str] | None:
        """Users explicitly allowed to view the story."""
        return getattr(self.privacy_settings, "user_ids", None)

    @property
    def denied_users(self) -> list[int | str] | None:
        """Users explicitly denied from viewing the story."""
        return getattr(self.privacy_settings, "except_user_ids", None)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _poster_id(self) -> int | None:
        """Chat id of whoever posted the story."""
        return self.chat.id if self.chat is not None else None

    # ------------------------------------------------------------------
    # reply_* bound methods
    # ------------------------------------------------------------------

    async def reply_text(
        self,
        text: str,
        parse_mode: enums.ParseMode | None = None,
        entities: list[types.MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        reply_markup=None,
    ) -> types.Message:
        """Bound method *reply_text* of :obj:`~pyrogram.types.Story`.

        Shortcut for :meth:`~pyrogram.Client.send_message` with
        ``reply_to_story_id`` pointing at this story.
        """
        return await self._client.send_message(
            chat_id=self._poster_id(),
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
            schedule_date=schedule_date,
            protect_content=protect_content,
            reply_markup=reply_markup,
        )

    reply = reply_text

    async def reply_animation(
        self,
        animation: str | BinaryIO,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        has_spoiler: bool | None = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: str | BinaryIO | None = None,
        file_name: str | None = None,
        disable_notification: bool | None = None,
        reply_markup=None,
        reply_to_story_id: int | None = None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message:
        """Bound method *reply_animation* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_animation(
            chat_id=self._poster_id(),
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            file_name=file_name,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
            reply_to_story_id=reply_to_story_id or self.id,
            progress=progress,
            progress_args=progress_args,
        )

    async def reply_audio(
        self,
        audio: str | BinaryIO,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        duration: int = 0,
        performer: str | None = None,
        title: str | None = None,
        thumb: str | BinaryIO | None = None,
        file_name: str | None = None,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
        reply_markup=None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message:
        """Bound method *reply_audio* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_audio(
            chat_id=self._poster_id(),
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            file_name=file_name,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args,
        )

    async def reply_cached_media(
        self,
        file_id: str,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
        reply_markup=None,
    ) -> types.Message:
        """Bound method *reply_cached_media* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_cached_media(
            chat_id=self._poster_id(),
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
            reply_markup=reply_markup,
        )

    async def reply_media_group(
        self,
        media: list,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
    ) -> list[types.Message]:
        """Bound method *reply_media_group* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_media_group(
            chat_id=self._poster_id(),
            media=media,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
        )

    async def reply_photo(
        self,
        photo: str | BinaryIO,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        has_spoiler: bool | None = None,
        ttl_seconds: int | None = None,
        view_once: bool | None = None,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
        reply_markup=None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message:
        """Bound method *reply_photo* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_photo(
            chat_id=self._poster_id(),
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            view_once=view_once,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args,
        )

    async def reply_sticker(
        self,
        sticker: str | BinaryIO,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
        reply_markup=None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message:
        """Bound method *reply_sticker* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_sticker(
            chat_id=self._poster_id(),
            sticker=sticker,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args,
        )

    async def reply_video(
        self,
        video: str | BinaryIO,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        has_spoiler: bool | None = None,
        ttl_seconds: int | None = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: str | BinaryIO | None = None,
        file_name: str | None = None,
        supports_streaming: bool = True,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
        reply_markup=None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message:
        """Bound method *reply_video* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_video(
            chat_id=self._poster_id(),
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            file_name=file_name,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args,
        )

    async def reply_video_note(
        self,
        video_note: str | BinaryIO,
        duration: int = 0,
        length: int = 1,
        thumb: str | BinaryIO | None = None,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
        reply_markup=None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message:
        """Bound method *reply_video_note* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_video_note(
            chat_id=self._poster_id(),
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args,
        )

    async def reply_voice(
        self,
        voice: str | BinaryIO,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        duration: int = 0,
        disable_notification: bool | None = None,
        reply_to_story_id: int | None = None,
        reply_markup=None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message:
        """Bound method *reply_voice* of :obj:`~pyrogram.types.Story`."""
        return await self._client.send_voice(
            chat_id=self._poster_id(),
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id or self.id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args,
        )

    # ------------------------------------------------------------------
    # edit / delete / forward / export
    # ------------------------------------------------------------------

    async def delete(self) -> list[int]:
        """Bound method *delete* of :obj:`~pyrogram.types.Story`.

        Shortcut for :meth:`~pyrogram.Client.delete_stories`. v2.7.6 returned a
        bool; the current client returns the list of deleted story ids, which is
        still truthy on success.
        """
        return await self._client.delete_stories(
            chat_id=self._poster_id(),
            story_ids=self.id,
        )

    async def edit(
        self,
        privacy: enums.StoriesPrivacyRules = None,
        allowed_users: list[int] | None = None,
        denied_users: list[int] | None = None,
        animation: str | BinaryIO | None = None,
        photo: str | BinaryIO | None = None,
        video: str | BinaryIO | None = None,
        caption: str | None = None,
        parse_mode: enums.ParseMode = None,
        caption_entities: list[types.MessageEntity] | None = None,
        media_areas: list | None = None,
    ) -> types.Story:
        """Bound method *edit* of :obj:`~pyrogram.types.Story`.

        Shortcut for :meth:`~pyrogram.Client.edit_story`. The separate media
        keyword arguments are folded into an
        :obj:`~pyrogram.types.InputStoryContent`, and the privacy triple into a
        :obj:`~pyrogram.types.StoryPrivacySettings`.
        """
        return await self._client.edit_story(
            chat_id=self._poster_id(),
            story_id=self.id,
            content=_legacy_content(animation=animation, photo=photo, video=video),
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            areas=media_areas,
            privacy_settings=_legacy_privacy_settings(
                privacy, allowed_users, denied_users
            ),
        )

    async def edit_animation(self, animation: str | BinaryIO) -> types.Story:
        """Bound method *edit_animation* of :obj:`~pyrogram.types.Story`."""
        return await self.edit(animation=animation)

    async def edit_photo(self, photo: str | BinaryIO) -> types.Story:
        """Bound method *edit_photo* of :obj:`~pyrogram.types.Story`."""
        return await self.edit(photo=photo)

    async def edit_video(self, video: str | BinaryIO) -> types.Story:
        """Bound method *edit_video* of :obj:`~pyrogram.types.Story`."""
        return await self.edit(video=video)

    async def edit_caption(
        self,
        caption: str,
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
    ) -> types.Story:
        """Bound method *edit_caption* of :obj:`~pyrogram.types.Story`."""
        return await self.edit(
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
        )

    async def edit_privacy(
        self,
        privacy: enums.StoriesPrivacyRules = None,
        allowed_users: list[int] | None = None,
        denied_users: list[int] | None = None,
    ) -> types.Story:
        """Bound method *edit_privacy* of :obj:`~pyrogram.types.Story`."""
        return await self.edit(
            privacy=privacy,
            allowed_users=allowed_users,
            denied_users=denied_users,
        )

    async def export_link(self) -> types.ExportedStoryLink:
        """Bound method *export_link* of :obj:`~pyrogram.types.Story`."""
        return await self._client.export_story_link(
            chat_id=self._poster_id(),
            story_id=self.id,
        )

    async def forward(
        self,
        chat_id: int | str = None,
        privacy: enums.StoriesPrivacyRules = None,
        allowed_users: list[int] | None = None,
        denied_users: list[int] | None = None,
        pinned: bool | None = None,
        protect_content: bool | None = None,
        caption: str | None = None,
        parse_mode: enums.ParseMode = None,
        caption_entities: list[types.MessageEntity] | None = None,
        period: int | None = None,
    ) -> types.Story:
        """Bound method *forward* of :obj:`~pyrogram.types.Story`.

        Reposts this story to *chat_id*. Like v2.7.6 this goes through
        :meth:`~pyrogram.Client.send_story` with the repost fields set, not
        through :meth:`~pyrogram.Client.forward_story` (which forwards a story
        into a chat as a *message*).
        """
        return await self._client.send_story(
            chat_id=chat_id,
            media=None,
            privacy=privacy,
            allowed_users=allowed_users,
            disallowed_users=denied_users,
            pinned=pinned,
            protect_content=protect_content,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            period=period,
            fwd_from_id=self._poster_id(),
            fwd_from_story=self.id,
        )
