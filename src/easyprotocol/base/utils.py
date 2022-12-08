from __future__ import annotations

from typing import Literal, Union

from bitarray import bitarray

dataT = Union[bitarray, bytearray, bytes, None]
endianT = Literal["little", "big"]
DEFAULT_ENDIANNESS: endianT = "big"


def input_to_bytes(
    data: dataT,
    endian: endianT,
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
        # byte_val = bytearray(data)
        # if endian != DEFAULT_ENDIANNESS and bit_count is not None:
        #     byte_count = int(bit_count // 8)
        #     if byte_count < 2:
        #         int_val = int.from_bytes(byte_val, byteorder=DEFAULT_ENDIANNESS, signed=False)
        #         byte_val = int.to_bytes(int_val, length=byte_count, byteorder="little", signed=False)
        bits = bitarray(endian="little")
        # bits = bitarray(endian="big")
        bits.frombytes(data)
        if len(bits) < (8 * len(data)):
            bits = bits + bitarray("0" * ((8 * len(data)) - len(bits)), endian="little")
    elif isinstance(data, bitarray):
        bit_length = len(data)
        bits = bitarray(endian="little")
        bits.frombytes(data.tobytes())
        bits = bits[:bit_length]
    else:
        raise TypeError()
    if bit_count is not None:
        if len(bits) < bit_count and isinstance(data, bytes):
            bits = bits + bitarray("0" * (bit_count - len(bits)), endian="little")
    return bits


def hex(bts: bytes, lsB: bool = True) -> str:
    """Convert bytes to hexadecimal, but nicely.

    Args:
        hex representation of bytes, nicely formatted

    Returns:
        _type_: _description_
    """
    if lsB is False:
        bts = bytearray(bts)
        bts.reverse()
        bts = bytes(bts)
    return bytes.hex(bts, sep=" ").upper()
