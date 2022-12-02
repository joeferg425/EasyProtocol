import struct
from collections import OrderedDict
from typing import Literal

import pytest
from bitarray import bitarray
from parse_data import ParseData

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS
from easyprotocol.base.parse_generic_value import ParseGenericValue
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
    bits = bitarray(endian="little")
    bits.frombytes(b)
    return bits


TEST_VALUES_08_BIT = [
    b"\x00",
    b"\x01",
    b"\x10",
    b"\x80",
    b"\xFF",
]
TEST_VALUES_08_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<B", v)[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_08_BIT
]
TEST_VALUES_08_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">B", v)[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_08_BIT
]
TEST_VALUES_16_BIT = [
    b"\x00\x00",
    b"\x00\x01",
    b"\x00\x10",
    b"\x00\x80",
    b"\x00\xFF",
    b"\x01\x00",
    b"\x08\x00",
    b"\x10\x00",
    b"\x80\x00",
    b"\xFF\x00",
]
TEST_VALUES_16_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<H", v)[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_16_BIT
]
TEST_VALUES_16_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">H", v)[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_16_BIT
]
TEST_VALUES_24_BIT = [
    b"\x00\x00\x00",
    b"\x00\x00\x01",
    b"\x00\x00\x10",
    b"\x00\x00\x80",
    b"\x00\x00\xFF",
    b"\x00\x01\x00",
    b"\x00\x10\x00",
    b"\x00\x80\x00",
    b"\x00\xFF\x00",
    b"\x01\x00\x00",
    b"\x10\x00\x00",
    b"\x80\x00\x00",
    b"\xFF\x00\x00",
]
TEST_VALUES_24_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<I", v + b"\x00")[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_24_BIT
]
TEST_VALUES_24_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">I", b"\x00" + v)[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_24_BIT
]
TEST_VALUES_32_BIT = [
    b"\x00\x00\x00\x00",
    b"\x00\x00\x00\x01",
    b"\x00\x00\x00\x10",
    b"\x00\x00\x00\x80",
    b"\x00\x00\x00\xFF",
    b"\x00\x00\x01\x00",
    b"\x00\x00\x10\x00",
    b"\x00\x00\x80\x00",
    b"\x00\x00\xFF\x00",
    b"\x00\x01\x00\x00",
    b"\x00\x10\x00\x00",
    b"\x00\x80\x00\x00",
    b"\x00\xFF\x00\x00",
    b"\x01\x00\x00\x00",
    b"\x10\x00\x00\x00",
    b"\x80\x00\x00\x00",
    b"\xFF\x00\x00\x00",
]
TEST_VALUES_32_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<I", v)[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_32_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">I", v)[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_64_BIT = [
    b"\x00\x00\x00\x00\x00\x00\x00\x00",
    b"\x00\x00\x00\x00\x00\x00\x00\x01",
    b"\x00\x00\x00\x00\x00\x00\x00\x10",
    b"\x00\x00\x00\x00\x00\x00\x00\x80",
    b"\x00\x00\x00\x00\x00\x00\x00\xFF",
    b"\x00\x00\x00\x00\x00\x00\x01\x00",
    b"\x00\x00\x00\x00\x00\x00\x10\x00",
    b"\x00\x00\x00\x00\x00\x00\x80\x00",
    b"\x00\x00\x00\x00\x00\x00\xFF\x00",
    b"\x00\x00\x00\x00\x00\x01\x00\x00",
    b"\x00\x00\x00\x00\x00\x10\x00\x00",
    b"\x00\x00\x00\x00\x00\x80\x00\x00",
    b"\x00\x00\x00\x00\x00\xFF\x00\x00",
    b"\x00\x00\x00\x00\x01\x00\x00\x00",
    b"\x00\x00\x00\x00\x10\x00\x00\x00",
    b"\x00\x00\x00\x00\x80\x00\x00\x00",
    b"\x00\x00\x00\x00\xFF\x00\x00\x00",
    b"\x00\x00\x00\x00\x00\x00\x00\x00",
    b"\x00\x00\x00\x01\x00\x00\x00\x00",
    b"\x00\x00\x00\x10\x00\x00\x00\x00",
    b"\x00\x00\x00\x80\x00\x00\x00\x00",
    b"\x00\x00\x00\xFF\x00\x00\x00\x00",
    b"\x00\x00\x01\x00\x00\x00\x00\x00",
    b"\x00\x00\x10\x00\x00\x00\x00\x00",
    b"\x00\x00\x80\x00\x00\x00\x00\x00",
    b"\x00\x00\xFF\x00\x00\x00\x00\x00",
    b"\x00\x01\x00\x00\x00\x00\x00\x00",
    b"\x00\x10\x00\x00\x00\x00\x00\x00",
    b"\x00\x80\x00\x00\x00\x00\x00\x00",
    b"\x00\xFF\x00\x00\x00\x00\x00\x00",
    b"\x01\x00\x00\x00\x00\x00\x00\x00",
    b"\x10\x00\x00\x00\x00\x00\x00\x00",
    b"\x80\x00\x00\x00\x00\x00\x00\x00",
    b"\xFF\x00\x00\x00\x00\x00\x00\x00",
]
TEST_VALUES_64_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<Q", v)[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_64_BIT
]
TEST_VALUES_64_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">Q", v)[0],
        get_bitarray(v),
        "big",
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
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        byte_data2 = struct.pack("B", value2)
        bits_data2 = bitarray(endian="little")
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
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        byte_data2 = struct.pack("b", value2)
        bits_data2 = bitarray(endian="little")
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

        obj.bits = bits_data2
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
        endian: Literal["big", "little"] = "big"
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
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint8field_create_empty_little_endian(self) -> None:
        endian: Literal["big", "little"] = "little"
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
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_UINT_BE,
    )
    def test_uint8field_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
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
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_UINT_LE,
    )
    def test_uint8field_create_parse_little_endian(
        self,
        byte_data: bytes,
        value: int,
        bits_data: bitarray,
        endian: Literal["big", "little"],
    ) -> None:
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
            data=tst.byte_data,
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
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_UINT_BE,
    )
    def test_uint8field_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT8_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian=endian,
        )
        obj = UInt8Field(
            name=tst.name,
            default=tst.value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_UINT_LE,
    )
    def test_uint8field_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT8_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian=endian,
        )
        obj = UInt8Field(
            name=tst.name,
            default=tst.value,
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
        endian: Literal["big", "little"] = "big"
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
            endian=tst.endian,
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
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_16_BIT_UINT_BE,
    )
    def test_uint16field_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
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
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_16_BIT_UINT_LE,
    )
    def test_uint16field_create_parse_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
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
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_16_BIT_UINT_LE,
    )
    def test_uint16field_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
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
            default=tst.value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_16_BIT_UINT_BE,
    )
    def test_uint16field_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
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
            default=tst.value,
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
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_24_BIT_UINT_BE,
    )
    def test_uint24field_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_24_BIT_UINT_LE,
    )
    def test_uint24field_create_parse_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_24_BIT_UINT_BE,
    )
    def test_uint24field_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            default=tst.value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_24_BIT_UINT_LE,
    )
    def test_uint24field_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            default=tst.value,
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
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_UINT_BE,
    )
    def test_uint32field_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_UINT_LE,
    )
    def test_uint32field_create_parse_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_UINT_BE,
    )
    def test_uint32field_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            default=tst.value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_UINT_LE,
    )
    def test_uint32field_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            default=tst.value,
            endian=tst.endian,
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
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_64_BIT_UINT_BE,
    )
    def test_uint64field_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_64_BIT_UINT_LE,
    )
    def test_uint64field_create_parse_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_64_BIT_UINT_BE,
    )
    def test_uint64field_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            default=tst.value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_64_BIT_UINT_LE,
    )
    def test_uint64field_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            default=tst.value,
            endian=tst.endian,
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
