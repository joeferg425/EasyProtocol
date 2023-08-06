# flake8:noqa
from __future__ import annotations

import struct
from typing import Any

import pytest
from bitarray import bitarray
from parse_data import ParseData

from easyprotocol.base.base import DEFAULT_ENDIANNESS
from easyprotocol.fields.array import ArrayFieldGeneric
from easyprotocol.fields.unsigned_int import BoolField, UInt8Field


def check_array_strings(
    obj: ArrayFieldGeneric[Any],
    tst: ParseData,
) -> None:
    assert len(obj.value_as_string) > 0, (
        f"{obj}: obj.value_as_string is not the expected value " + f"(? != expected value: {obj.value_as_string})"
    )
    assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.value_as_string in str(
        obj
    ), f"{obj}: obj.value_as_string is not in the object's string vale ({obj.value_as_string} not in {str(obj)})"
    assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.value_as_string in repr(
        obj
    ), f"{obj}: obj.value_as_string is not in the object's repr vale ({obj.value_as_string} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def check_array_value(
    obj: ArrayFieldGeneric[int],
    tst: ParseData,
) -> None:
    assert (
        obj.value_list == tst.value
    ), f"{obj}: obj.value is not the expected value ({obj.value} != expected value: {tst.value})"


def check_array_properties(
    obj: ArrayFieldGeneric[int],
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
        obj.value_as_bytes == tst.byte_data
    ), f"{obj}: bytes(obj) is not the expected value ({bytes(obj)!r} != expected value: {tst.byte_data!r})"
    assert (
        obj.endian == tst.endian
    ), f"{obj}: obj.endian is not the expected value ({obj.endian} != expected value: {tst.endian})"


def check_array(
    obj: ArrayFieldGeneric[Any],
    tst: ParseData,
) -> None:
    check_array_value(
        obj=obj,
        tst=tst,
    )
    check_array_properties(
        obj=obj,
        tst=tst,
    )
    check_array_strings(
        obj=obj,
        tst=tst,
    )


class TestArray:
    def test_array_create_empty_int_count(self) -> None:
        value: list[Any] = []
        byte_data = b""
        bits_data = bitarray()
        count = 0
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ArrayFieldGeneric(
            name=tst.name,
            count=count,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        check_array(
            obj=obj,
            tst=tst,
        )

    def test_array_create_empty_field_count(self) -> None:
        value: list[Any] = []
        byte_data = b""
        bits_data = bitarray()
        count = UInt8Field(name="count")
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ArrayFieldGeneric(
            name=tst.name,
            count=count,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        check_array(
            obj=obj,
            tst=tst,
        )

    def test_array_create_one_int(self) -> None:
        name = "parent"
        name = "array"
        obj = ArrayFieldGeneric(
            name=name,
            count=1,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        data = b"\x00"
        obj.parse(data=data)
        assert obj.value_list == [0]

    def test_array_create_one_field(self) -> None:
        name = "parent"
        name = "array"
        count = UInt8Field(
            name="f",
            default=2,
        )
        obj = ArrayFieldGeneric(
            name=name,
            count=count,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        data = b"\x00\x00"
        obj.parse(data=data)
        assert obj.value_list == [0, 0]

    def test_array_create_two_defaults(self) -> None:
        name = "parent"
        name = "array"
        f1 = UInt8Field(
            name="f",
            default=1,
        )
        obj = ArrayFieldGeneric(
            name=name,
            count=2,
            array_item_class=UInt8Field,
            array_item_default=f1,
        )
        data = b"\x00\x00"
        obj.parse(data=data)
        assert obj.value_list == [0, 0]

    def test_array_create_three(self) -> None:
        name = "parent"
        # f1_name = "count"
        # f1 = UInt8Field(name=f1_name)
        name = "array"
        obj = ArrayFieldGeneric(
            name=name,
            count=3,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        data = b"\x00\x01\x02"
        # obj = ParseList(name=name, children=[f1, f2])
        obj.parse(data=data)

        # assert f1.value == 3
        assert obj.value_list == [0, 1, 2]

    def test_array_create_invalid(self) -> None:
        name = "parent"
        # f1_name = "count"
        # f1 = ParseList(name=f1_name)
        name = "array"
        obj = ArrayFieldGeneric(
            name=name,
            count=3,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        data = b"\x00\x03"
        with pytest.raises(IndexError):
            # obj = ParseList(name=name, children=[f1, obj])
            obj.parse(data=data)

    def test_array_of_booleans(self) -> None:
        name = "parent"
        count = 8
        name = "array"
        obj = ArrayFieldGeneric(
            name=name,
            count=count,
            array_item_class=BoolField,
            array_item_default=0,
        )
        value = 0b10100010
        byte_data = struct.pack("B", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        # obj = ParseList(name=name, children=[f2])
        obj.parse(data=byte_data)

        # assert obj.bytes_value == byte_data
        assert obj.bits == bits_data

    def test_array_set_name(self) -> None:
        value: list[Any] = []
        byte_data = b""
        bits_data = bitarray()
        count = 0
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ArrayFieldGeneric(
            name=tst.name,
            count=count,
            array_item_class=BoolField,
            array_item_default=0,
        )
        check_array(
            obj=obj,
            tst=tst,
        )

        tst.name = "new_name"
        obj.name = tst.name
        check_array(
            obj=obj,
            tst=tst,
        )

    def test_array_set_parent(self) -> None:
        value: list[Any] = [0, 0]
        byte_data1 = bytes(value)
        bits_data1 = bitarray()
        bits_data1.frombytes(byte_data1)
        count = 2
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ArrayFieldGeneric(
            name=tst.name,
            count=count,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        check_array(
            obj=obj,
            tst=tst,
        )

        tst.parent = UInt8Field(name="parent")
        obj.parent = tst.parent
        check_array(
            obj=obj,
            tst=tst,
        )

    def test_array_set_value_list_int(self) -> None:
        value0: list[Any] = [0, 0]
        byte_data0 = bytes(value0)
        bits_data0 = bitarray()
        bits_data0.frombytes(byte_data0)
        value1: list[Any] = [72, 13]
        byte_data1 = bytes(value1)
        bits_data1 = bitarray()
        bits_data1.frombytes(byte_data1)
        count = 2
        tst = ParseData(
            name="test",
            value=value0,
            string_format="{}",
            byte_data=byte_data0,
            bits_data=bits_data0,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ArrayFieldGeneric(
            name=tst.name,
            count=count,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        check_array(
            obj=obj,
            tst=tst,
        )

        tst.parent = UInt8Field(name="parent")
        obj.parent = tst.parent
        check_array(
            obj=obj,
            tst=tst,
        )

        obj.value = value1
        tst.bits_data = bits_data1
        tst.byte_data = byte_data1
        tst.value = value1
        check_array(
            obj=obj,
            tst=tst,
        )

    def test_array_set_value_list_base_field(self) -> None:
        value0: list[Any] = [0, 0]
        byte_data0 = bytes(value0)
        bits_data0 = bitarray()
        bits_data0.frombytes(byte_data0)
        value1: list[UInt8Field] = [UInt8Field(name="f1", default=12)]
        byte_data1 = bytes([v.value for v in value1])
        bits_data1 = bitarray()
        bits_data1.frombytes(byte_data1)
        count = 2
        tst = ParseData(
            name="test",
            value=value0,
            string_format="{}",
            byte_data=byte_data0,
            bits_data=bits_data0,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ArrayFieldGeneric(
            name=tst.name,
            count=count,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        check_array(
            obj=obj,
            tst=tst,
        )

        tst.parent = UInt8Field(name="parent")
        obj.parent = tst.parent
        check_array(
            obj=obj,
            tst=tst,
        )

        obj.value = value1
        tst.bits_data = bits_data1
        tst.byte_data = byte_data1
        tst.value = [v.value for v in value1]
        check_array(
            obj=obj,
            tst=tst,
        )

    def test_array_set_value_dict_int(self) -> None:
        value0: list[Any] = [0, 0]
        byte_data0 = bytes(value0)
        bits_data0 = bitarray()
        bits_data0.frombytes(byte_data0)
        value1: dict[str, int] = {"0": 1, "1": 2}
        byte_data1 = bytes(value1.values())
        bits_data1 = bitarray()
        bits_data1.frombytes(byte_data1)
        count = 2
        tst = ParseData(
            name="test",
            value=value0,
            string_format="{}",
            byte_data=byte_data0,
            bits_data=bits_data0,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ArrayFieldGeneric(
            name=tst.name,
            count=count,
            array_item_class=UInt8Field,
            array_item_default=0,
        )
        check_array(
            obj=obj,
            tst=tst,
        )

        tst.parent = UInt8Field(name="parent")
        obj.parent = tst.parent
        check_array(
            obj=obj,
            tst=tst,
        )

        obj.value = list(value1.values())
        tst.bits_data = bits_data1
        tst.byte_data = byte_data1
        tst.value = list(value1.values())
        check_array(
            obj=obj,
            tst=tst,
        )
