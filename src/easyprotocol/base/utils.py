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
        bits = bitarray(endian="little")
        bits.frombytes(data)
        if len(bits) < (8 * len(data)):
            bits = bits + bitarray("0" * ((8 * len(data)) - len(bits)), endian="little")
    else:
        bits = bitarray(data, endian="little")
    if bit_count is not None:
        if len(bits) < bit_count and isinstance(data, bytes):
            bits = +bits + bitarray("0" * (bit_count - len(bits)), endian="little")
    return bits


def hex(bts: bytes) -> str:
    return bytes.hex(bts, sep=" ").upper()
