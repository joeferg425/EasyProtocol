from __future__ import annotations
from collections import OrderedDict
from typing import Any
import pytest
from easyprotocol.parse_dict import ParseDict
from easyprotocol.parse_object import ParseObject
from easyprotocol.fields import UInt8Field
from bitarray import bitarray
from test_parse_object import parseobject_properties, parseobject_children, parseobject_tests


def parsedict_value(
    obj: ParseDict,
    values: OrderedDict[str, Any],
) -> None:
    assert len(obj.value) == len(values), (
        f"{obj}: len(obj.value) is not the expected value " + f"({len(obj.value)} != expected value: {len(values)})"
    )
    assert obj.value.keys() == values.keys(), (
        f"{obj}: obj.value.keys() is not the expected value "
        + f"({obj.value.keys()} != expected value: {values.keys()})"
    )
    for key in values.keys():
        assert obj.value[key] == values[key], (
            f"{obj}: obj.value[key] is not the expected value " + f"({obj.value[key]} != expected value: {values[key]})"
        )

    for key in obj.value.keys():
        assert obj[key].format.format(obj.value[key]) in obj.formatted_value
        assert obj[key].format.format(obj.value[key]) in str(obj)
        assert obj[key].format.format(obj.value[key]) in repr(obj)


def parsedict_tests(
    obj: ParseDict,
    name: str,
    values: OrderedDict[str, Any],
    bits_data: bitarray,
    byte_data: bytes,
    parent: ParseObject[Any] | None,
    children: OrderedDict[str, ParseObject[Any]],
) -> None:
    parseobject_properties(
        obj=obj,
        name=name,
        format="{}",
        bits_data=bits_data,
        byte_data=byte_data,
        parent=parent,
    )
    parseobject_children(
        obj=obj,
        name=name,
        children=children,
        parent=parent,
    )
    parsedict_value(
        obj=obj,
        values=values,
    )


class TestParseDict:
    def test_parsedict_create_empty(self) -> None:
        name = "test"
        values: OrderedDict[str, Any] = OrderedDict()
        byte_data = b""
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = ParseDict(name=name)
        parsedict_tests(
            obj=obj,
            name=name,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parsedict_create_parse(self) -> None:
        name = "test"
        f1_name = "child"
        f1_value = 0
        f1_bytes = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_bytes)
        f1 = UInt8Field(name=f1_name)
        values: OrderedDict[str, Any] = OrderedDict({f1_name: f1_value})
        byte_data = f1_bytes
        bits_data = f1_bits
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1})
        obj = ParseDict(name=name, children=children, data=byte_data)
        obj[f1.name] = f1
        parsedict_tests(
            obj=obj,
            name=name,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parsedict_create_children(self) -> None:
        name = "test"
        f1_name = "child"
        f1_value = 0
        f1_value = 0
        f1_bytes = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_bytes)
        f1 = UInt8Field(name=f1_name)
        bits_data = f1.bits
        byte_data = bits_data.tobytes()
        parent = None
        values: OrderedDict[str, Any] = OrderedDict({f1_name: f1_value})
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1})
        obj = ParseDict(name=name, children=children)
        parsedict_tests(
            obj=obj,
            name=name,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parsedict_set_name(self) -> None:
        name1 = "test"
        name2 = "new_name"
        byte_data = b""
        bits_data = bitarray()
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        values: OrderedDict[str, Any] = OrderedDict()
        obj = ParseDict(name=name1)
        parsedict_tests(
            obj=obj,
            name=name1,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )
        obj.name = name2
        parsedict_tests(
            obj=obj,
            name=name2,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parsedict_set_value(self) -> None:
        name = "test"
        f1_name = "object1"
        v2 = 0
        v3 = 1
        byte_data1 = b""
        byte_data2 = int.to_bytes(v2, length=1, byteorder="big")
        byte_data3 = int.to_bytes(v3, length=1, byteorder="big")
        bits_data1 = bitarray()
        bits_data2 = bitarray()
        bits_data3 = bitarray()
        bits_data2.frombytes(byte_data2)
        bits_data3.frombytes(byte_data3)
        f1 = UInt8Field(name=f1_name, value=v2)
        values1: OrderedDict[str, Any] = OrderedDict()
        values2: OrderedDict[str, Any] = OrderedDict({f1_name: v2})
        values3: OrderedDict[str, Any] = OrderedDict({f1_name: v3})
        parent = None
        children1: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1})
        children3: OrderedDict[str, ParseObject[Any]] = children2.copy()
        obj = ParseDict(name=name)
        parsedict_tests(
            obj=obj,
            name=name,
            values=values1,
            bits_data=bits_data1,
            byte_data=byte_data1,
            parent=parent,
            children=children1,
        )

        obj.value = children2
        parsedict_tests(
            obj=obj,
            name=name,
            values=values2,
            bits_data=bits_data2,
            byte_data=byte_data2,
            parent=parent,
            children=children2,
        )

        obj.value = values3
        parsedict_tests(
            obj=obj,
            name=name,
            values=values3,
            bits_data=bits_data3,
            byte_data=byte_data3,
            parent=parent,
            children=children3,
        )

        value = 1
        obj = ParseDict(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_parsedict_set_parent(self) -> None:
        name = "test"
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big")
        f1_bits = bitarray()
        f1_bits.frombytes(b"\x00")
        f1_name = "parent"
        byte_data1 = b""
        bits_data1 = bitarray()
        byte_data2 = f1_data
        bits_data2 = f1_bits
        f1 = UInt8Field(name=f1_name)
        values1: OrderedDict[str, Any] = OrderedDict()
        values2: OrderedDict[str, Any] = OrderedDict({f1.name: f1.value})
        parent = None
        children1: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1_name: f1})
        obj = ParseDict(name=name)

        parsedict_tests(
            obj=obj,
            name=name,
            values=values1,
            bits_data=bits_data1,
            byte_data=byte_data1,
            parent=parent,
            children=children1,
        )

        obj.children = children2
        parsedict_tests(
            obj=obj,
            name=name,
            values=values2,
            bits_data=bits_data2,
            byte_data=byte_data2,
            parent=parent,
            children=children2,
        )

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
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1, f2.name: f2})
        obj = ParseDict(name=name, children=children)

        assert len(obj) == 2
        assert f1.parent == obj
        assert f2.parent == obj
        obj.pop(f2_name)
        assert len(obj) == 1
        assert f2.parent is None

    def test_parsedict_parse_1(self) -> None:
        name = "test"
        f1_data0 = b"\x00"
        f1_bits0 = bitarray()
        f1_bits0.frombytes(f1_data0)
        f1_name = "f1"
        f1_value = 255
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big")
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        byte_data1 = int.to_bytes(0, length=1, byteorder="big")
        byte_data2 = f1_data
        bits_data1 = bitarray()
        bits_data1.frombytes(byte_data1)
        bits_data2 = f1_bits
        left_over = bitarray()
        values1: OrderedDict[str, Any] = OrderedDict({f1_name: f1.value})
        values2: OrderedDict[str, Any] = OrderedDict({f1_name: 255})
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1_name: f1})
        obj = ParseDict(name=name)
        obj[f1.name] = f1

        parsedict_tests(
            obj=obj,
            name=name,
            values=values1,
            bits_data=bits_data1,
            byte_data=byte_data1,
            parent=parent,
            children=children,
        )

        remainder = obj.parse(byte_data2)
        assert remainder == left_over
        parsedict_tests(
            obj=obj,
            name=name,
            values=values2,
            bits_data=bits_data2,
            byte_data=byte_data2,
            parent=parent,
            children=children,
        )

    def test_parsedict_parse_3(self) -> None:
        name = "test"
        u_data = b"\x00"
        u_bits = bitarray()
        u_bits.frombytes(u_data)

        init_value = 0
        init_data = int.to_bytes(init_value, length=1, byteorder="big")
        init_bits = bitarray()
        init_bits.frombytes(init_data)

        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
        f_children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        f2_name = "f2"
        f2_value = 187
        f2_data = b"\xbb"
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f2 = UInt8Field(name=f2_name)
        f3_name = "f3"
        f3_value = 204
        f3_data = b"\xcc"
        f3_bits = bitarray()
        f3_bits.frombytes(f3_data)
        f3 = UInt8Field(name=f3_name)
        left_over = bitarray()
        byte_data1 = init_data + init_data + init_data
        byte_data2 = f3_data + f2_data + f1_data
        bits_data1 = init_bits + init_bits + init_bits
        bits_data2 = f3_bits + f2_bits + f1_bits

        values1: OrderedDict[str, Any] = OrderedDict({f1_name: 0, f2_name: 0, f3_name: 0})
        values2: OrderedDict[str, Any] = OrderedDict({f1_name: f1_value, f2_name: f2_value, f3_name: f3_value})
        parent = None
        children1: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
        children2: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
        obj = ParseDict(name=name)
        obj[f1.name] = f1
        obj[f2.name] = f2
        obj[f3.name] = f3

        parseobject_tests(
            obj=f1,
            name=f1_name,
            value=init_value,
            format=f1.format,
            bits_data=init_bits,
            byte_data=init_data,
            parent=obj,
            children=f_children,
        )
        parseobject_tests(
            obj=f2,
            name=f2_name,
            value=init_value,
            format=f2.format,
            bits_data=init_bits,
            byte_data=init_data,
            parent=obj,
            children=f_children,
        )
        parseobject_tests(
            obj=f3,
            name=f3_name,
            value=init_value,
            format=f3.format,
            bits_data=init_bits,
            byte_data=init_data,
            parent=obj,
            children=f_children,
        )
        parsedict_tests(
            obj=obj,
            name=name,
            values=values1,
            bits_data=bits_data1,
            byte_data=byte_data1,
            parent=parent,
            children=children1,
        )

        remainder = obj.parse(byte_data2)
        assert remainder == left_over
        parseobject_tests(
            obj=f1,
            name=f1_name,
            value=f1_value,
            format=f1.format,
            bits_data=f1_bits,
            byte_data=f1_data,
            parent=obj,
            children=f_children,
        )
        parseobject_tests(
            obj=f2,
            name=f2_name,
            value=f2_value,
            format=f2.format,
            bits_data=f2_bits,
            byte_data=f2_data,
            parent=obj,
            children=f_children,
        )
        parseobject_tests(
            obj=f3,
            name=f3_name,
            value=f3_value,
            format=f3.format,
            bits_data=f3_bits,
            byte_data=f3_data,
            parent=obj,
            children=f_children,
        )
        parsedict_tests(
            obj=obj,
            name=name,
            values=values2,
            bits_data=bits_data2,
            byte_data=byte_data2,
            parent=parent,
            children=children2,
        )
