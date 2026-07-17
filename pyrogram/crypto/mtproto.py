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

"""MTProto 2.0 pack / unpack.

Uses ``TgCrypto-pyroblack`` native ``pack_message`` / ``unpack_message`` when
available (warpcrypto-equivalent GIL-releasing C path). Falls back to pure
Python otherwise.

``decrypt`` returns raw body bytes for the crypto executor; ``parse`` runs TL
deserialization on the event loop.
"""

from hashlib import sha256
from io import BytesIO
from os import urandom
import logging

from pyrogram.errors import SecurityCheckMismatch
from pyrogram.raw.core import Message, Long
from . import aes

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Native pack/unpack via TgCrypto-pyroblack (import name: tgcrypto)
# ---------------------------------------------------------------------------
_native = None

try:
    import tgcrypto as _native  # type: ignore

    if not (
        hasattr(_native, "pack_message") and hasattr(_native, "unpack_message")
    ):
        _native = None
except ImportError:
    _native = None

_HAS_NATIVE_MTPROTO = _native is not None

if _HAS_NATIVE_MTPROTO:
    log.info("Using native MTProto pack/unpack via TgCrypto-pyroblack")
else:
    log.debug(
        "Native MTProto pack/unpack unavailable "
        "(install TgCrypto-pyroblack for speedups)"
    )


def kdf(auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
    # https://core.telegram.org/mtproto/description#defining-aes-key-and-initialization-vector
    x = 0 if outgoing else 8

    sha256_a = sha256(msg_key + auth_key[x : x + 36]).digest()
    sha256_b = sha256(auth_key[x + 40 : x + 76] + msg_key).digest()  # 76 = 40 + 36

    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]

    return aes_key, aes_iv


def _pack_native(
    message: Message, salt: int, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> bytes:
    # TgCrypto-pyroblack accepts signed i64 salts (same as warpcrypto).
    return _native.pack_message(
        message.msg_id,
        message.seq_no,
        message.body.write(),
        salt,
        session_id,
        auth_key,
        auth_key_id,
    )


def _pack_python(
    message: Message, salt: int, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> bytes:
    data = Long(salt) + session_id + message.write()
    padding = urandom(-(len(data) + 12) % 16 + 12)

    # 88 = 88 + 0 (outgoing message)
    msg_key_large = sha256(auth_key[88 : 88 + 32] + data + padding).digest()
    msg_key = msg_key_large[8:24]
    aes_key, aes_iv = kdf(auth_key, msg_key, True)

    return auth_key_id + msg_key + aes.ige256_encrypt(data + padding, aes_key, aes_iv)


def pack(
    message: Message, salt: int, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> bytes:
    if _HAS_NATIVE_MTPROTO:
        return _pack_native(message, salt, session_id, auth_key, auth_key_id)

    return _pack_python(message, salt, session_id, auth_key, auth_key_id)


def _decrypt_native(
    packet: bytes, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> tuple:
    try:
        msg_id, seq_no, length, body_bytes, total_len = _native.unpack_message(
            packet, session_id, auth_key, auth_key_id
        )
    except ValueError as e:
        raise SecurityCheckMismatch(str(e)) from e

    # https://core.telegram.org/mtproto/security_guidelines#checking-message-length
    padding = total_len - 16 - length
    SecurityCheckMismatch.check(12 <= padding <= 1024, "12 <= len(padding) <= 1024")
    SecurityCheckMismatch.check(total_len % 4 == 0, "len(payload) % 4 == 0")

    return msg_id, seq_no, length, body_bytes


def _decrypt_python(
    packet: bytes, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> tuple:
    b = BytesIO(packet)

    SecurityCheckMismatch.check(b.read(8) == auth_key_id, "b.read(8) == auth_key_id")

    msg_key = b.read(16)
    aes_key, aes_iv = kdf(auth_key, msg_key, False)
    data = aes.ige256_decrypt(b.read(), aes_key, aes_iv)

    # data = salt(8) | session_id(8) | msg_id(8) | seq_no(4) | length(4) | body | padding
    SecurityCheckMismatch.check(data[8:16] == session_id, "data.read(8) == session_id")

    # 96 = 88 + 8 (incoming message)
    SecurityCheckMismatch.check(
        msg_key == sha256(auth_key[96 : 96 + 32] + data).digest()[8:24],
        "msg_key == sha256(auth_key[96:96 + 32] + data.getvalue()).digest()[8:24]",
    )

    msg_id = int.from_bytes(data[16:24], "little", signed=True)
    seq_no = int.from_bytes(data[24:28], "little")
    length = int.from_bytes(data[28:32], "little")

    payload = data[32:]
    padding = payload[length:]
    SecurityCheckMismatch.check(12 <= len(padding) <= 1024, "12 <= len(padding) <= 1024")
    SecurityCheckMismatch.check(len(payload) % 4 == 0, "len(payload) % 4 == 0")

    return msg_id, seq_no, length, payload[:length]


def decrypt(
    packet: bytes, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> tuple:
    """Decrypt and verify a packet → ``(msg_id, seq_no, length, body_bytes)``."""
    if _HAS_NATIVE_MTPROTO:
        return _decrypt_native(packet, session_id, auth_key, auth_key_id)

    return _decrypt_python(packet, session_id, auth_key, auth_key_id)


def parse(msg_id: int, seq_no: int, length: int, body_bytes: bytes) -> Message:
    """Deserialize decrypted body into a :class:`Message` (event-loop side)."""
    from pyrogram.raw.core import TLObject

    try:
        body = TLObject.read(BytesIO(body_bytes))
    except KeyError as e:
        if e.args[0] == 0:
            raise ConnectionError(
                "Received empty data. Check your internet connection."
            ) from e

        left = body_bytes.hex()
        left = [left[i : i + 64] for i in range(0, len(left), 64)]
        left = [[left[i : i + 8] for i in range(0, len(left), 8)] for left in left]
        left = "\n".join(" ".join(x for x in left) for left in left)

        raise ValueError(
            f"The server sent an unknown constructor: {hex(e.args[0])}\n{left}"
        ) from e

    message = Message(body, msg_id, seq_no, length)

    SecurityCheckMismatch.check(message.msg_id % 2 != 0, "message.msg_id % 2 != 0")

    return message


def unpack(
    b: BytesIO, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> Message:
    """One-shot decrypt + parse (backward-compatible)."""
    return parse(*decrypt(b.read(), session_id, auth_key, auth_key_id))
