import struct
from collections import OrderedDict
from typing import Literal

import pytest
from bitarray import bitarray
from parse_data import ParseData

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.utils import hex
from easyprotocol.fields.unsigned_int import (
    UINT8_STRING_FORMAT,
    UINT16_STRING_FORMAT,
    UINT24_STRING_FORMAT,
    UINT32_STRING_FORMAT,
    UINT64_STRING_FORMAT,
    UINT_STRING_FORMAT,
    UInt8Field,
    UInt16Field,
    UInt24Field,
    UInt32Field,
    UInt64Field,
    UIntField,
    UIntFieldGeneric,
)


def get_bitarray(b: bytes) -> bitarray:
    bits = bitarray(endian="big")
    bits.frombytes(b)
    return bits


def get_8bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">B", v)
    else:
        return struct.pack("<B", v)


def get_16bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">H", v)
    else:
        return struct.pack("<H", v)


def get_24bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">I", v)[1:]
    else:
        return struct.pack("<I", v)[:-1]


def get_32bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">I", v)
    else:
        return struct.pack("<I", v)


def get_64bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">Q", v)
    else:
        return struct.pack("<Q", v)


TEST_VALUES_08_BIT = [
    0x00,
    0x01,
    0x10,
    0x80,
    0xFF,
]
TEST_VALUES_08_BIT_UINT_LE = [
    pytest.param(
        v,
        get_8bit_bytes(v, "big"),
        get_8bit_bytes(v, "little"),
        get_bitarray(get_8bit_bytes(v, "big")),
        get_bitarray(get_8bit_bytes(v, "little")),
        "little",
        id=f'{v}, "{hex(get_8bit_bytes(v, "little"))}", "{get_bitarray(get_8bit_bytes(v, "little")).to01()}", "little"',
    )
    for v in TEST_VALUES_08_BIT
]
TEST_VALUES_08_BIT_UINT_BE = [
    pytest.param(
        v,
        get_8bit_bytes(v, "big"),
        get_8bit_bytes(v, "little"),
        get_bitarray(get_8bit_bytes(v, "big")),
        get_bitarray(get_8bit_bytes(v, "little")),
        "big",
        id=f'{v}, "{hex(get_8bit_bytes(v, "big"))}", "{get_bitarray(get_8bit_bytes(v, "big")).to01()}", "big"',
    )
    for v in TEST_VALUES_08_BIT
]
TEST_VALUES_16_BIT = [
    0x0000,
    0x0001,
    0x0010,
    0x0080,
    0x00FF,
    0x0100,
    0x0800,
    0x1000,
    0x8000,
    0xFF00,
]
TEST_VALUES_16_BIT_UINT_LE = [
    pytest.param(
        v,
        get_16bit_bytes(v, "big"),
        get_16bit_bytes(v, "little"),
        get_bitarray(get_16bit_bytes(v, "big")),
        get_bitarray(get_16bit_bytes(v, "little")),
        "little",
        id=f'{v}, "{hex(get_16bit_bytes(v, "little"))}", "{get_bitarray(get_16bit_bytes(v, "little")).to01()}", "little"',
    )
    for v in TEST_VALUES_16_BIT
]
TEST_VALUES_16_BIT_UINT_BE = [
    pytest.param(
        v,
        get_16bit_bytes(v, "big"),
        get_16bit_bytes(v, "little"),
        get_bitarray(get_16bit_bytes(v, "big")),
        get_bitarray(get_16bit_bytes(v, "little")),
        "big",
        id=f'{v}, "{hex(get_16bit_bytes(v, "big"))}", "{get_bitarray(get_16bit_bytes(v, "big")).to01()}", "big"',
    )
    for v in TEST_VALUES_16_BIT
]
TEST_VALUES_24_BIT = [
    0x000000,
    0x000001,
    0x000010,
    0x000080,
    0x0000FF,
    0x000100,
    0x001000,
    0x008000,
    0x00FF00,
    0x010000,
    0x100000,
    0x800000,
    0xFF0000,
]
TEST_VALUES_24_BIT_UINT_LE = [
    pytest.param(
        v,
        get_24bit_bytes(v, "big"),
        get_24bit_bytes(v, "little"),
        get_bitarray(get_24bit_bytes(v, "big")),
        get_bitarray(get_24bit_bytes(v, "little")),
        "little",
        id=f'{v}, "{hex(get_24bit_bytes(v, "little"))}", "{get_bitarray(get_24bit_bytes(v, "little")).to01()}", "little"',
    )
    for v in TEST_VALUES_24_BIT
]
TEST_VALUES_24_BIT_UINT_BE = [
    pytest.param(
        v,
        get_24bit_bytes(v, "big"),
        get_24bit_bytes(v, "little"),
        get_bitarray(get_24bit_bytes(v, "big")),
        get_bitarray(get_24bit_bytes(v, "little")),
        "big",
        id=f'{v}, "{hex(get_24bit_bytes(v, "big"))}", "{get_bitarray(get_24bit_bytes(v, "big")).to01()}", "big"',
    )
    for v in TEST_VALUES_24_BIT
]
TEST_VALUES_32_BIT = [
    0x00000000,
    0x00000001,
    0x00000010,
    0x00000080,
    0x000000FF,
    0x00000100,
    0x00001000,
    0x00008000,
    0x0000FF00,
    0x00010000,
    0x00100000,
    0x00800000,
    0x00FF0000,
    0x01000000,
    0x10000000,
    0x80000000,
    0xFF000000,
]
TEST_VALUES_32_BIT_UINT_LE = [
    pytest.param(
        v,
        get_32bit_bytes(v, "big"),
        get_32bit_bytes(v, "little"),
        get_bitarray(get_32bit_bytes(v, "big")),
        get_bitarray(get_32bit_bytes(v, "little")),
        "little",
        id=f'{v}, "{hex(get_32bit_bytes(v, "little"))}", "{get_bitarray(get_32bit_bytes(v, "little")).to01()}", "little"',
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_32_BIT_UINT_BE = [
    pytest.param(
        v,
        get_32bit_bytes(v, "big"),
        get_32bit_bytes(v, "little"),
        get_bitarray(get_32bit_bytes(v, "big")),
        get_bitarray(get_32bit_bytes(v, "little")),
        "big",
        id=f'{v}, "{hex(get_32bit_bytes(v, "big"))}", "{get_bitarray(get_32bit_bytes(v, "big")).to01()}", "big"',
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_64_BIT = [
    0x0000000000000000,
    0x0000000000000001,
    0x0000000000000010,
    0x0000000000000080,
    0x00000000000000FF,
    0x0000000000000100,
    0x0000000000001000,
    0x0000000000008000,
    0x000000000000FF00,
    0x0000000000010000,
    0x0000000000100000,
    0x0000000000800000,
    0x0000000000FF0000,
    0x0000000001000000,
    0x0000000010000000,
    0x0000000080000000,
    0x00000000FF000000,
    0x0000000000000000,
    0x0000000100000000,
    0x0000001000000000,
    0x0000008000000000,
    0x000000FF00000000,
    0x0000010000000000,
    0x0000100000000000,
    0x0000800000000000,
    0x0000FF0000000000,
    0x0001000000000000,
    0x0010000000000000,
    0x0080000000000000,
    0x00FF000000000000,
    0x0100000000000000,
    0x1000000000000000,
    0x8000000000000000,
    0xFF00000000000000,
]
TEST_VALUES_64_BIT_UINT_LE = [
    pytest.param(
        v,
        get_64bit_bytes(v, "big"),
        get_64bit_bytes(v, "little"),
        get_bitarray(get_64bit_bytes(v, "big")),
        get_bitarray(get_64bit_bytes(v, "little")),
        "little",
        id=f'{v}, "{hex(get_64bit_bytes(v, "little"))}", "{get_bitarray(get_64bit_bytes(v, "little")).to01()}", "little"',
    )
    for v in TEST_VALUES_64_BIT
]
TEST_VALUES_64_BIT_UINT_BE = [
    pytest.param(
        v,
        get_64bit_bytes(v, "big"),
        get_64bit_bytes(v, "little"),
        get_bitarray(get_64bit_bytes(v, "big")),
        get_bitarray(get_64bit_bytes(v, "little")),
        "big",
        id=f'{v}, "{hex(get_64bit_bytes(v, "big"))}", "{get_bitarray(get_64bit_bytes(v, "big")).to01()}", "big"',
    )
    for v in TEST_VALUES_64_BIT
]


def check_int_properties(
    obj: ParseGenericValue[int],
    tst: ParseData,
) -> None:
    assert obj is not None, "Object is None"
    assert obj.name == tst.name, f"{obj}: obj.name is not the expected value ({obj.name} != expected value: {tst.name})"
    assert (
        obj.string_format == tst.string_format
    ), f"{obj}: obj.format is not the expected value ({obj.string_format} != expected value: {tst.string_format})"
    assert (
        obj.bits == tst.bits_data
    ), f"{obj}: obj.bits is not the expected value ({obj.bits} != expected value: {tst.bits_data})"
    assert (
        obj._parent == tst.parent  # pyright:ignore[reportPrivateUsage]
    ), f"{obj}: obj.parent is not the expected value ({obj._parent} != expected value: {tst.parent})"  # pyright:ignore[reportPrivateUsage]
    assert (
        obj.bytes == tst.byte_data
    ), f"{obj}: bytes(obj) is not the expected value ({bytes(obj)!r} != expected value: {tst.byte_data!r})"
    assert (
        obj.endian == tst.endian
    ), f"{obj}: obj.endian is not the expected value ({obj.endian} != expected value: {tst.endian})"


def check_int_children(
    obj: ParseGenericValue[int],
    tst: ParseData,
) -> None:
    assert len(obj._children) == len(tst.children), (  # pyright:ignore[reportPrivateUsage]
        f"{obj}: len(obj.children) is not the expected value "
        + f"({len(obj._children)} != expected value: {len(tst.children)})"  # pyright:ignore[reportPrivateUsage]
    )
    assert obj._children.keys() == tst.children.keys(), (  # pyright:ignore[reportPrivateUsage]
        f"{obj}: obj.children.keys() is not the expected value "
        + f"({obj._children.keys()} != expected value: {tst.children.keys()})"  # pyright:ignore[reportPrivateUsage]
    )
    for key in tst.children.keys():
        assert obj._children[key] == tst.children[key], (  # pyright:ignore[reportPrivateUsage]
            f"{obj}: obj.children[key] is not the expected value "
            + f"({obj._children[key]} != expected value: {tst.children[key]})"  # pyright:ignore[reportPrivateUsage]
        )
        assert obj._children[key]._parent == obj, (  # pyright:ignore[reportPrivateUsage]
            f"{obj}: obj.children[key].parent is not the expected value "
            + f"({obj._children[key]._parent} != expected value: {obj})"  # pyright:ignore[reportPrivateUsage]
        )

    for v in tst.children.values():
        assert v.string in obj.string
        assert v.string in str(obj)
        assert v.string in repr(obj)
    assert tst.name in str(obj)
    assert tst.name in repr(obj)


def check_int_value(
    obj: ParseGenericValue[int],
    tst: ParseData,
) -> None:
    assert (
        obj.value == tst.value
    ), f"{obj}: obj.value is not the expected value ({obj.value} != expected value: {tst.value})"


def check_int_strings(
    obj: ParseGenericValue[int],
    tst: ParseData,
) -> None:
    assert tst.string_format.format(tst.value) == obj.string, (
        f"{obj}: obj.string is not the expected value "
        + f"({tst.string_format.format(tst.value)} != expected value: {obj.string})"
    )
    assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.string in str(
        obj
    ), f"{obj}: obj.string is not in the object's string vale ({obj.string} not in {str(obj)})"
    assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.string in repr(
        obj
    ), f"{obj}: obj.string is not in the object's repr vale ({obj.string} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def check_int(
    obj: ParseGenericValue[int],
    tst: ParseData,
) -> None:
    check_int_value(
        obj=obj,
        tst=tst,
    )
    check_int_properties(
        obj=obj,
        tst=tst,
    )
    check_int_children(
        obj=obj,
        tst=tst,
    )
    check_int_strings(
        obj=obj,
        tst=tst,
    )


class TestUIntField:
    def test_uintfield_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uintfield_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uintfield_set_name(self) -> None:
        value = 0
        byte_data = struct.pack("B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UIntField(
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

    def test_uintfield_set_value(self) -> None:
        value1 = 0
        byte_data1 = struct.pack("B", value1)
        bits_data1 = bitarray(endian="big")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        byte_data2 = struct.pack("B", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
            name="test",
            value=value1,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UIntField(
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

    def test_uintfield_set_bits(self) -> None:
        value1 = 0
        byte_data1 = struct.pack("B", value1)
        bits_data1 = bitarray(endian="big")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        byte_data2 = struct.pack("b", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
            name="test",
            value=value1,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UIntField(
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

    def test_uintfield_set_parent(self) -> None:
        value = 0
        byte_data = struct.pack("B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )
        tst.parent = UInt8Field(name="parent")
        obj._parent = tst.parent  # pyright:ignore[reportPrivateUsage]
        check_int(
            obj=obj,
            tst=tst,
        )


class TestUInt08:
    def test_uint8field_create_empty_big_endian(self) -> None:
        endian: endianT = "big"
        value = 0
        byte_data = struct.pack(">B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT8_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt8Field(
            name=tst.name,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint8field_create_empty_little_endian(self) -> None:
        endian: endianT = "little"
        value = 0
        byte_data = struct.pack("<B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT8_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt8Field(
            name=tst.name,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_08_BIT_UINT_BE,
    )
    def test_uint8field_create_parse_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT8_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt8Field(
            name=tst.name,
            data=byte_data_be,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_08_BIT_UINT_LE,
    )
    def test_uint8field_create_parse_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT8_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt8Field(
            name=tst.name,
            data=byte_data_le,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint8field_create_parse_short(self) -> None:
        value1 = 0xFFFF
        value2 = 0xFF
        byte_data1 = struct.pack("H", value1)
        byte_data2 = struct.pack("B", value2)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        name = "test"
        obj = UInt8Field(
            name=name,
            data=byte_data1,
            endian=DEFAULT_ENDIANNESS,
        )

        assert obj.bits == bits_data2
        assert obj.bytes == byte_data2

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_08_BIT_UINT_BE,
    )
    def test_uint8field_create_init_value_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT8_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            children=OrderedDict(),
            endian=endian,
        )
        obj = UInt8Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_08_BIT_UINT_LE,
    )
    def test_uint8field_create_init_value_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT8_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            children=OrderedDict(),
            endian=endian,
        )
        obj = UInt8Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint8field_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt8Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint8field_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100
        obj = UInt8Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt16:
    def test_uint16field_create_empty_big_endian(self) -> None:
        endian: endianT = "big"
        value = 0
        byte_data = struct.pack(">H", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint16field_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<H", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_16_BIT_UINT_BE,
    )
    def test_uint16field_create_parse_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            data=byte_data_be,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_16_BIT_UINT_LE,
    )
    def test_uint16field_create_parse_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            data=byte_data_le,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_16_BIT_UINT_LE,
    )
    def test_uint16field_create_init_value_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_16_BIT_UINT_BE,
    )
    def test_uint16field_create_init_value_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint16field_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint16field_assign_invalid_value(self) -> None:
        name = "test"
        value = 0x10000
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt24:
    def test_uint24field_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">I", value)[1:]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint24field_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<I", value)[:-1]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_24_BIT_UINT_BE,
    )
    def test_uint24field_create_parse_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            data=byte_data_be,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_24_BIT_UINT_LE,
    )
    def test_uint24field_create_parse_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            data=byte_data_le,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_24_BIT_UINT_BE,
    )
    def test_uint24field_create_init_value_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_24_BIT_UINT_LE,
    )
    def test_uint24field_create_init_value_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint24field_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint24field_assign_invalid_value(self) -> None:
        name = "test"
        value = 0x1000000
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt32:
    def test_uint32field_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">I", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint32field_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<I", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_32_BIT_UINT_BE,
    )
    def test_uint32field_create_parse_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            data=byte_data_be,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_32_BIT_UINT_LE,
    )
    def test_uint32field_create_parse_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            data=byte_data_le,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_32_BIT_UINT_BE,
    )
    def test_uint32field_create_init_value_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_32_BIT_UINT_LE,
    )
    def test_uint32field_create_init_value_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint32field_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt32Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint32field_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100000000
        obj = UInt32Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt64:
    def test_uint64field_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">Q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint64field_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<Q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_64_BIT_UINT_BE,
    )
    def test_uint64field_create_parse_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            data=byte_data_be,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_64_BIT_UINT_LE,
    )
    def test_uint64field_create_parse_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            data=byte_data_le,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_64_BIT_UINT_BE,
    )
    def test_uint64field_create_init_value_big_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data_be,
            bits_data=bits_data_be,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        [
            "value",
            "byte_data_be",
            "byte_data_le",
            "bits_data_be",
            "bits_data_le",
            "endian",
        ],
        TEST_VALUES_64_BIT_UINT_LE,
    )
    def test_uint64field_create_init_value_little_endian(
        self,
        value: int,
        byte_data_be: bytes,
        byte_data_le: bytes,
        bits_data_be: bitarray,
        bits_data_le: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data_le,
            bits_data=bits_data_le,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint64field_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt64Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint64field_set_value_invalid_value(self) -> None:
        name = "test"
        value = -900000000001
        obj = UInt64Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value
