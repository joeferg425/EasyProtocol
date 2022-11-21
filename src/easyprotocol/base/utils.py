from __future__ import annotations
from typing import TypeVar, Any
from bitarray import bitarray
from bitarray.util import int2ba

T = TypeVar("T", Any, Any)
InputT = TypeVar("InputT", bitarray, bytearray, bytes)


def input_to_bytes(
    data: InputT,
    bit_count: int | None = None,
) -> bitarray:
    if isinstance(data, (bytes, bytearray)):
        data = bytearray(data)
        data.reverse()
        i = int.from_bytes(data, byteorder="big", signed=False)
        bits = int2ba(i)
        if len(bits) < (8 * len(data)):
            bits = bitarray("0" * ((8 * len(data)) - len(bits))) + bits
    else:
        bits = bitarray(data)
    if bit_count is not None:
        if len(bits) < bit_count and isinstance(data, bytes):
            bits = bitarray("0" * (bit_count - len(bits))) + bits
    return bits


def hex(bts: bytes) -> str:
    return bytes.hex(bts, sep=" ").upper()
