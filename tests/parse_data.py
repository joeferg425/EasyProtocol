from __future__ import annotations

import math
import struct
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Literal

import pytest
from bitarray import bitarray

from easyprotocol.base.parse_generic import UNDEFINED, ParseGeneric
from easyprotocol.base.utils import hex

PARAMETER_NAMES = [
    "value",
    "bit_count",
    "byte_data",
    "bits_data",
    "endian",
]


@dataclass
class ParseData:
    name: str
    value: Any
    endian: Literal["big", "little"]
    string_format: str
    bits_data: bitarray
    byte_data: bytes | bytearray
    parent: ParseGeneric[Any] | None
    children: OrderedDict[str, Any]


def get_uint_value(value: int, bit_count: int, endian: Literal["little", "big"]) -> int:
    mask = (2**bit_count) - 1
    length = math.ceil(bit_count / 8)
    byte_val = int.to_bytes(mask, length=length, byteorder="little", signed=False)
    mask = int.from_bytes(byte_val, byteorder=endian, signed=False)
    return value & mask


def get_bitarray(value: int, bit_count: int, endian: Literal["little", "big"]) -> bitarray:
    byte_val = get_bytes(value=value, bit_count=bit_count, endian=endian)
    bits = bitarray(endian="big")
    bits.frombytes(byte_val)
    if bit_count == 0:
        b = bitarray(endian="big")
    elif bit_count == -1:
        b = bits
    else:
        b = bits[-bit_count:]
    return b


def get_bytes(value: int, bit_count: int, endian: Literal["little", "big"]) -> bytes:
    if value < 0x100 and bit_count <= 8:
        if endian == "big":
            b = struct.pack(">B", value)
        else:
            b = struct.pack("<B", value)
    elif value < 0x10000 and bit_count <= 16:
        if endian == "big":
            b = struct.pack(">H", value)
            if bit_count > 8:
                b = b
            else:
                b = b[1:]
        else:
            b = struct.pack("<H", value)
            if bit_count > 8:
                b = b
            else:
                b = b[:1]
    elif value < 0x100000000 and bit_count <= 32:
        if endian == "big":
            b = struct.pack(">I", value)
            if bit_count > 24:
                b = b
            elif bit_count > 16:
                b = b[1:]
            elif bit_count > 8:
                b = b[2:]
            else:
                b = b[3:]
        else:
            b = struct.pack("<I", value)
            if bit_count > 24:
                b = b
            elif bit_count > 16:
                b = b[:3]
            elif bit_count > 8:
                b = b[:2]
            else:
                b = b[:1]
    elif value < 0x10000000000000000 and bit_count <= 64:
        if endian == "big":
            b = struct.pack(">Q", value)
            if bit_count > 56:
                b = b
            elif bit_count > 48:
                b = b[1:]
            elif bit_count > 40:
                b = b[2:]
            elif bit_count > 32:
                b = b[3:]
            elif bit_count > 24:
                b = b[4:]
            elif bit_count > 16:
                b = b[5:]
            elif bit_count > 8:
                b = b[6:]
            else:
                b = b[7:]
        else:
            b = struct.pack("<Q", value)
            if bit_count > 56:
                b = b
            elif bit_count > 48:
                b = b[:7]
            elif bit_count > 40:
                b = b[:6]
            elif bit_count > 32:
                b = b[:5]
            elif bit_count > 24:
                b = b[:4]
            elif bit_count > 16:
                b = b[:3]
            elif bit_count > 8:
                b = b[:2]
            else:
                b = b[:1]
    else:
        b = b""
    if bit_count > 0:
        return b
    else:
        return b""


_TEST_VALUES_08_BIT = list(
    set(list([2**i for i in range(0, 8, 2)]) + list([(2**i) - 1 for i in range(0, 8 + 1, 2)]))
)
_TEST_VALUES_08_BIT.sort()
TEST_VALUES_08_BIT = [(value, 8) for value in _TEST_VALUES_08_BIT]
TEST_VALUES_08_BIT_COUNTS = list(
    set(
        [
            (((2**bit_count) - 1) & value, bit_count)
            for bit_count in range(2, 8 + 1, 2)
            if bit_count > 0
            for value in _TEST_VALUES_08_BIT
        ]
    )
)
TEST_VALUES_08_BIT_COUNTS.sort()
_TEST_VALUES_08_BIT_UINT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_08_BIT_COUNTS
    if get_uint_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_08_BIT_UINT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_08_BIT_COUNTS
    if get_uint_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_08_BIT_UINT_BE.sort()
_TEST_VALUES_08_BIT_UINT_LE.sort()
TEST_VALUES_08_BIT_UINT_BE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        "big",
        id=f'{value:03d} ({bit_count} bits), hex: "{hex(get_bytes(value=value,bit_count=bit_count,endian= "big"))}":<, bin: "{get_bitarray(value=value,bit_count=bit_count,endian= "big").to01()}":<, "big"',
    )
    for value, bit_count in TEST_VALUES_08_BIT
]
TEST_VALUES_08_BIT_UINT_LE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        "little",
        id=f'{value:03d} ({bit_count} bits), hex: "{hex(get_bytes(value=value,bit_count=bit_count,endian= "little"))}":<, bin: "{get_bitarray(value=value,bit_count=bit_count,endian= "little").to01()}":<, "little"',
    )
    for value, bit_count in TEST_VALUES_08_BIT
]
TEST_VALUES_08_BIT_UINT_BE_VARIABLE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        "big",
        id=f'{value:03d} ({bit_count} bits), hex: "{hex(get_bytes(value= value, bit_count=bit_count,endian= "big"))}":<, bin: "{get_bitarray(value= value, bit_count=bit_count,endian= "big").to01()}":<, "big"',
    )
    for value, bit_count in TEST_VALUES_08_BIT_COUNTS
]
TEST_VALUES_08_BIT_UINT_LE_VARIABLE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        "little",
        id=f'{value:03d} ({bit_count} bits), hex: "{hex(get_bytes(value= value, bit_count=bit_count, endian="little"))}":<, bin: "{get_bitarray(value=value,bit_count=bit_count,endian= "little").to01()}":<, "little"',
    )
    for value, bit_count in TEST_VALUES_08_BIT_COUNTS
]


_TEST_VALUES_16_BIT = (
    list(
        set(
            list([(2**i) for i in range(0, 16, 4) if (2**i) < 0x10000])
            + list([(2**i) - 1 for i in range(0, 16 + 4, 4)])
        )
    )
    + _TEST_VALUES_08_BIT
)
_TEST_VALUES_16_BIT.sort()
TEST_VALUES_16_BIT = [(value, 16) for value in _TEST_VALUES_16_BIT]
TEST_VALUES_16_BIT_COUNTS = list(
    set(
        [
            (((2**bit_count) - 1) & value, bit_count)
            for bit_count in range(4, 16 + 4, 4)
            for value in _TEST_VALUES_16_BIT
        ]
    )
)
TEST_VALUES_16_BIT_COUNTS.sort()
_TEST_VALUES_16_BIT_UINT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_16_BIT_COUNTS
    if get_uint_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_16_BIT_UINT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_16_BIT_COUNTS
    if get_uint_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_16_BIT_UINT_BE.sort()
_TEST_VALUES_16_BIT_UINT_LE.sort()
TEST_VALUES_16_BIT_UINT_BE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        "big",
        id=f'{value:05d} ({bit_count:02d} bits), hex: "{hex(get_bytes(value=value,bit_count=bit_count, endian="big"))}":<, bin: "{get_bitarray(value=value,bit_count=bit_count,endian= "big").to01()}":<, "big"',
    )
    for value, bit_count in TEST_VALUES_16_BIT
]
TEST_VALUES_16_BIT_UINT_LE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        "little",
        id=f'{value:05d} ({bit_count:02d} bits), hex: "{hex(get_bytes(value=value,bit_count=bit_count,endian= "little"))}":<, bin: "{get_bitarray(value=value,bit_count=bit_count,endian= "little").to01()}":<, "little"',
    )
    for value, bit_count in TEST_VALUES_16_BIT
]
TEST_VALUES_16_BIT_UINT_BE_VARIABLE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        "big",
        id=f'{value:05d} ({bit_count:02d} bits), hex: "{hex(get_bytes(value=value,bit_count=bit_count, endian="big"))}":<, bin: "{get_bitarray(value=value,bit_count=bit_count,endian= "big").to01()}":<, "big"',
    )
    for value, bit_count in _TEST_VALUES_16_BIT_UINT_BE
]
TEST_VALUES_16_BIT_UINT_LE_VARIABLE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        "little",
        id=f'{value:05d} ({bit_count:02d} bits), hex: "{hex(get_bytes(value=value,bit_count=bit_count,endian= "little"))}":<, bin: "{get_bitarray(value=value,bit_count=bit_count,endian= "little").to01()}":<, "little"',
    )
    for value, bit_count in _TEST_VALUES_16_BIT_UINT_LE
]

_TEST_VALUES_32_BIT = (
    list(
        set(
            list([(2**i) for i in range(0, 32, 8) if (2**i) < 0x100000000])
            + list([(2**i) - 1 for i in range(0, 32 + 8, 8)])
        )
    )
    + _TEST_VALUES_16_BIT
)
_TEST_VALUES_32_BIT.sort()
TEST_VALUES_32_BIT = [(value, 32) for value in _TEST_VALUES_32_BIT]
TEST_VALUES_32_BIT_COUNTS = list(
    set(
        [
            (((2**bit_count) - 1) & value, bit_count)
            for bit_count in range(8, 32 + 8, 8)
            for value in _TEST_VALUES_32_BIT
        ]
    )
)
TEST_VALUES_32_BIT_COUNTS.sort()
_TEST_VALUES_32_BIT_UINT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_32_BIT_COUNTS
    if get_uint_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_32_BIT_UINT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_32_BIT_COUNTS
    if get_uint_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_32_BIT_UINT_BE.sort()
_TEST_VALUES_32_BIT_UINT_LE.sort()

_TEST_VALUES_64_BIT = (
    list(
        set(
            list([(2**i) for i in range(0, 64, 16) if (2**i) < 0x10000000000000000])
            + list([(2**i) - 1 for i in range(0, 64 + 16, 16)])
        )
    )
    + _TEST_VALUES_32_BIT
)
_TEST_VALUES_64_BIT.sort()
TEST_VALUES_64_BIT = [(value, 64) for value in _TEST_VALUES_64_BIT]
TEST_VALUES_64_BIT_COUNTS = list(
    set(
        [
            (((2**bit_count) - 1) & value, bit_count)
            for bit_count in range(16, 64 + 16, 16)
            for value in _TEST_VALUES_64_BIT
        ]
    )
)
TEST_VALUES_64_BIT_COUNTS.sort()
_TEST_VALUES_64_BIT_UINT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_64_BIT_COUNTS
    if get_uint_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_64_BIT_UINT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_64_BIT_COUNTS
    if get_uint_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_64_BIT_UINT_BE.sort()
_TEST_VALUES_64_BIT_UINT_LE.sort()

TEST_VALUES_N_BIT_COUNTS_BE = list(
    set(
        _TEST_VALUES_08_BIT_UINT_BE
        + _TEST_VALUES_16_BIT_UINT_BE
        + _TEST_VALUES_32_BIT_UINT_BE
        + _TEST_VALUES_64_BIT_UINT_BE
    )
)
TEST_VALUES_N_BIT_COUNTS_LE = list(
    set(
        _TEST_VALUES_08_BIT_UINT_LE
        + _TEST_VALUES_16_BIT_UINT_LE
        + _TEST_VALUES_32_BIT_UINT_LE
        + _TEST_VALUES_64_BIT_UINT_LE
    )
)
TEST_VALUES_N_BIT_UINT_BE_VARIABLE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="big",
        ),
        "big",
        id=f'{value:05d} ({bit_count:02d} bits), hex: "{hex(get_bytes(value= value, bit_count=bit_count,endian= "big"))}":<, bin: "{get_bitarray(value= value, bit_count=bit_count,endian="big",).to01()}":<, "big"',
    )
    for value, bit_count in TEST_VALUES_N_BIT_COUNTS_BE
]
TEST_VALUES_N_BIT_UINT_LE_VARIABLE = [
    pytest.param(
        value,
        bit_count,
        get_bytes(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        get_bitarray(
            value=value,
            bit_count=bit_count,
            endian="little",
        ),
        "little",
        id=f'{value:03d} ({bit_count:02d} bits), hex: "{hex(get_bytes(value= value, bit_count=bit_count, endian="little"))}":<, bin: "{get_bitarray(value=value,bit_count=bit_count,endian= "little").to01()}":<, "little"',
    )
    for value, bit_count in TEST_VALUES_N_BIT_COUNTS_LE
]