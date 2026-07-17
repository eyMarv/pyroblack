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

"""AES primitives used by MTProto.

Backend priority:

1. **tgcrypto** (``TgCrypto-pyroblack``) — GIL-releasing C extension with
   full MTProto pack/unpack. This is pyroblack's official speedup package
   (warpcrypto-equivalent API; no separate warpcrypto dependency needed).
2. **pyaes** — pure Python fallback (slow; always works)

Install speedups with::

    pip install -U TgCrypto-pyroblack
    # or
    pip install -U pyroblack[fast]
"""

from typing import Optional
import logging

log = logging.getLogger(__name__)

# Which native backend was selected (for executor worker sizing, logging, tests)
BACKEND = "pyaes"


def _bind_tgcrypto():
    global BACKEND
    import tgcrypto

    def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return tgcrypto.ige256_encrypt(data, key, iv)

    def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return tgcrypto.ige256_decrypt(data, key, iv)

    def ctr256_encrypt(
        data: bytes, key: bytes, iv: bytearray, state: Optional[bytearray] = None
    ) -> bytes:
        return tgcrypto.ctr256_encrypt(data, key, iv, state or bytearray(1))

    def ctr256_decrypt(
        data: bytes, key: bytes, iv: bytearray, state: Optional[bytearray] = None
    ) -> bytes:
        return tgcrypto.ctr256_decrypt(data, key, iv, state or bytearray(1))

    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )

    BACKEND = "tgcrypto"
    log.info("Using TgCrypto-pyroblack")
    return ige256_encrypt, ige256_decrypt, ctr256_encrypt, ctr256_decrypt, xor


def _bind_pyaes():
    global BACKEND
    import pyaes

    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )

    def ige(data: bytes, key: bytes, iv: bytes, encrypt: bool) -> bytes:
        cipher = pyaes.AES(key)

        iv_1 = iv[:16]
        iv_2 = iv[16:]

        data = [data[i : i + 16] for i in range(0, len(data), 16)]

        if encrypt:
            for i, chunk in enumerate(data):
                iv_1 = data[i] = xor(cipher.encrypt(xor(chunk, iv_1)), iv_2)
                iv_2 = chunk
        else:
            for i, chunk in enumerate(data):
                iv_2 = data[i] = xor(cipher.decrypt(xor(chunk, iv_2)), iv_1)
                iv_1 = chunk

        return b"".join(data)

    def ctr(data: bytes, key: bytes, iv: bytearray, state: bytearray) -> bytes:
        cipher = pyaes.AES(key)

        out = bytearray(data)
        chunk = cipher.encrypt(iv)

        for i in range(0, len(data), 16):
            for j in range(0, min(len(data) - i, 16)):
                out[i + j] ^= chunk[state[0]]

                state[0] += 1

                if state[0] >= 16:
                    state[0] = 0

                if state[0] == 0:
                    for k in range(15, -1, -1):
                        try:
                            iv[k] += 1
                            break
                        except ValueError:
                            iv[k] = 0

                    chunk = cipher.encrypt(iv)

        return out

    def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return ige(data, key, iv, True)

    def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return ige(data, key, iv, False)

    def ctr256_encrypt(
        data: bytes, key: bytes, iv: bytearray, state: Optional[bytearray] = None
    ) -> bytes:
        return ctr(data, key, iv, state or bytearray(1))

    def ctr256_decrypt(
        data: bytes, key: bytes, iv: bytearray, state: Optional[bytearray] = None
    ) -> bytes:
        return ctr(data, key, iv, state or bytearray(1))

    BACKEND = "pyaes"
    log.warning(
        "TgCrypto-pyroblack is missing! "
        "Pyroblack will work the same, but uploads/downloads will be much slower. "
        "Install: pip install -U TgCrypto-pyroblack   (or pyroblack[fast])"
    )
    return ige256_encrypt, ige256_decrypt, ctr256_encrypt, ctr256_decrypt, xor


try:
    (
        ige256_encrypt,
        ige256_decrypt,
        ctr256_encrypt,
        ctr256_decrypt,
        xor,
    ) = _bind_tgcrypto()
except ImportError:
    (
        ige256_encrypt,
        ige256_decrypt,
        ctr256_encrypt,
        ctr256_decrypt,
        xor,
    ) = _bind_pyaes()
