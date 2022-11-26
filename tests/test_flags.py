import struct
from collections import OrderedDict
from enum import IntFlag
from typing import Any

import pytest
from bitarray import bitarray
from test_parse_object import (
    TestData,
    check_parseobject_properties,
    check_parseobject_value,
)

from easyprotocol.base.parse_object import (
    DEFAULT_ENDIANNESS,
    ParseObject,
    ParseObjectGeneric,
)
from easyprotocol.fields.flags import FlagsField


def check_flags_strings(
    obj: FlagsField[IntFlag],
    tst: TestData,
) -> None:

    assert len(obj.formatted_value) > 0, (
        f"{obj}: obj.formatted_value is not the expected value " + f"(? != expected value: {obj.formatted_value})"
    )
    assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.formatted_value in str(
        obj
    ), f"{obj}: obj.formatted_value is not in the object's string vale ({obj.formatted_value} not in {str(obj)})"
    assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.formatted_value in repr(
        obj
    ), f"{obj}: obj.formatted_value is not in the object's repr vale ({obj.formatted_value} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def check_flags(
    obj: FlagsField[Any],
    tst: TestData,
) -> None:
    check_parseobject_value(
        obj=obj,
        tst=tst,
    )
    check_parseobject_properties(
        obj=obj,
        tst=tst,
    )
    check_flags_strings(
        obj=obj,
        tst=tst,
    )


class TestingFlags(IntFlag):
    NONE = 0
    ONE = 1
    TWO = 2
    FOUR = 4
    EIGHT = 8


class TestFlags:
    def test_flags_create_empty(self) -> None:
        bit_count = 2
        value = TestingFlags.NONE
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )

    def test_flags_create_parse_one(self) -> None:
        value = TestingFlags.ONE
        bit_count = 2
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
            data=tst.byte_data,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )

    def test_flags_create_parse_multiple(self) -> None:
        value = TestingFlags.ONE | TestingFlags.TWO | TestingFlags.FOUR | TestingFlags.EIGHT
        bit_count = 4
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
            data=tst.byte_data,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )

    def test_flags_create_truncate(self) -> None:
        value1 = TestingFlags.ONE | TestingFlags.TWO | TestingFlags.FOUR | TestingFlags.EIGHT
        value2 = TestingFlags.ONE | TestingFlags.TWO
        bit_count = 2
        byte_data1 = struct.pack("B", value1.value)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data1 = bits_data1[:bit_count]
        byte_data2 = struct.pack("B", value2.value)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data2 = bits_data2[:bit_count]
        tst = TestData(
            name="test",
            value=value2,
            format="{}",
            byte_data=byte_data2,
            bits_data=bits_data2,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
            data=byte_data2,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )

    def test_flags_create_invalid(self) -> None:
        with pytest.raises(ValueError):
            FlagsField(
                name="invalid",
                bit_count=4,
                flags_type=TestingFlags,
                data="pickles",  # type:ignore
            )

    def test_flags_set_name(self) -> None:
        value = TestingFlags.ONE | TestingFlags.TWO | TestingFlags.FOUR | TestingFlags.EIGHT
        bit_count = 4
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
            data=tst.byte_data,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )

        tst.name = "new_name"
        obj.name = tst.name
        check_flags(
            obj=obj,
            tst=tst,
        )

    def test_flags_set_value(self) -> None:
        value1 = TestingFlags.ONE
        value2 = TestingFlags.ONE | TestingFlags.TWO | TestingFlags.FOUR | TestingFlags.EIGHT
        bit_count = 4
        byte_data1 = struct.pack("B", value1.value)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data1 = bits_data1[:bit_count]
        byte_data2 = struct.pack("B", value2.value)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data2 = bits_data2[:bit_count]
        tst = TestData(
            name="test",
            value=value1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
            data=tst.byte_data,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )

        obj.value = value2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_flags(
            obj=obj,
            tst=tst,
        )

    def test_flags_set_bits(self) -> None:
        value1 = TestingFlags.ONE
        value2 = TestingFlags.ONE | TestingFlags.TWO | TestingFlags.FOUR | TestingFlags.EIGHT
        bit_count = 4
        byte_data1 = struct.pack("B", value1.value)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data1 = bits_data1[:bit_count]
        byte_data2 = struct.pack("B", value2.value)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data2 = bits_data2[:bit_count]
        tst = TestData(
            name="test",
            value=value1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
            data=tst.byte_data,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )

        obj.bits = bits_data2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_flags(
            obj=obj,
            tst=tst,
        )

    def test_flags_set_parent(self) -> None:
        value = TestingFlags.ONE | TestingFlags.TWO | TestingFlags.FOUR | TestingFlags.EIGHT
        bit_count = 4
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
            data=tst.byte_data,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )

        tst.parent = ParseObject(name="parent")
        obj.parent = tst.parent
        check_flags(
            obj=obj,
            tst=tst,
        )

    def test_flags_set_children(self) -> None:
        value = TestingFlags.ONE | TestingFlags.TWO | TestingFlags.FOUR | TestingFlags.EIGHT
        bit_count = 4
        byte_data = struct.pack("B", value.value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:bit_count]
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=OrderedDict(),
        )
        obj = FlagsField(
            name=tst.name,
            bit_count=bit_count,
            flags_type=TestingFlags,
            data=tst.byte_data,
        )
        check_flags(
            obj=obj,
            tst=tst,
        )
        child = ParseObject(name="child`")
        with pytest.raises(NotImplementedError):
            obj.children = OrderedDict({child.name: child})
