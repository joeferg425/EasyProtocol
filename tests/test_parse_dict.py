from __future__ import annotations

import struct
from collections import OrderedDict
from typing import Any

import pytest
from bitarray import bitarray
from test_parse_object import (
    TestData,
    check_parseobject,
    check_parseobject_children,
    check_parseobject_properties,
)

from easyprotocol.base.parse_dict import ParseDict
from easyprotocol.base.parse_object import (
    DEFAULT_ENDIANNESS,
    ParseObject,
    ParseObjectGeneric,
)
from easyprotocol.fields import UInt8Field
from easyprotocol.fields.unsigned_int import UIntField


def check_parsedict_value(
    obj: ParseDict,
    tst: TestData,
) -> None:
    if obj.value is None:
        assert False, "object value is not instantiated"
    else:
        assert len(obj.value) == len(tst.value), (
            f"{obj}: len(obj.value) is not the expected value "
            + f"({len(obj.value)} != expected value: {len(tst.value)})"
        )
        assert obj.value.keys() == tst.value.keys(), (
            f"{obj}: obj.value.keys() is not the expected value "
            + f"({obj.value.keys()} != expected value: {tst.value.keys()})"
        )
        for key in tst.value.keys():
            assert obj.value[key] == tst.value[key], (
                f"{obj}: obj.value[key] is not the expected value "
                + f"({obj.value[key]} != expected value: {tst.value[key]})"
            )

        for key in obj.value.keys():
            value = obj[key]
            assert value.formatted_value in obj.formatted_value
            assert value.formatted_value in str(obj)
            assert value.formatted_value in repr(obj)


def check_parsedict(
    obj: ParseDict,
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
    check_parsedict_value(
        obj=obj,
        tst=tst,
    )


class TestParseDict:
    def test_parsedict_create_empty(self) -> None:
        values: OrderedDict[str, Any] = OrderedDict()
        byte_data = b""
        bits_data = bitarray(endian="little")
        tst = TestData(
            name="test",
            value=values,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseDict(
            name=tst.name,
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_create_children(self) -> None:
        f1_name = "child"
        f1_value = 0
        f1_value = 0
        f1_bytes = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_bytes)
        f1 = UInt8Field(name=f1_name)
        bits_data = f1.bits
        byte_data = bits_data.tobytes()
        values: OrderedDict[str, Any] = OrderedDict({f1_name: f1_value})
        children: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1.name: f1})
        tst = TestData(
            name="test",
            value=children,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=children,
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseDict(
            name=tst.name,
            children=tst.children,
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_create_parse_single(self) -> None:
        f1_name = "child"
        f1_value = 0
        f1_bytes = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_bytes)
        f1 = UInt8Field(name=f1_name)
        values: OrderedDict[str, Any] = OrderedDict({f1_name: f1_value})
        children: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1.name: f1})
        byte_data = f1_bytes
        bits_data = f1_bits
        tst = TestData(
            name="test",
            value=children,
            byte_data=byte_data,
            bits_data=bits_data,
            format="{}",
            parent=None,
            children=children,
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseDict(
            name=tst.name,
            children=tst.children,
            data=tst.byte_data,
        )
        obj[f1.name] = f1
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_create_parse_multi_field(self) -> None:
        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        f_children: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict()
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
        values: OrderedDict[str, Any] = OrderedDict({f1_name: f1_value, f2_name: f2_value, f3_name: f3_value})
        children: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
        tst = TestData(
            name="test",
            value=children,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=children,
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseDict(
            name=tst.name,
            data=byte_data,
            children=children,
        )
        check_parseobject(
            obj=f1,
            tst=TestData(
                name=f1_name,
                value=f1_value,
                format=f1.fmt,
                bits_data=f1_bits,
                byte_data=f1_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parseobject(
            obj=f2,
            tst=TestData(
                name=f2_name,
                value=f2_value,
                format=f2.fmt,
                bits_data=f2_bits,
                byte_data=f2_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parseobject(
            obj=f3,
            tst=TestData(
                name=f3_name,
                value=f3_value,
                format=f3.fmt,
                bits_data=f3_bits,
                byte_data=f3_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_parse_single_field(self) -> None:
        f1_data0 = b"\x00"
        f1_bits0 = bitarray(endian="little")
        f1_bits0.frombytes(f1_data0)
        f1_name = "f1"
        f1_value = 255
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big")
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        byte_data1 = int.to_bytes(0, length=1, byteorder="big")
        byte_data2 = f1_data
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = f1_bits
        left_over = bitarray(endian="little")
        values1: OrderedDict[str, Any] = OrderedDict({f1_name: f1.value})
        values2: OrderedDict[str, Any] = OrderedDict({f1_name: 255})
        children1: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1})
        children2: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1})
        tst = TestData(
            name="test",
            value=children1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            children=children1,
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseDict(
            name=tst.name,
        )
        obj[f1.name] = f1

        check_parsedict(
            obj=obj,
            tst=tst,
        )

        remainder = obj.parse(byte_data2)
        assert remainder == left_over
        tst.value = children2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_parse_multi_field(self) -> None:
        u_data = b"\x00"
        u_bits = bitarray(endian="little")
        u_bits.frombytes(u_data)

        init_value = 0
        init_data = int.to_bytes(init_value, length=1, byteorder="big")
        init_bits = bitarray(endian="little")
        init_bits.frombytes(init_data)

        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        f_children: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict()
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
        left_over = bitarray(endian="little")
        byte_data1 = init_data + init_data + init_data
        byte_data2 = f1_data + f2_data + f3_data
        bits_data1 = u_bits + u_bits + u_bits
        bits_data2 = f1_bits + f2_bits + f3_bits
        values1: OrderedDict[str, Any] = OrderedDict({f1_name: 0, f2_name: 0, f3_name: 0})
        values2: OrderedDict[str, Any] = OrderedDict({f1_name: f1_value, f2_name: f2_value, f3_name: f3_value})
        children1: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
        children2: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
        tst = TestData(
            name="test",
            value=children1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            children=children1,
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseDict(
            name=tst.name,
        )
        obj[f1.name] = f1
        obj[f2.name] = f2
        obj[f3.name] = f3

        check_parseobject(
            obj=f1,
            tst=TestData(
                name=f1_name,
                value=init_value,
                format=f1.fmt,
                bits_data=init_bits,
                byte_data=init_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parseobject(
            obj=f2,
            tst=TestData(
                name=f2_name,
                value=init_value,
                format=f2.fmt,
                bits_data=init_bits,
                byte_data=init_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parseobject(
            obj=f3,
            tst=TestData(
                name=f3_name,
                value=init_value,
                format=f3.fmt,
                bits_data=init_bits,
                byte_data=init_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

        remainder = obj.parse(byte_data2)
        assert remainder == left_over
        tst.value = children2
        tst.children = children2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_parseobject(
            obj=f1,
            tst=TestData(
                name=f1_name,
                value=f1_value,
                format=f1.fmt,
                bits_data=f1_bits,
                byte_data=f1_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parseobject(
            obj=f2,
            tst=TestData(
                name=f2_name,
                value=f2_value,
                format=f2.fmt,
                bits_data=f2_bits,
                byte_data=f2_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parseobject(
            obj=f3,
            tst=TestData(
                name=f3_name,
                value=f3_value,
                format=f3.fmt,
                bits_data=f3_bits,
                byte_data=f3_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_parse_multi_bit_field_little_endian(self) -> None:
        f1_bit_count = 2
        f1_name = "f1"
        f1_value = 0b11
        f1_byte = struct.pack("B", f1_value)
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(f1_byte)
        f1_bits = f1_bits[:f1_bit_count]
        f1 = UIntField(
            name=f1_name,
            bit_count=f1_bit_count,
            endian=DEFAULT_ENDIANNESS,
        )

        f2_bit_count = 5
        f2_name = "f2"
        f2_value = 0b00000
        f2_data = struct.pack("B", f2_value)
        f2_bits = bitarray(endian="little")
        f2_bits.frombytes(f2_data)
        f2_bits = f2_bits[:f2_bit_count]
        f2 = UIntField(
            name=f2_name,
            bit_count=f2_bit_count,
            endian=DEFAULT_ENDIANNESS,
        )

        f3_bit_count = 9
        f3_name = "f3"
        f3_value = 0b111111111
        f3_data = struct.pack("<H", f3_value)
        f3_bits = bitarray(endian="little")
        f3_bits.frombytes(f3_data)
        f3_bits = f3_bits[:f3_bit_count]
        f3 = UIntField(
            name=f3_name,
            bit_count=f3_bit_count,
            endian=DEFAULT_ENDIANNESS,
        )

        f_children: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict()

        left_over = bitarray(endian="little")
        byte_data1 = b"\x00\x00"
        byte_data2 = b"\x83\xFF"
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        values1: OrderedDict[str, Any] = OrderedDict({f1_name: 0, f2_name: 0, f3_name: 0})
        values2: OrderedDict[str, Any] = OrderedDict({f1_name: f1_value, f2_name: f2_value, f3_name: f3_value})
        children1: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
        children2: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
        tst = TestData(
            name="test",
            value=children1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            children=children1,
            endian=DEFAULT_ENDIANNESS,
        )
        obj = ParseDict(
            name=tst.name,
            children=OrderedDict(
                {
                    f1.name: f1,
                    f2.name: f2,
                    f3.name: f3,
                }
            ),
        )
        remainder = obj.parse(byte_data2)
        assert remainder == left_over
        tst.value = children2
        tst.children = children2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_parseobject(
            obj=f1,
            tst=TestData(
                name=f1_name,
                value=f1_value,
                format=f1.fmt,
                bits_data=f1_bits,
                byte_data=f1_byte,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parseobject(
            obj=f2,
            tst=TestData(
                name=f2_name,
                value=f2_value,
                format=f2.fmt,
                bits_data=f2_bits,
                byte_data=f2_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parseobject(
            obj=f3,
            tst=TestData(
                name=f3_name,
                value=f3_value,
                format=f3.fmt,
                bits_data=f3_bits,
                byte_data=f3_data,
                parent=obj,
                children=f_children,
                endian=DEFAULT_ENDIANNESS,
            ),
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_set_name(self) -> None:
        name1 = "test"
        name2 = "new_name"
        byte_data = b""
        bits_data = bitarray(endian="little")
        values: OrderedDict[str, Any] = OrderedDict()
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
        obj = ParseDict(
            name=tst.name,
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

        tst.name = name2
        obj.name = tst.name
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_set_value(self) -> None:
        f1_name = "object1"
        v2 = 0
        v3 = 1
        byte_data1 = b""
        byte_data2 = int.to_bytes(v2, length=1, byteorder="big")
        byte_data3 = int.to_bytes(v3, length=1, byteorder="big")
        bits_data1 = bitarray(endian="little")
        bits_data2 = bitarray(endian="little")
        bits_data3 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data3.frombytes(byte_data3)
        f1 = UInt8Field(name=f1_name, value=v2)
        values1: OrderedDict[str, Any] = OrderedDict()
        values2: OrderedDict[str, Any] = OrderedDict({f1_name: v2})
        values3: OrderedDict[str, Any] = OrderedDict({f1_name: v3})
        children1: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1.name: f1})
        children3: OrderedDict[str, ParseObjectGeneric[Any]] = children2.copy()
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

        obj = ParseDict(
            name=tst.name,
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

        obj.value = children2
        tst.children = children2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        tst.value = children2
        check_parsedict(
            obj=obj,
            tst=tst,
        )

        obj.value = values3
        tst.children = children3
        tst.byte_data = byte_data3
        tst.bits_data = bits_data3
        tst.value = children3
        check_parsedict(
            obj=obj,
            tst=tst,
        )

        value = 1
        obj = ParseDict(name=tst.name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_parsedict_set_parent(self) -> None:
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big")
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(b"\x00")
        f1_name = "parent"
        byte_data1 = b""
        bits_data1 = bitarray(endian="little")
        byte_data2 = f1_data
        bits_data2 = f1_bits
        f1 = UInt8Field(name=f1_name)
        values1: OrderedDict[str, Any] = OrderedDict()
        values2: OrderedDict[str, Any] = OrderedDict({f1.name: f1.value})
        children1: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1})
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
        obj = ParseDict(
            name=tst.name,
        )

        check_parsedict(
            obj=obj,
            tst=tst,
        )

        obj.children = children2
        tst.children = children2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        tst.value = children2
        check_parsedict(
            obj=obj,
            tst=tst,
        )

    def test_parsedict_set_children(self) -> None:
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big")
        f1_bits = bitarray(endian="little")
        f1_bits.frombytes(b"\x00")
        f1_name = "parent"
        byte_data1 = b""
        bits_data1 = bitarray(endian="little")
        byte_data2 = f1_data
        bits_data2 = f1_bits
        f1 = UInt8Field(name=f1_name)
        values1: OrderedDict[str, Any] = OrderedDict()
        values2: OrderedDict[str, Any] = OrderedDict({f1.name: f1.value})
        children1: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1_name: f1})
        tst = TestData(
            name="test",
            value=values1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=children1,
        )
        obj = ParseDict(
            name=tst.name,
        )
        check_parsedict(
            obj=obj,
            tst=tst,
        )

        obj.children = children2
        tst.children = children2
        tst.value = values2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2

    def test_parsedict_set_item(self) -> None:
        name = "test"
        obj = ParseDict(name=name)
        with pytest.raises(TypeError):
            obj["x"] = "popcorn"  # type:ignore

    def test_parsedict_pop(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        f2_name = "f2"
        f2 = UInt8Field(name=f2_name)
        children: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict({f1.name: f1, f2.name: f2})
        obj = ParseDict(name=name, children=children)

        assert len(obj) == 2
        assert f1.parent == obj
        assert f2.parent == obj
        obj.pop(f2_name)
        assert len(obj) == 1
        assert f2.parent is None
