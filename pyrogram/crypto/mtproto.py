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

from hashlib import sha256
from io import BytesIO
from os import urandom

from pyrogram.errors import SecurityCheckMismatch
from pyrogram.raw.core import Message, Long
from . import aes

# TgCrypto >= 1.3.0 ships native pack_message / unpack_message: the whole
# MTProto 2.0 frame (KDF + msg_key + AES-IGE + framing) computed in one C call
# that releases the GIL a single time. This is the throughput lever wzgram gets
# from warpcrypto — it keeps the per-packet path off the Python/hashlib+GIL hot
# loop under concurrent transfers. If an older TgCrypto is installed we fall
# back to the pure-Python path below so pyroblack still runs (just slower).
try:
    import tgcrypto

    _HAS_NATIVE_MTPROTO = hasattr(tgcrypto, "pack_message") and hasattr(
        tgcrypto, "unpack_message"
    )
except ImportError:
    _HAS_NATIVE_MTPROTO = False

# 64-bit mask: raw.core.Long is *signed*, but the native pack_message parses the
# salt as an unsigned 64-bit int. The two's-complement bytes are identical, so
# masking a negative salt (e.g. a server salt) yields the same wire bytes
# without an OverflowError.
_U64 = (1 << 64) - 1


def kdf(auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
    # https://core.telegram.org/mtproto/description#defining-aes-key-and-initialization-vector
    x = 0 if outgoing else 8

    sha256_a = sha256(msg_key + auth_key[x: x + 36]).digest()
    sha256_b = sha256(auth_key[x + 40:x + 76] + msg_key).digest()  # 76 = 40 + 36

    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]

    return aes_key, aes_iv


def _pack_native(
    message: Message, salt: int, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> bytes:
    # message.write() is msg_id(8) | seq_no(4) | length(4) | body. Hand the
    # decomposed fields to the native packer so it can assemble
    # salt | session_id | msg_id | seq_no | length | body | padding, hash, and
    # encrypt in one GIL-released call. Mirrors wzgram's crypto/mtproto.py:pack.
    return tgcrypto.pack_message(
        message.msg_id,
        message.seq_no,
        message.body.write(),
        salt & _U64,
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
    msg_key_large = sha256(auth_key[88: 88 + 32] + data + padding).digest()
    msg_key = msg_key_large[8:24]
    aes_key, aes_iv = kdf(auth_key, msg_key, True)

    return auth_key_id + msg_key + aes.ige256_encrypt(data + padding, aes_key, aes_iv)


def pack(message: Message, salt: int, session_id: bytes, auth_key: bytes, auth_key_id: bytes) -> bytes:
    if _HAS_NATIVE_MTPROTO:
        return _pack_native(message, salt, session_id, auth_key, auth_key_id)

    return _pack_python(message, salt, session_id, auth_key, auth_key_id)


def _decrypt_native(
    packet: bytes, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> tuple:
    # The native unpacker verifies auth_key_id, msg_key and session_id (raising
    # ValueError on mismatch) in one GIL-released C call and returns the raw
    # body bytes — no TL parsing. Convert its ValueError into
    # SecurityCheckMismatch so callers keep a single failure type.
    try:
        msg_id, seq_no, length, body_bytes, total_len = tgcrypto.unpack_message(
            packet, session_id, auth_key, auth_key_id
        )
    except ValueError as e:
        raise SecurityCheckMismatch(str(e))

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
    # https://core.telegram.org/mtproto/security_guidelines#checking-session-id
    SecurityCheckMismatch.check(data[8:16] == session_id, "data.read(8) == session_id")

    # https://core.telegram.org/mtproto/security_guidelines#checking-sha256-hash-value-of-msg-key
    # 96 = 88 + 8 (incoming message)
    SecurityCheckMismatch.check(
        msg_key == sha256(auth_key[96:96 + 32] + data).digest()[8:24],
        "msg_key == sha256(auth_key[96:96 + 32] + data.getvalue()).digest()[8:24]"
    )

    msg_id = int.from_bytes(data[16:24], "little", signed=True)
    seq_no = int.from_bytes(data[24:28], "little")
    length = int.from_bytes(data[28:32], "little")

    # https://core.telegram.org/mtproto/security_guidelines#checking-message-length
    payload = data[32:]
    padding = payload[length:]
    SecurityCheckMismatch.check(12 <= len(padding) <= 1024, "12 <= len(padding) <= 1024")
    SecurityCheckMismatch.check(len(payload) % 4 == 0, "len(payload) % 4 == 0")

    return msg_id, seq_no, length, payload[:length]


def decrypt(
    packet: bytes, session_id: bytes, auth_key: bytes, auth_key_id: bytes
) -> tuple:
    """Decrypt and verify a packet, returning ``(msg_id, seq_no, length, body_bytes)``.

    Only the AES/hash work and the byte-level MTProto security checks happen
    here; the TL body is left as raw bytes so this can run on the crypto
    executor while the (Python, GIL-bound) TL parse runs on the event loop via
    :func:`parse`. Raises :class:`SecurityCheckMismatch` on any check failure.
    """
    if _HAS_NATIVE_MTPROTO:
        return _decrypt_native(packet, session_id, auth_key, auth_key_id)

    return _decrypt_python(packet, session_id, auth_key, auth_key_id)


def parse(msg_id: int, seq_no: int, length: int, body_bytes: bytes) -> Message:
    """Deserialize a decrypted body into a :class:`Message`.

    Runs the TL deserialization (pure Python) and the final msg_id parity check.
    Intended to run on the event loop, not the crypto executor, so the crypto
    threads only ever do crypto — the second half of the wzgram throughput win.
    """
    from pyrogram.raw.core import TLObject

    try:
        body = TLObject.read(BytesIO(body_bytes))
    except KeyError as e:
        if e.args[0] == 0:
            raise ConnectionError("Received empty data. Check your internet connection.")

        left = body_bytes.hex()
        left = [left[i:i + 64] for i in range(0, len(left), 64)]
        left = [[left[i:i + 8] for i in range(0, len(left), 8)] for left in left]
        left = "\n".join(" ".join(x for x in left) for left in left)

        raise ValueError(f"The server sent an unknown constructor: {hex(e.args[0])}\n{left}")

    message = Message(body, msg_id, seq_no, length)

    # https://core.telegram.org/mtproto/security_guidelines#checking-msg-id
    SecurityCheckMismatch.check(message.msg_id % 2 != 0, "message.msg_id % 2 != 0")

    return message


def unpack(
    b: BytesIO,
    session_id: bytes,
    auth_key: bytes,
    auth_key_id: bytes
) -> Message:
    # Backwards-compatible one-shot: decrypt + parse together. session.py splits
    # these across the executor / loop boundary instead, but any external caller
    # (and the pure-Python fallback path) still gets a fully-formed Message.
    return parse(*decrypt(b.read(), session_id, auth_key, auth_key_id))
