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

import logging
import re
from typing import List, Optional

import pyrogram
from pyrogram import enums, raw, types
from pyrogram.errors import NetworkMigrate, PhoneMigrate
from pyrogram.session import Session, Auth

log = logging.getLogger(__name__)


class SendPhoneNumberCode:
    async def send_phone_number_code(
        self: "pyrogram.Client",
        phone_number: str,
        settings: Optional["types.PhoneNumberAuthenticationSettings"] = None,
        type: "enums.PhoneNumberCodeType" = enums.PhoneNumberCodeType.AUTHENTICATION,
        # Deprecated params
        current_number: Optional[bool] = None,
        allow_flashcall: Optional[bool] = None,
        allow_app_hash: Optional[bool] = None,
        allow_missed_call: Optional[bool] = None,
        allow_firebase: Optional[bool] = None,
        logout_tokens: Optional[List[bytes]] = None,
        token: Optional[str] = None,
        app_sandbox: Optional[bool] = None,
    ) -> "types.SentCode":
        """Sends a code to the specified phone number. Aborts previous phone number verification if there was one.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            settings (:obj:`~pyrogram.types.PhoneNumberAuthenticationSettings`, *optional*):
                Settings for the authentication of the user's phone number.

            type (:obj:`~pyrogram.enums.PhoneNumberCodeType`, *optional*):
                Type of the request for which the code is sent.
                Defaults to authentication.

        Returns:
            :obj:`~pyrogram.types.SentCode`: On success, returns information about the sent code.

        Raises:
            BadRequest: In case the phone number is invalid.
        """
        phone_number = re.sub(r"\D", "", phone_number)

        if settings is None:
            settings = types.PhoneNumberAuthenticationSettings()

        if any(
            (
                current_number is not None,
                allow_flashcall is not None,
                allow_app_hash is not None,
                allow_missed_call is not None,
                allow_firebase is not None,
                logout_tokens is not None,
                token is not None,
                app_sandbox is not None,
            )
        ):
            if current_number is not None:
                log.warning(
                    "`current_number` is deprecated and will be removed in future updates. Use `settings` instead."
                )

            if allow_flashcall is not None:
                log.warning(
                    "`allow_flashcall` is deprecated and will be removed in future updates. Use `settings` instead."
                )

            if allow_app_hash is not None:
                log.warning(
                    "`allow_app_hash` is deprecated and will be removed in future updates. Use `settings` instead."
                )

            if allow_missed_call is not None:
                log.warning(
                    "`allow_missed_call` is deprecated and will be removed in future updates. Use `settings` instead."
                )

            if allow_firebase is not None:
                log.warning(
                    "`allow_firebase` is deprecated and will be removed in future updates. Use `settings` instead."
                )

            if logout_tokens is not None:
                log.warning(
                    "`logout_tokens` is deprecated and will be removed in future updates. Use `settings` instead."
                )

            if token is not None:
                log.warning(
                    "`token` is deprecated and will be removed in future updates. Use `settings` instead."
                )

            if app_sandbox is not None:
                log.warning(
                    "`app_sandbox` is deprecated and will be removed in future updates. Use `settings` instead."
                )

            firebase_settings = None

            if allow_firebase:
                firebase_settings = types.FirebaseAuthenticationSettingsAndroid()

            if token is not None or app_sandbox is not None:
                firebase_settings = types.FirebaseAuthenticationSettingsIos(
                    device_token=token, is_app_sandbox=app_sandbox
                )

            settings = types.PhoneNumberAuthenticationSettings(
                allow_flash_call=allow_flashcall,
                allow_missed_call=allow_missed_call,
                is_current_phone_number=current_number,
                allow_sms_retriever_api=allow_app_hash,
                firebase_authentication_settings=firebase_settings,
                authentication_tokens=logout_tokens,
            )

        while True:
            try:
                if type == enums.PhoneNumberCodeType.CHANGE:
                    rpc = raw.functions.account.SendChangePhoneCode(
                        phone_number=phone_number,
                        settings=settings.write(),
                    )
                elif type == enums.PhoneNumberCodeType.VERIFY:
                    rpc = raw.functions.account.SendVerifyPhoneCode(
                        phone_number=phone_number,
                        settings=settings.write(),
                    )
                else:
                    rpc = raw.functions.auth.SendCode(
                        phone_number=phone_number,
                        api_id=self.api_id,
                        api_hash=self.api_hash,
                        settings=settings.write(),
                    )

                r = await self.invoke(rpc)
            except (PhoneMigrate, NetworkMigrate) as e:
                await self.session.stop()

                await self.storage.dc_id(e.value)
                await self.storage.auth_key(
                    await Auth(
                        self, await self.storage.dc_id(),
                        await self.storage.test_mode()
                    ).create()
                )
                self.session = Session(
                    self, await self.storage.dc_id(),
                    await self.storage.auth_key(), await self.storage.test_mode()
                )

                await self.session.start()
            else:
                return types.SentCode._parse(r)

    send_code = send_phone_number_code
