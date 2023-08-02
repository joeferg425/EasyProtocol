# flake8:noqa
from __future__ import annotations

import struct
from typing import Any, Sequence

import pytest
from bitarray import bitarray
from parse_data import ParseData

from easyprotocol.base.base import DEFAULT_ENDIANNESS, BaseField
from easyprotocol.base.list import ListField
from easyprotocol.base.value import ValueFieldGeneric
from easyprotocol.fields import UInt8Field
from easyprotocol.fields.unsigned_int import UIntField


def check_ParseFieldList_value(
    obj: ListField,
    tst: ParseData,
) -> None:
    assert len(obj.value) == len(tst.value), (
        f"{obj}: len(obj.value) is not the expected value " + f"({len(obj.value)} != expected value: {len(tst.value)})"
    )
    for i in range(len(tst.value)):
        assert obj.value[i] == tst.value[i], (
            f"{obj}: obj.value[{i}] is not the expected value " + f"({obj.value[i]} != expected value: {tst.value[i]})"
        )


def check_ParseFieldList_properties(
    obj: ListField,
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
        obj.parent == tst.parent
    ), f"{obj}: obj.parent is not the expected value ({obj.parent} != expected value: {tst.parent})"
    assert (
        bytes(obj) == tst.byte_data
    ), f"{obj}: bytes(obj) is not the expected value ({bytes(obj)!r} != expected value: {tst.byte_data!r})"
    assert (
        obj.endian == tst.endian
    ), f"{obj}: obj.endian is not the expected value ({obj.endian} != expected value: {tst.endian})"


def check_ParseFieldList_children(
    obj: ListField,
    tst: ParseData,
) -> None:
    assert len(obj.children) == len(tst.children), (
        f"{obj}: len(obj.children) is not the expected value "
        + f"({len(obj.children)} != expected value: {len(tst.children)})"
    )
    assert obj.children.keys() == tst.children.keys(), (
        f"{obj}: obj.children.keys() is not the expected value "
        + f"({obj.children.keys()} != expected value: {tst.children.keys()})"
    )
    for key in tst.children.keys():
        assert obj.children[key] == tst.children[key], (
            f"{obj}: obj.children[key] is not the expected value "
            + f"({obj.children[key]} != expected value: {tst.children[key]})"
        )
        assert obj.children[key].parent == obj, (
            f"{obj}: obj.children[key].parent is not the expected value "
            + f"({obj.children[key].parent} != expected value: {obj})"
        )

    for v in tst.children.values():
        assert v.value_as_string in obj.value_as_string
        assert v.value_as_string in str(obj)
        assert v.value_as_string in repr(obj)
    assert tst.name in str(obj)
    assert tst.name in repr(obj)


def ParseFieldList_tests(
    obj: ListField,
    tst: ParseData,
) -> None:
    check_ParseFieldList_properties(
        obj=obj,
        tst=tst,
    )
    check_ParseFieldList_value(
        obj=obj,
        tst=tst,
    )
    check_ParseFieldList_children(
        obj=obj,
        tst=tst,
    )


class TestParseFieldList:
    def test_ParseFieldList_create_empty(self) -> None:
        value: list[Any] = []
        byte_data = b""
        bits_data = bitarray()
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ListField(
            name=tst.name,
        )
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_create_children_list(self) -> None:
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        f2_value = 0
        f2_data = int.to_bytes(f2_value, length=1, byteorder="big", signed=False)
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name)
        bits_data = f2.bits + f1.bits
        byte_data = bytes(f2) + bytes(f1)
        value: list[Any] = [f1, f2]
        children_list: list[ValueFieldGeneric[Any]] = [f1, f2]
        tst = ParseData(
            name="test",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            string_format="{}",
            parent=None,
            children=dict({f1.name: f1, f2.name: f2}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ListField(
            name=tst.name,
            default=children_list,
        )
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_create_children_dict(self) -> None:
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        f2_value = 0
        f2_data = int.to_bytes(f2_value, length=1, byteorder="big", signed=False)
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name)
        bits_data = f2.bits + f1.bits
        byte_data = bytes(f2) + bytes(f1)
        values: list[Any] = [f1, f2]
        tst = ParseData(
            name="test",
            value=values,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict({f1.name: f1, f2.name: f2}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ListField(
            name=tst.name,
            default=tst.children,
        )
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_create_parse_single_field(self) -> None:
        f1_value = 255
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        byte_data = f1_data
        bits_data = f1_bits
        values = [f1]
        tst = ParseData(
            name="test",
            value=values,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict({f1.name: f1}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ListField(
            name=tst.name,
            default=[f1],
            data=tst.byte_data,
        )
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_create_parse_multi_field(self) -> None:
        init_value = 0
        init_data = int.to_bytes(init_value, length=1, byteorder="big", signed=False)
        init_bits = bitarray()
        init_bits.frombytes(init_data)
        f1_name = "f1"
        # f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        f2_name = "f2"
        # f2_value = 187
        f2_data = b"\xbb"
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f2 = UInt8Field(name=f2_name)
        f3_name = "f3"
        # f3_value = 204
        f3_data = b"\xcc"
        f3_bits = bitarray()
        f3_bits.frombytes(f3_data)
        f3 = UInt8Field(name=f3_name)
        byte_data = f1_data + f2_data + f3_data
        bits_data = f1_bits + f2_bits + f3_bits
        values = [f1, f2, f3]
        tst = ParseData(
            name="test",
            value=values,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict({f1.name: f1, f2.name: f2, f3.name: f3}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ListField(
            name=tst.name,
            default=[f1, f2, f3],
            data=tst.byte_data,
        )

        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_create_parse_multi_bit_field(self) -> None:
        f1_name = "f1"
        f1_bit_count = 6
        f1_value = 0x3F
        f1_byte = struct.pack("B", f1_value)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_byte)
        f1_bits = f1_bits[:f1_bit_count]
        f1 = UIntField(
            name=f1_name,
            bit_count=f1_bit_count,
        )

        f2_bit_count = 6
        f2_name = "f2"
        f2_value = 0x00
        f2_data = struct.pack("B", f2_value)
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f2_bits = f2_bits[:f2_bit_count]
        f2 = UIntField(
            name=f2_name,
            bit_count=f1_bit_count,
        )

        f3_bit_count = 6
        f3_name = "f3"
        f3_value = 0x3F
        f3_data = struct.pack("B", f3_value)
        f3_bits = bitarray()
        f3_bits.frombytes(f3_data)
        f3_bits = f3_bits[:f3_bit_count]
        f3 = UIntField(
            name=f3_name,
            bit_count=f1_bit_count,
        )

        f4_bit_count = 6
        f4_name = "f4"
        f4_value = 0x00
        f4_data = struct.pack("B", f4_value)
        f4_bits = bitarray()
        f4_bits.frombytes(f4_data)
        f4_bits = f4_bits[:f4_bit_count]
        f4 = UIntField(
            name=f4_name,
            bit_count=f1_bit_count,
        )

        byte_data = b"\x3F\xF0\x03"
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        values = [f1, f2, f3, f4]
        tst = ParseData(
            name="test",
            value=values,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict({f1.name: f1, f2.name: f2, f3.name: f3, f4.name: f4}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ListField(
            name=tst.name,
            default=[f1, f2, f3, f4],
            data=tst.byte_data,
        )

        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_parse_single_field(self) -> None:
        f1_value = 255
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        byte_data1 = b"\x00"
        bits_data1 = bitarray()
        bits_data1.frombytes(byte_data1)
        values1 = [f1]
        byte_data2 = f1_data
        bits_data2 = f1_bits
        values2 = [f1]
        tst = ParseData(
            name="test",
            value=values1,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            children=dict({f1.name: f1}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ListField(
            name=tst.name,
            default=[f1],
        )
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

        obj.parse(data=byte_data2)
        tst.value = values2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_parse_multi_field(self) -> None:
        init_value = 0
        init_data = int.to_bytes(init_value, length=1, byteorder="big", signed=False)
        init_bits = bitarray()
        init_bits.frombytes(init_data)
        f1_name = "f1"
        # f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        f2_name = "f2"
        # f2_value = 187
        f2_data = b"\xbb"
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f2 = UInt8Field(name=f2_name)
        f3_name = "f3"
        # f3_value = 204
        f3_data = b"\xcc"
        f3_bits = bitarray()
        f3_bits.frombytes(f3_data)
        f3 = UInt8Field(name=f3_name)
        byte_data1 = b"\x00\x00\x00"
        bits_data1 = bitarray()
        bits_data1.frombytes(byte_data1)
        values1 = [f1, f2, f3]
        byte_data2 = f1_data + f2_data + f3_data
        bits_data2 = f1_bits + f2_bits + f3_bits
        values2 = [f1, f2, f3]
        tst = ParseData(
            name="test",
            value=values1,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            children=dict({f1.name: f1, f2.name: f2, f3.name: f3}),
            endian=DEFAULT_ENDIANNESS,
        )

        obj = ListField(
            name=tst.name,
            default=[f1, f2, f3],
        )
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

        obj.parse(data=byte_data2)
        tst.value = values2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_set_name(self) -> None:
        name1 = "test"
        name2 = "new_name"
        byte_data = b""
        bits_data = bitarray()
        values: list[Any] = []
        tst = ParseData(
            name=name1,
            value=values,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ListField(
            name=tst.name,
        )
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )
        tst.name = name2
        obj.name = tst.name
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_set_value(self) -> None:
        f1_value = 2
        f2_value = 7
        f3_value = 15
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f2_data = int.to_bytes(f2_value, length=1, byteorder="big", signed=False)
        f3_data = int.to_bytes(f3_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f3_bits = bitarray()
        f3_bits.frombytes(f3_data)
        f1_name = "f1"
        f2_name = "f7"
        f3_name = "X"
        f1 = UInt8Field(name=f1_name, default=f1_value)
        f2 = UInt8Field(name=f2_name, default=f2_value)
        f3 = UInt8Field(name=f3_name, default=f3_value)
        bits_data0 = bitarray()
        byte_data0 = b""
        bits_data1 = bitarray()
        bits_data1.frombytes(f1_data)
        byte_data1 = f1_data
        bits_data2 = bitarray()
        bits_data2.frombytes(f2_data)
        byte_data2 = f2_data
        bits_data3 = bitarray()
        bits_data3.frombytes(f3_data)
        byte_data3 = f3_data
        values0: Sequence[Any] = []
        values1: Sequence[Any] = [f1]
        values2: Sequence[Any] = [f2]
        values3: Sequence[Any] = [f3]
        children0: dict[str, BaseField] = dict()
        children1: dict[str, BaseField] = dict({f1.name: f1})
        children2: dict[str, BaseField] = dict({f2.name: f2})
        children3: dict[str, BaseField] = dict({f3.name: f3})
        tst = ParseData(
            name="test",
            value=values0,
            string_format="{}",
            byte_data=byte_data0,
            bits_data=bits_data0,
            parent=None,
            children=children0,
            endian=DEFAULT_ENDIANNESS,
        )

        obj = ListField(
            name=tst.name,
        )
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

        obj.value = [f1]
        tst.value = values1
        tst.bits_data = bits_data1
        tst.byte_data = byte_data1
        tst.children = children1
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

        obj.value = [f2]
        tst.value = values2
        tst.bits_data = bits_data2
        tst.byte_data = byte_data2
        tst.children = children2
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

        obj.value = {f3.name: f3}
        tst.value = values3
        tst.bits_data = bits_data3
        tst.byte_data = byte_data3
        tst.children = children3
        ParseFieldList_tests(
            obj=obj,
            tst=tst,
        )

    def test_ParseFieldList_remove(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name)
        obj = ListField(name=name, default=[f1, f2])

        assert len(obj) == 2
        assert f1.parent == obj
        assert f2.parent == obj
        del obj[1]
        assert len(obj) == 1
        assert f2.parent is None

    def test_ParseFieldList_set_item(self) -> None:
        name = "test"
        f1_name = "f1"
        f1_value = 1
        f1 = UInt8Field(name=f1_name, default=f1_value)
        f2_name = "f2"
        f2_value = 2
        f2 = UInt8Field(name=f2_name, default=f2_value)
        f3_name = "f3"
        f3_value = 3
        f3 = UInt8Field(name=f3_name, default=f3_value)
        f4_name = "f4"
        f4_value = 4
        f4 = UInt8Field(name=f4_name, default=f4_value)
        f5_name = "f5"
        f5_value = 5
        f5 = UInt8Field(name=f5_name, default=f5_value)
        f6_name = "f6"
        f6_value = 6
        f6 = UInt8Field(name=f6_name, default=f6_value)
        obj = ListField(name=name, default=[f1, f2, f3])

        assert f1.parent == obj
        assert f2.parent == obj
        assert f3.parent == obj
        assert f4.parent is None
        assert len(obj) == 3
        assert obj[2] == f3
        assert obj[2].value == f3.value

        obj[2] = f4
        assert f4.parent == obj
        assert len(obj) == 3
        assert obj[2] == f4
        assert obj[2].value == f4.value

        obj[0:2] = [f5, f6]
        assert f1.parent == None
        assert f2.parent == None
        assert f5.parent == obj
        assert f6.parent == obj
        assert len(obj) == 3
        assert obj[2] == f4
        assert obj[2].value == f4.value

        with pytest.raises(TypeError):
            obj[7.0] = "nothing"  # pyright:ignore[reportGeneralTypeIssues]

    def test_ParseFieldList_get_item(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name, default=1)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name, default=2)
        f3_name = "f3"
        f3 = UInt8Field(name=f3_name, default=3)
        f3_also = UInt8Field(name=f3_name, default=17)
        obj = ListField(name=name, default=[f1, f2, f3])

        assert f1.parent == obj
        assert f2.parent == obj
        assert f3.parent == obj
        assert f3_also.parent is None
        assert len(obj) == 3
        assert obj[2] == f3
        assert obj[2].value == f3.value
        assert obj[1:] == [f2, f3]

    def test_ParseFieldList_del(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name, default=1)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name, default=2)
        f3_name = "f3"
        f3 = UInt8Field(name=f3_name, default=3)
        obj = ListField(name=name, default=[f1, f2, f3])

        assert f1.parent == obj
        assert f2.parent == obj
        assert f3.parent == obj
        assert len(obj) == 3
        assert obj[2] == f3
        assert obj[2].value == f3.value
        del obj[1:]
        assert f1.parent == obj
        assert f2.parent == None
        assert f3.parent == None
        assert len(obj) == 1
        assert obj[0] == f1
        assert obj[0].value == f1.value

    def test_ParseFieldList_insert(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name, default=1)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name, default=2)
        f3_name = "f3"
        f3 = UInt8Field(name=f3_name, default=3)
        obj = ListField(name=name, default=[f1, f3])

        assert f1.parent == obj
        assert f2.parent is None
        assert f3.parent == obj
        assert len(obj) == 2
        assert obj[0] == f1
        assert obj[0].value == f1.value
        assert obj[1] == f3
        assert obj[1].value == f3.value
        obj.insert(1, f2)
        assert f2.parent == obj
        assert len(obj) == 3
        assert obj[0] == f1
        assert obj[0].value == f1.value
        assert obj[1] == f2
        assert obj[1].value == f2.value
        assert obj[2] == f3
        assert obj[2].value == f3.value

    def test_ParseFieldList_get_concatenated(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name, default=1)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name, default=2)
        f3_name = "f3"
        f3 = UInt8Field(name=f3_name, default=3)
        obj = ListField(name=name, default=[f1, f2, f3])

        with pytest.raises(NotImplementedError):
            obj.get_value_concatenated()

    def test_ParseFieldList_get_value_list(self) -> None:
        name = "test"
        f1_name = "f1"
        f1_value = 1
        f1 = UInt8Field(name=f1_name, default=f1_value)
        f2_name = "f2"
        f2_value = 2
        f2 = UInt8Field(name=f2_name, default=f2_value)
        f3_name = "f3"
        f3_value = 3
        f3 = UInt8Field(name=f3_name, default=f3_value)
        obj = ListField(name=name, default=[f1, f2, f3])

        assert obj.value_list == [f1_value, f2_value, f3_value]

    def test_ParseFieldList_get_value_dict(self) -> None:
        name = "test"
        f1_name = "f1"
        f1_value = 1
        f1 = UInt8Field(name=f1_name, default=f1_value)
        f2_name = "f2"
        f2_value = 2
        f2 = UInt8Field(name=f2_name, default=f2_value)
        f3_name = "f3"
        f3_value = 3
        f3 = UInt8Field(name=f3_name, default=f3_value)
        obj = ListField(name=name, default=[f1, f2, f3])

        assert obj.value_dict == {f1_name: f1_value, f2_name: f2_value, f3_name: f3_value}
