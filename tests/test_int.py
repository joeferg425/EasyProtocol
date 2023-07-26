# flake8:noqa
import math
import struct
from typing import Literal

import pytest
from bitarray import bitarray
from parse_data import (
    PARAMETER_NAMES,
    TEST_VALUES_08_BIT_UINT,
    TEST_VALUES_16_BIT_UINT,
    TEST_VALUES_24_BIT_UINT,
    TEST_VALUES_32_BIT_UINT,
    TEST_VALUES_64_BIT_UINT,
    ParseData,
)
from test_uint import check_int

from easyprotocol.base.base_field import endianT
from easyprotocol.base.utils import DEFAULT_ENDIANNESS, hex
from easyprotocol.fields.signed_int import (
    INT08_STRING_FORMAT,
    INT16_STRING_FORMAT,
    INT24_STRING_FORMAT,
    INT32_STRING_FORMAT,
    INT64_STRING_FORMAT,
    INT_STRING_FORMAT,
    Int8Field,
    Int16Field,
    Int24Field,
    Int32Field,
    Int64Field,
    IntField,
)


def get_int_value(value: int, bit_count: int, endian: Literal["little", "big"]) -> int:
    mask = (2**bit_count) - 1
    length = math.ceil(bit_count / 8)
    byte_val = int.to_bytes(mask, length=length, byteorder="little", signed=False)
    mask = int.from_bytes(byte_val, byteorder=endian, signed=False)
    value &= mask
    byte_val = int.to_bytes(value, length=length, byteorder="little", signed=False)
    value = int.from_bytes(byte_val, byteorder=endian, signed=True)
    return value


def get_bytes(value: int, bit_count: int, endian: Literal["little", "big"]) -> bytes:
    if value < 0x100 and bit_count <= 8:
        if endian == "big":
            b = struct.pack(">b", value)
        else:
            b = struct.pack("<b", value)
    elif value < 0x10000 and bit_count <= 16:
        if endian == "big":
            b = struct.pack(">h", value)
            if bit_count > 8:
                b = b
            else:
                b = b[1:]
        else:
            b = struct.pack("<h", value)
            if bit_count > 8:
                b = b
            else:
                b = b[:1]
    elif value < 0x1000000 and bit_count <= 24:
        if endian == "big":
            b = struct.pack(">i", value)[1:]
            if bit_count > 16:
                b = b
            elif bit_count > 8:
                b = b[1:]
            else:
                b = b[2:]
        else:
            b = struct.pack("<i", value)[:-1]
            if bit_count > 16:
                b = b
            elif bit_count > 8:
                b = b[:2]
            else:
                b = b[:1]
    elif value < 0x100000000 and bit_count <= 32:
        if endian == "big":
            b = struct.pack(">i", value)
            if bit_count > 24:
                b = b
            elif bit_count > 16:
                b = b[1:]
            elif bit_count > 8:
                b = b[2:]
            else:
                b = b[3:]
        else:
            b = struct.pack("<i", value)
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
            b = struct.pack(">q", value)
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
            b = struct.pack("<q", value)
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


_TEST_VALUES_08_BIT_INT = [get_int_value(value=value, bit_count=8, endian="big") for value in TEST_VALUES_08_BIT_UINT]
TEST_VALUES_08_BIT_INT = [(value, 8) for value in _TEST_VALUES_08_BIT_INT]
TEST_VALUES_08_BIT_INT_COUNTS = list(
    set(
        [
            (get_int_value(((2**bit_count) - 1) & value, bit_count=bit_count, endian="big"), bit_count)
            for bit_count in range(2, 8 + 1, 2)
            if bit_count > 0
            for value in _TEST_VALUES_08_BIT_INT
        ]
    )
)
TEST_VALUES_08_BIT_INT_COUNTS.sort()
_TEST_VALUES_08_BIT_INT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_08_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_08_BIT_INT_BE.sort()
TEST_VALUES_08_BIT_INT_BE = [
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
    for value, bit_count in TEST_VALUES_08_BIT_INT
]
TEST_VALUES_08_BIT_INT_BE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_08_BIT_INT_COUNTS
]
_TEST_VALUES_08_BIT_INT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_08_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_08_BIT_INT_LE.sort()
TEST_VALUES_08_BIT_INT_LE = [
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
    for value, bit_count in TEST_VALUES_08_BIT_INT
]
TEST_VALUES_08_BIT_INT_LE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_08_BIT_INT_COUNTS
]

_TEST_VALUES_16_BIT_INT = [get_int_value(value=value, bit_count=16, endian="big") for value in TEST_VALUES_16_BIT_UINT]
TEST_VALUES_16_BIT_INT = [(value, 16) for value in _TEST_VALUES_16_BIT_INT]
TEST_VALUES_16_BIT_INT_COUNTS = list(
    set(
        [
            (get_int_value(((2**bit_count) - 1) & value, bit_count=bit_count, endian="big"), bit_count)
            for bit_count in range(2, 16 + 1, 2)
            if bit_count > 0
            for value in _TEST_VALUES_16_BIT_INT
        ]
    )
)
TEST_VALUES_16_BIT_INT_COUNTS.sort()
_TEST_VALUES_16_BIT_INT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_16_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_16_BIT_INT_BE.sort()
TEST_VALUES_16_BIT_INT_BE = [
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
    for value, bit_count in TEST_VALUES_16_BIT_INT
]
TEST_VALUES_16_BIT_INT_BE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_16_BIT_INT_COUNTS
]
_TEST_VALUES_16_BIT_INT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_16_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_16_BIT_INT_LE.sort()
TEST_VALUES_16_BIT_INT_LE = [
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
    for value, bit_count in TEST_VALUES_16_BIT_INT
]
TEST_VALUES_16_BIT_INT_LE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_16_BIT_INT_COUNTS
]

_TEST_VALUES_24_BIT_INT = [get_int_value(value=value, bit_count=24, endian="big") for value in TEST_VALUES_24_BIT_UINT]
TEST_VALUES_24_BIT_INT = [(value, 24) for value in _TEST_VALUES_24_BIT_INT]
TEST_VALUES_24_BIT_INT_COUNTS = list(
    set(
        [
            (get_int_value(((2**bit_count) - 1) & value, bit_count=bit_count, endian="big"), bit_count)
            for bit_count in range(2, 24 + 1, 2)
            if bit_count > 0
            for value in _TEST_VALUES_24_BIT_INT
        ]
    )
)
TEST_VALUES_24_BIT_INT_COUNTS.sort()
_TEST_VALUES_24_BIT_INT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_24_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_24_BIT_INT_BE.sort()
TEST_VALUES_24_BIT_INT_BE = [
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
    for value, bit_count in TEST_VALUES_24_BIT_INT
]
TEST_VALUES_24_BIT_INT_BE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_24_BIT_INT_COUNTS
]
_TEST_VALUES_24_BIT_INT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_24_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_24_BIT_INT_LE.sort()
TEST_VALUES_24_BIT_INT_LE = [
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
    for value, bit_count in TEST_VALUES_24_BIT_INT
]
TEST_VALUES_24_BIT_INT_LE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_24_BIT_INT_COUNTS
]

_TEST_VALUES_32_BIT_INT = [get_int_value(value=value, bit_count=32, endian="big") for value in TEST_VALUES_32_BIT_UINT]
TEST_VALUES_32_BIT_INT = [(value, 32) for value in _TEST_VALUES_32_BIT_INT]
TEST_VALUES_32_BIT_INT_COUNTS = list(
    set(
        [
            (get_int_value(((2**bit_count) - 1) & value, bit_count=bit_count, endian="big"), bit_count)
            for bit_count in range(2, 32 + 1, 2)
            if bit_count > 0
            for value in _TEST_VALUES_32_BIT_INT
        ]
    )
)
TEST_VALUES_32_BIT_INT_COUNTS.sort()
_TEST_VALUES_32_BIT_INT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_32_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_32_BIT_INT_BE.sort()
TEST_VALUES_32_BIT_INT_BE = [
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
    for value, bit_count in TEST_VALUES_32_BIT_INT
]
TEST_VALUES_32_BIT_INT_BE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_32_BIT_INT_COUNTS
]
_TEST_VALUES_32_BIT_INT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_32_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_32_BIT_INT_LE.sort()
TEST_VALUES_32_BIT_INT_LE = [
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
    for value, bit_count in TEST_VALUES_32_BIT_INT
]
TEST_VALUES_32_BIT_INT_LE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_32_BIT_INT_COUNTS
]

_TEST_VALUES_64_BIT_INT = [get_int_value(value=value, bit_count=64, endian="big") for value in TEST_VALUES_64_BIT_UINT]
TEST_VALUES_64_BIT_INT = [(value, 64) for value in _TEST_VALUES_64_BIT_INT]
TEST_VALUES_64_BIT_INT_COUNTS = list(
    set(
        [
            (get_int_value(((2**bit_count) - 1) & value, bit_count=bit_count, endian="big"), bit_count)
            for bit_count in range(2, 64 + 1, 2)
            if bit_count > 0
            for value in _TEST_VALUES_64_BIT_INT
        ]
    )
)
TEST_VALUES_64_BIT_INT_COUNTS.sort()
_TEST_VALUES_64_BIT_INT_BE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_64_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="big") == value
]
_TEST_VALUES_64_BIT_INT_BE.sort()
TEST_VALUES_64_BIT_INT_BE = [
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
    for value, bit_count in TEST_VALUES_64_BIT_INT
]
TEST_VALUES_64_BIT_INT_BE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_64_BIT_INT_COUNTS
]
_TEST_VALUES_64_BIT_INT_LE = [
    (value, bit_count)
    for value, bit_count in TEST_VALUES_64_BIT_INT_COUNTS
    if get_int_value(value=value, bit_count=bit_count, endian="little") == value
]
_TEST_VALUES_64_BIT_INT_LE.sort()
TEST_VALUES_64_BIT_INT_LE = [
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
    for value, bit_count in TEST_VALUES_64_BIT_INT
]
TEST_VALUES_64_BIT_INT_LE_VARIABLE = [
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
    for value, bit_count in TEST_VALUES_64_BIT_INT_COUNTS
]

TEST_VALUES_N_BIT_COUNTS_BE = list(
    set(
        _TEST_VALUES_08_BIT_INT_BE
        + _TEST_VALUES_16_BIT_INT_BE
        + _TEST_VALUES_24_BIT_INT_BE
        + _TEST_VALUES_32_BIT_INT_BE
        + _TEST_VALUES_64_BIT_INT_BE
    )
)
TEST_VALUES_N_BIT_COUNTS_LE = list(
    set(
        _TEST_VALUES_08_BIT_INT_LE
        + _TEST_VALUES_16_BIT_INT_LE
        + _TEST_VALUES_24_BIT_INT_LE
        + _TEST_VALUES_32_BIT_INT_LE
        + _TEST_VALUES_64_BIT_INT_LE
    )
)
TEST_VALUES_N_BIT_INT_BE_VARIABLE = [
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
        id=f'{value:020d} ({bit_count:02d} bits), hex: "{hex(get_bytes(value= value, bit_count=bit_count,endian= "big"))}":<, bin: "{get_bitarray(value= value, bit_count=bit_count,endian="big",).to01()}":<, "big"',
    )
    for value, bit_count in TEST_VALUES_N_BIT_COUNTS_BE
]
TEST_VALUES_N_BIT_INT_LE_VARIABLE = [
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


class TestIntField:
    def test_intfield_create_empty_big_endian(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack(">b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_create_empty_little_endian(self) -> None:
        value = 0
        endian = "little"
        byte_data = struct.pack("<b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_name(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack("b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        tst.name = "new_name"
        obj.name = tst.name
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_value(self) -> None:
        value1 = 0
        byte_data1 = struct.pack(">b", value1)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 10
        endian = "big"
        byte_data2 = struct.pack(">b", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
            name="test",
            value=value1,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        obj.value = value2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_bits(self) -> None:
        value1 = 0
        byte_data1 = struct.pack("b", value1)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        endian = "big"
        byte_data2 = struct.pack("b", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
            name="test",
            value=value1,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        obj.bits_lsb = bits_data2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_parent(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack("b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )
        tst.parent = Int8Field(name="parent")
        obj.parent = tst.parent
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_N_BIT_INT_BE_VARIABLE,
    )
    def test_uintfield_create_parse_n_bit_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=INT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=bit_count,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_N_BIT_INT_LE_VARIABLE,
    )
    def test_uintfield_create_parse_n_bit_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=INT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=bit_count,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_N_BIT_INT_BE_VARIABLE,
    )
    def test_intfield_create_init_value_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=INT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=bit_count,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_N_BIT_INT_LE_VARIABLE,
    )
    def test_intfield_create_init_value_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=INT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=bit_count,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )


class TestInt08:
    def test_int8_create_empty_big_endian(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack(">b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=0,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int8Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int8_create_empty_little_endian(self) -> None:
        value = 0
        endian = "little"
        byte_data = struct.pack("<b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            bits_data=bits_data,
            byte_data=byte_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int8Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_INT_BE,
    )
    def test_int8_create_parse_bytes_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            string_format="{}",
            value=value,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int8Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_INT_LE,
    )
    def test_int8_create_parse_bytes_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            string_format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int8Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_INT_BE,
    )
    def test_int8_create_parse_bits_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            string_format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int8Field(
            name=tst.name,
            data=bits_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_INT_LE,
    )
    def test_int8_create_parse_bits_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            string_format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int8Field(
            name=tst.name,
            data=bits_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_INT_BE,
    )
    def test_int8_create_init_value_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            string_format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int8Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_INT_LE,
    )
    def test_int8_create_init_value_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            string_format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int8Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int8field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFF
        value2 = 0xFF
        byte_data1 = struct.pack("h", struct.unpack("h", struct.pack("H", value1))[0])
        byte_data2 = struct.pack("b", struct.unpack("b", struct.pack("B", value2))[0])
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = Int8Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_int8field_create_parse_too_little_data(self) -> None:
        value = 0x0F
        byte_data = struct.pack("b", struct.unpack("b", struct.pack("B", value))[0])
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = Int8Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_int8_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int8Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_int8_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100
        obj = Int8Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt16:
    def test_int16_create_empty_big_endian(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack(">h", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int16Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int16_create_empty_little_endian(self) -> None:
        value = 0
        endian = "little"
        byte_data = struct.pack("<h", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int16Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_16_BIT_INT_BE,
    )
    def test_int16_create_parse_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int16Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_16_BIT_INT_LE,
    )
    def test_int16_create_parse_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int16Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_16_BIT_INT_BE,
    )
    def test_int16_create_init_value_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int16Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_16_BIT_INT_LE,
    )
    def test_int16_create_init_value_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int16Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int16field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFF
        value2 = 0xFFFF
        byte_data1 = struct.pack("i", struct.unpack("i", struct.pack("I", value1))[0])
        byte_data2 = struct.pack("h", struct.unpack("h", struct.pack("H", value2))[0])
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = Int16Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_int16field_create_parse_too_little_data(self) -> None:
        value = 0x0F
        byte_data = struct.pack("h", struct.unpack("h", struct.pack("H", value))[0])
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = Int16Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_int16_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int16Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_int16_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x10000
        obj = Int16Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt24:
    def test_int24_create_empty_big_endian(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack(">i", value)[1:]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int24Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int24_create_empty_little_endian(self) -> None:
        value = 0
        endian = "little"
        byte_data = struct.pack("<i", value)[:-1]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int24Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_24_BIT_INT_BE,
    )
    def test_int24_create_parse_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int24Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_24_BIT_INT_LE,
    )
    def test_int24_create_parse_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int24Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_24_BIT_INT_BE,
    )
    def test_int24_create_init_value_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int24Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_24_BIT_INT_LE,
    )
    def test_int24_create_init_value_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int24Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int24field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFF
        value2 = 0xFFFFFFFF
        value3 = 0xFF
        byte_data1 = struct.pack("i", struct.unpack("i", struct.pack("I", value1))[0])
        byte_data2 = struct.pack("i", struct.unpack("i", struct.pack("I", value2))[0])[:-1]
        byte_data3 = struct.pack("b", struct.unpack("b", struct.pack("B", value3))[0])
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data3 = bitarray(endian="little")
        bits_data3.frombytes(byte_data3)
        extra = bitarray(bits_data3)
        name = "test"
        obj = Int24Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_int24field_create_parse_too_little_data(self) -> None:
        value = 0x0FFF
        byte_data = struct.pack("h", struct.unpack("h", struct.pack("H", value))[0])
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = Int24Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_int24_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int24Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_int24_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x1000000
        obj = Int24Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt32:
    def test_int32_create_empty_big_endian(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack(">i", value)
        bits_data = bitarray(endian="big")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int32_create_empty_little_endian(self) -> None:
        value = 0
        endian = "little"
        byte_data = struct.pack("<i", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_INT_BE,
    )
    def test_int32_create_parse_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int32Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_INT_LE,
    )
    def test_int32_create_parse_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int32Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_INT_BE,
    )
    def test_int32_create_init_value_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int32Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_INT_LE,
    )
    def test_int32_create_init_value_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int32Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int32field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFFFFFFFFFF
        value2 = 0xFFFFFFFF
        byte_data1 = struct.pack("q", struct.unpack("q", struct.pack("Q", value1))[0])
        byte_data2 = struct.pack("i", struct.unpack("i", struct.pack("I", value2))[0])
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = Int32Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_int32field_create_parse_too_little_data(self) -> None:
        value = 0x0F
        byte_data = struct.pack("i", struct.unpack("i", struct.pack("I", value))[0])
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = Int32Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_int32_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int32Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_int32_set_value_invalid_value(self) -> None:
        name = "test"
        value = 900000000001
        obj = Int32Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt64:
    def test_int64_create_empty_big_endian(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack(">q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int64Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int64_create_empty_little_endian(self) -> None:
        value = 0
        endian = "little"
        byte_data = struct.pack("<q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int64Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_64_BIT_INT_BE,
    )
    def test_int64_create_parse_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int64Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_64_BIT_INT_LE,
    )
    def test_int64_create_parse_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int64Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_64_BIT_INT_BE,
    )
    def test_int64_create_init_value_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int64Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_64_BIT_INT_LE,
    )
    def test_int64_create_init_value_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = Int64Field(
            name=tst.name,
            default=tst.value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_int64field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFFFFFFFFFF
        value2 = 0xFFFFFFFF
        byte_data1 = struct.pack("q", struct.unpack("q", struct.pack("Q", value1))[0])
        byte_data1 += byte_data1
        byte_data2 = struct.pack("i", struct.unpack("i", struct.pack("I", value2))[0])
        byte_data2 += byte_data2
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = Int64Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_int64field_create_parse_too_little_data(self) -> None:
        value = 0x0F
        byte_data = struct.pack("i", struct.unpack("i", struct.pack("I", value))[0])
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = Int32Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_int64_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int64Field(name=name)
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_int64_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x10000000000000000
        obj = Int64Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value
