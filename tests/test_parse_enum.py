import struct
from collections import OrderedDict
from enum import IntEnum
from typing import Any

import pytest
from bitarray import bitarray
from parse_data import ParseData
from test_parse_uint import check_int_properties, check_int_value

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS
from easyprotocol.fields.enum import EnumField


def check_enum_strings(
    obj: EnumField[IntEnum],
    tst: ParseData,
) -> None:
    assert tst.string_format.format(tst.value.name) == obj.string, (
        f"{obj}: obj.string is not the expected value "
        + f"({tst.string_format.format(tst.value)} != expected value: {obj.string})"
    )
    assert len(obj.string) > 0, f"{obj}: obj.string is not the expected value " + f"(? != expected value: {obj.string})"
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


def check_enum(
    obj: EnumField[Any],
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
    check_enum_strings(
        obj=obj,
        tst=tst,
    )


class TestEnumerating(IntEnum):
    ZERO = 0b000
    ONE = 0b001
    TWO = 0b010
    THREE = 0b011
    FOUR = 0b100
    FIVE = 0b101
    SIX = 0b110
    SEVEN = 0b111


class TestEnums:
    def test_enum_create_empty_big_endian(self) -> None:
        value = TestEnumerating.ZERO
        bit_count = 2
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = EnumField(
            name=tst.name,
            bit_count=bit_count,
            enum_type=TestEnumerating,
            default=TestEnumerating.ZERO,
        )
        check_enum(
            obj=obj,
            tst=tst,
        )

    def test_enum_create_empty_little_endian(self) -> None:
        value = TestEnumerating.ZERO
        bit_count = 2
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = EnumField(
            name=tst.name,
            bit_count=bit_count,
            enum_type=TestEnumerating,
            default=TestEnumerating.ZERO,
        )
        check_enum(
            obj=obj,
            tst=tst,
        )

    def test_enum_create_parse(self) -> None:
        value = TestEnumerating.THREE
        bit_count = 2
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = EnumField(
            name=tst.name,
            bit_count=bit_count,
            enum_type=TestEnumerating,
            data=tst.byte_data,
            default=TestEnumerating.ZERO,
        )
        check_enum(
            obj=obj,
            tst=tst,
        )

    def test_enum_create_truncate(self) -> None:
        bit_count = 2
        value1 = TestEnumerating.SEVEN
        byte_data1 = struct.pack("B", value1.value)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data1 = bits_data1[:bit_count]
        value2 = TestEnumerating.THREE
        byte_data2 = struct.pack("B", value2.value)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data2 = bits_data2[:bit_count]
        tst = ParseData(
            name="test",
            value=value2,
            string_format="{}",
            byte_data=byte_data2,
            bits_data=bits_data2,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = EnumField(
            name=tst.name,
            bit_count=bit_count,
            enum_type=TestEnumerating,
            data=byte_data1,
            default=TestEnumerating.ZERO,
        )
        check_enum(
            obj=obj,
            tst=tst,
        )

    def test_enum_create_invalid(self) -> None:
        with pytest.raises(TypeError):
            EnumField(
                name="enum",
                bit_count=4,
                enum_type=TestEnumerating,
                data=tuple((1, 2, "ff")),  # pyright:ignore[reportGeneralTypeIssues]
            )

    def test_enum_set_name(self) -> None:
        value = TestEnumerating.SEVEN
        bit_count = 4
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = EnumField(
            name=tst.name,
            bit_count=bit_count,
            enum_type=TestEnumerating,
            data=tst.byte_data,
            default=TestEnumerating.ZERO,
        )
        check_enum(
            obj=obj,
            tst=tst,
        )

        tst.name = "new_name"
        obj.name = tst.name
        check_enum(
            obj=obj,
            tst=tst,
        )

    def test_enum_set_value(self) -> None:
        value1 = TestEnumerating.ONE
        value2 = TestEnumerating.FOUR
        bit_count = 4
        byte_data1 = struct.pack("B", value1.value)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data1 = bits_data1[:bit_count]
        byte_data2 = struct.pack("B", value2.value)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data2 = bits_data2[:bit_count]
        tst = ParseData(
            name="test",
            value=value1,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = EnumField(
            name=tst.name,
            bit_count=bit_count,
            enum_type=TestEnumerating,
            data=tst.byte_data,
            default=TestEnumerating.ZERO,
        )
        check_enum(
            obj=obj,
            tst=tst,
        )

        obj.value = value2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_enum(
            obj=obj,
            tst=tst,
        )

    def test_enum_set_bits(self) -> None:
        value1 = TestEnumerating.ONE
        value2 = TestEnumerating.SIX
        bit_count = 4
        byte_data1 = struct.pack("B", value1.value)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data1 = bits_data1[:bit_count]
        byte_data2 = struct.pack("B", value2.value)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data2 = bits_data2[:bit_count]
        tst = ParseData(
            name="test",
            value=value1,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = EnumField(
            name=tst.name,
            bit_count=bit_count,
            enum_type=TestEnumerating,
            data=tst.byte_data,
            default=TestEnumerating.ZERO,
        )
        check_enum(
            obj=obj,
            tst=tst,
        )

        obj.bits = bits_data2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_enum(
            obj=obj,
            tst=tst,
        )

    def test_enum_set_parent(self) -> None:
        value = TestEnumerating.FIVE
        bit_count = 4
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = EnumField(
            name=tst.name,
            bit_count=bit_count,
            enum_type=TestEnumerating,
            data=tst.byte_data,
            default=TestEnumerating.ZERO,
        )
        check_enum(
            obj=obj,
            tst=tst,
        )

        tst.parent = EnumField(
            name="parent",
            bit_count=bit_count,
            enum_type=TestEnumerating,
            data=tst.byte_data,
            default=TestEnumerating.ZERO,
        )
        obj.parent = tst.parent
        check_enum(
            obj=obj,
            tst=tst,
        )
