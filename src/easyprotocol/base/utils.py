from __future__ import annotations

from typing import Any, TypeVar, Union

from bitarray import bitarray

dataT = Union[bitarray, bytearray, bytes, None]


def input_to_bytes(
    data: dataT,
    bit_count: int | None = None,
) -> bitarray:
    """Convert bits or bytes into valid bits

    Args:
        data: data that needs to be little-endian bits
        bit_count: the number of desired output bits

    Returns:
        the bit data
    """
    if isinstance(data, (bytes, bytearray)):
        data = bytearray(data)
        bits = bitarray(endian="little")
        bits.frombytes(data)
        if len(bits) < (8 * len(data)):
            bits = bits + bitarray("0" * ((8 * len(data)) - len(bits)), endian="little")
    elif isinstance(data, bitarray):
        bits = bitarray(data, endian="little")
    else:
        raise TypeError()
    if bit_count is not None:
        if len(bits) < bit_count and isinstance(data, bytes):
            bits = bits + bitarray("0" * (bit_count - len(bits)), endian="little")
    return bits


def hex(bts: bytes) -> str:
    """Convert bytes to hexadecimal, but nicely.

    Args:
        hex representation of bytes, nicely formatted

    Returns:
        _type_: _description_
    """
    return bytes.hex(bts, sep=" ").upper()
