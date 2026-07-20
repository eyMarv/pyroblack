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


from .accept_terms_of_service import AcceptTermsOfService
from .change_phone_number import ChangePhoneNumber
from .check_password import CheckPassword
from .connect import Connect
from .disconnect import Disconnect
from .get_active_sessions import GetActiveSessions
from .get_option import GetOption
from .get_password_hint import GetPasswordHint
from .initialize import Initialize
from .log_out import LogOut
from .recover_password import RecoverPassword
from .resend_code import ResendCode
from .resend_phone_number_code import ResendPhoneNumberCode
from .reset_session import ResetSession
from .reset_sessions import ResetSessions
from .send_code import SendCode
from .send_phone_number_code import SendPhoneNumberCode
from .send_recovery_code import SendRecoveryCode
from .sign_in import SignIn
from .sign_in_bot import SignInBot
from .sign_in_qrcode import SignInQrcode
from .sign_up import SignUp
from .terminate import Terminate
from .terminate_all_other_sessions import TerminateAllOtherSessions
from .terminate_session import TerminateSession


class Auth(
    AcceptTermsOfService,
    CheckPassword,
    Connect,
    Disconnect,
    GetActiveSessions,
    GetOption,
    GetPasswordHint,
    Initialize,
    LogOut,
    RecoverPassword,
    ResendCode,
    ResetSession,
    ResetSessions,
    SendCode,
    SendRecoveryCode,
    SignIn,
    SignInBot,
    SignInQrcode,
    SignUp,
    Terminate,
    TerminateAllOtherSessions,
    TerminateSession,
    ChangePhoneNumber,
    SendPhoneNumberCode,
    ResendPhoneNumberCode,
):
    pass
