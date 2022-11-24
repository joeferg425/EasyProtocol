from __future__ import annotations

import struct
from collections import OrderedDict
from typing import Any

import pytest
from bitarray import bitarray
from test_parse_object import TestData, check_parseobject_children, check_parseobject_properties

from easyprotocol.base.parse_list import ParseList
from easyprotocol.base.parse_object import DEFAULT_ENDIANNESS, ParseObject
from easyprotocol.fields import UInt8Field
from easyprotocol.fields.unsigned_int import UIntField


def parselist_value(
    obj: ParseList,
    tst: TestData,
) -> None:
    if obj.value is None:
        assert False, "object value is not instantiated"
    else:
        assert len(obj.value) == len(tst.value), (
            f"{obj}: len(obj.value) is not the expected value "
            + f"({len(obj.value)} != expected value: {len(tst.value)})"
        )
        for i in range(len(tst.value)):
            assert obj.value[i] == tst.value[i], (
                f"{obj}: obj.value[{i}] is not the expected value "
                + f"({obj.value[i]} != expected value: {tst.value[i]})"
            )
            assert obj[i].fmt.format(obj.value[i]) in obj.formatted_value
            assert obj[i].fmt.format(obj.value[i]) in str(obj)
            assert obj[i].fmt.format(obj.value[i]) in repr(obj)


def parselist_tests(
    obj: ParseList,
    tst: TestData,
) -> None:
    check_parseobject_properties(
        obj=obj,
        tst=tst,
    )
    check_parseobject_children(
        obj=obj,
        tst=tst,
    )
    parselist_value(
        obj=obj,
        tst=tst,
    )


class TestParseList:
    def test_parselist_create_empty(self) -> None:
        value: list[Any] = []
        byte_data = b""
        bits_data = bitarray(endian="little")
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseList(
            name=tst.name,
        )
        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_create_children_list(self) -> None:
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        f2_value = 0
        f2_data = int.to_bytes(f2_value, length=1, byteorder="big", signed=False)
        f2_bits = bitarray(endian="little")
        f2_bits.frombytes(f2_data)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name)
        bits_data = f2.bits + f1.bits
        byte_data = bytes(f2) + bytes(f1)
        value: list[Any] = [f1.value, f2.value]
        children_list: list[ParseObject[Any]] = [f1, f2]
        tst = TestData(
            name="test",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            format="{}",
            parent=None,
            children=OrderedDict({f1.name: f1, f2.name: f2}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseList(
            name=tst.name,
            children=children_list,
        )
        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_create_children_dict(self) -> None:
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        f2_value = 0
        f2_data = int.to_bytes(f2_value, length=1, byteorder="big", signed=False)
        f2_bits = bitarray(endian="little")
        f2_bits.frombytes(f2_data)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name)
        bits_data = f2.bits + f1.bits
        byte_data = bytes(f2) + bytes(f1)
        values: list[Any] = [f1.value, f2.value]
        tst = TestData(
            name="test",
            value=values,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict({f1.name: f1, f2.name: f2}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseList(
            name=tst.name,
            children=tst.children,
        )
        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_create_parse_single_field(self) -> None:
        f1_value = 255
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        byte_data = f1_data
        bits_data = f1_bits
        values = [f1_value]
        tst = TestData(
            name="test",
            value=values,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict({f1.name: f1}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseList(
            name=tst.name,
            children=[f1],
            data=tst.byte_data,
        )
        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_create_parse_multi_field(self) -> None:
        init_value = 0
        init_data = int.to_bytes(init_value, length=1, byteorder="big", signed=False)
        init_bits = bitarray(endian="little")
        init_bits.frombytes(init_data)
        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        f2_name = "f2"
        f2_value = 187
        f2_data = b"\xbb"
        f2_bits = bitarray(endian="little")
        f2_bits.frombytes(f2_data)
        f2 = UInt8Field(name=f2_name)
        f3_name = "f3"
        f3_value = 204
        f3_data = b"\xcc"
        f3_bits = bitarray(endian="little")
        f3_bits.frombytes(f3_data)
        f3 = UInt8Field(name=f3_name)
        byte_data = f1_data + f2_data + f3_data
        bits_data = f1_bits + f2_bits + f3_bits
        values = [f1_value, f2_value, f3_value]
        tst = TestData(
            name="test",
            value=values,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict({f1.name: f1, f2.name: f2, f3.name: f3}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseList(
            name=tst.name,
            children=[f1, f2, f3],
            data=tst.byte_data,
        )

        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_create_parse_multi_bit_field(self) -> None:
        f1_name = "f1"
        f1_bit_count = 6
        f1_value = 0x3F
        f1_byte = struct.pack("B", f1_value)
        f1_bits = bitarray(endian="little")
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
        f2_bits = bitarray(endian="little")
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
        f3_bits = bitarray(endian="little")
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
        f4_bits = bitarray(endian="little")
        f4_bits.frombytes(f4_data)
        f4_bits = f4_bits[:f4_bit_count]
        f4 = UIntField(
            name=f4_name,
            bit_count=f1_bit_count,
        )

        byte_data = b"\x3F\xF0\x03"
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        values = [f1_value, f2_value, f3_value, f4_value]
        tst = TestData(
            name="test",
            value=values,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict({f1.name: f1, f2.name: f2, f3.name: f3, f4.name: f4}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseList(
            name=tst.name,
            children=[f1, f2, f3, f4],
            data=tst.byte_data,
        )

        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_parse_single_field(self) -> None:
        f1_value = 255
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        byte_data1 = b"\x00"
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        values1 = [0]
        byte_data2 = f1_data
        bits_data2 = f1_bits
        values2 = [f1_value]
        tst = TestData(
            name="test",
            value=values1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            children=OrderedDict({f1.name: f1}),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseList(
            name=tst.name,
            children=[f1],
        )
        parselist_tests(
            obj=obj,
            tst=tst,
        )

        obj.parse(data=byte_data2)
        tst.value = values2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_parse_multi_field(self) -> None:
        init_value = 0
        init_data = int.to_bytes(init_value, length=1, byteorder="big", signed=False)
        init_bits = bitarray(endian="little")
        init_bits.frombytes(init_data)
        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        f2_name = "f2"
        f2_value = 187
        f2_data = b"\xbb"
        f2_bits = bitarray(endian="little")
        f2_bits.frombytes(f2_data)
        f2 = UInt8Field(name=f2_name)
        f3_name = "f3"
        f3_value = 204
        f3_data = b"\xcc"
        f3_bits = bitarray(endian="little")
        f3_bits.frombytes(f3_data)
        f3 = UInt8Field(name=f3_name)
        byte_data1 = b"\x00\x00\x00"
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        values1 = [0, 0, 0]
        byte_data2 = f1_data + f2_data + f3_data
        bits_data2 = f1_bits + f2_bits + f3_bits
        values2 = [f1_value, f2_value, f3_value]
        tst = TestData(
            name="test",
            value=values1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            children=OrderedDict({f1.name: f1, f2.name: f2, f3.name: f3}),
            endian=DEFAULT_ENDIANNESS,
        )

        obj = ParseList(
            name=tst.name,
            children=[f1, f2, f3],
        )
        parselist_tests(
            obj=obj,
            tst=tst,
        )

        obj.parse(data=byte_data2)
        tst.value = values2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_set_name(self) -> None:
        name1 = "test"
        name2 = "new_name"
        byte_data = b""
        bits_data = bitarray(endian="little")
        values: list[Any] = []
        tst = TestData(
            name=name1,
            value=values,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseList(
            name=tst.name,
        )
        parselist_tests(
            obj=obj,
            tst=tst,
        )
        tst.name = name2
        obj.name = tst.name
        parselist_tests(
            obj=obj,
            tst=tst,
        )

    def test_parselist_set_value(self) -> None:
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f2_value = 2
        f2_data = int.to_bytes(f2_value, length=1, byteorder="big", signed=False)
        f2_bits = bitarray(endian="little")
        f2_bits.frombytes(f2_data)
        f3_value = 20
        f3_data = int.to_bytes(f3_value, length=1, byteorder="big", signed=False)
        f3_bits = bitarray(endian="little")
        f3_bits.frombytes(f3_data)
        f1_name = "f1"
        f2_name = "f2"
        f1 = UInt8Field(name=f1_name, value=f1_value)
        f2 = UInt8Field(name=f2_name, value=f2_value)
        bits_data1 = bitarray(endian="little")
        bits_data2 = f1_bits
        bits_data3 = f2_bits
        bits_data4 = f3_bits
        byte_data1 = b""
        byte_data2 = f1_data
        byte_data3 = f2_data
        byte_data4 = f3_data
        values1: list[Any] = []
        values2: list[Any] = [f1_value]
        values3: list[Any] = [f2_value]
        values4: list[Any] = [f3_value]
        children1: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1})
        children3: OrderedDict[str, ParseObject[Any]] = OrderedDict({f2.name: f2})
        children4: OrderedDict[str, ParseObject[Any]] = OrderedDict({f2.name: f2})
        tst = TestData(
            name="test",
            value=values1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            children=children1,
            endian=DEFAULT_ENDIANNESS,
        )

        obj = ParseList(
            name=tst.name,
        )
        parselist_tests(
            obj=obj,
            tst=tst,
        )

        obj.value = [f1]
        tst.value = values2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        tst.children = children2
        parselist_tests(
            obj=obj,
            tst=tst,
        )

        obj.value = [f2]
        tst.value = values3
        tst.byte_data = byte_data3
        tst.bits_data = bits_data3
        tst.children = children3
        parselist_tests(
            obj=obj,
            tst=tst,
        )

        obj.value = [f3_value]
        tst.value = values4
        tst.byte_data = byte_data4
        tst.bits_data = bits_data4
        tst.children = children4
        parselist_tests(
            obj=obj,
            tst=tst,
        )

        value = 1
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_parselist_remove(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name)
        po = ParseList(name=name, children=[f1, f2])

        assert len(po) == 2
        assert f1.parent == po
        assert f2.parent == po
        po.remove(f2)
        assert len(po) == 1
        assert f2.parent is None

    def test_parselist_set_item(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name, value=1)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name, value=2)
        f3_name = "f3"
        f3 = UInt8Field(name=f3_name, value=3)
        f3_also = UInt8Field(name=f3_name, value=17)
        po = ParseList(name=name, children=[f1, f2, f3])

        assert f1.parent == po
        assert f2.parent == po
        assert f3.parent == po
        assert f3_also.parent is None
        assert len(po) == 3
        assert po[2] == f3
        assert po[2].value == f3.value
        po[2] = f3_also
        assert f3_also.parent == po
        assert len(po) == 3
        assert po[2] == f3_also
        assert po[2].value == f3_also.value

    def test_parselist_insert(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name, value=1)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name, value=2)
        f3_name = "f3"
        f3 = UInt8Field(name=f3_name, value=3)
        po = ParseList(name=name, children=[f1, f3])

        assert f1.parent == po
        assert f2.parent is None
        assert f3.parent == po
        assert len(po) == 2
        assert po[0] == f1
        assert po[0].value == f1.value
        assert po[1] == f3
        assert po[1].value == f3.value
        po.insert(1, f2)
        assert f2.parent == po
        assert len(po) == 3
        assert po[0] == f1
        assert po[0].value == f1.value
        assert po[1] == f2
        assert po[1].value == f2.value
        assert po[2] == f3
        assert po[2].value == f3.value
