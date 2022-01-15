# /usr/bin/env python

"""Base58 encoding and decoding"""

from binascii import hexlify, unhexlify

B58_BASE = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class InvalidBase58Error(Exception):
    pass


def i2b(n: int) -> bytes:
    # return n.to_bytes((n.bit_length() + 7) // 8, byteorder='big', signed=True)
    return n.to_bytes(4, byteorder='big', signed=True)

def b2i(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big', signed=True)

def encode(b: bytes) -> str:
    """Encode bytes to a base58-encoded string"""

    import sys

    # Convert big-endian bytes to integer
    # we rely on pythonic INT variable size
    n = int("0x0" + hexlify(b).decode("utf8"), 16)

    # Divide that integer into bas58
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(B58_BASE[r])
    res = "".join(res[::-1])

    # Encode leading zeros as base58 zeros
    czero = 0
    pad = 0

    for c in b:
        if c == czero:
            pad += 1
        else:
            break

    return B58_BASE[0] * pad + res


def decode(s: str) -> bytes:
    """Decode a base58-encoding string, returning bytes"""
    if not s:
        return b""

    # Convert the string to an integer
    n = 0
    for c in s:
        n *= 58
        if c not in B58_BASE:
            raise InvalidBase58Error("Character %r is not a valid base58 character" % c)
        digit = B58_BASE.index(c)
        n += digit

    # Convert the integer to bytes
    h = "%x" % n
    if len(h) % 2:
        h = "0" + h
    res = unhexlify(h.encode("utf8"))

    # Add padding back.
    pad = 0
    for c in s[:-1]:
        if c == B58_BASE[0]:
            pad += 1
        else:
            break
    return b"\x00" * pad + res
