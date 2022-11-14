from __future__ import annotations
from collections import OrderedDict
from typing import Any
import pytest
from easyprotocol.base.parse_list import ParseList
from easyprotocol.base.parse_object import ParseObject
from easyprotocol.fields import UInt8Field
from bitarray import bitarray
from test_parse_object import parseobject_properties, parseobject_children


def parselist_value(
    obj: ParseList,
    values: list[Any],
) -> None:
    assert len(obj.value) == len(values), (
        f"{obj}: len(obj.value) is not the expected value " + f"({len(obj.value)} != expected value: {len(values)})"
    )
    for i in range(len(values)):
        assert obj.value[i] == values[i], (
            f"{obj}: obj.value[{i}] is not the expected value " + f"({obj.value[i]} != expected value: {values[i]})"
        )
        assert obj[i].format.format(obj.value[i]) in obj.formatted_value
        assert obj[i].format.format(obj.value[i]) in str(obj)
        assert obj[i].format.format(obj.value[i]) in repr(obj)


def parselist_tests(
    obj: ParseList,
    name: str,
    values: list[Any],
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
    parselist_value(
        obj=obj,
        values=values,
    )


class TestParseList:
    def test_parselist_create_empty(self) -> None:
        name = "test"
        data = b""
        bits = bitarray()
        values: list[Any] = []
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = ParseList(name=name)
        parselist_tests(
            obj=obj,
            name=name,
            values=values,
            bits_data=bits,
            byte_data=data,
            parent=parent,
            children=children,
        )

    def test_parselist_create_children_list(self) -> None:
        name = "test"
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
        values: list[Any] = [f1.value, f2.value]
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1, f2.name: f2})
        children_list: list[ParseObject[Any]] = [f1, f2]
        obj = ParseList(name=name, children=children_list)
        parselist_tests(
            obj=obj,
            name=name,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parselist_create_children_dict(self) -> None:
        name = "test"
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
        values: list[Any] = [f1.value, f2.value]
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1, f2.name: f2})
        obj = ParseList(name=name, children=children)
        parselist_tests(
            obj=obj,
            name=name,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parselist_create_parse_single_field(self) -> None:
        name = "test"
        f1_value = 255
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1_name = "f1"
        f1 = UInt8Field(name=f1_name)
        byte_data = f1_data
        bits_data = f1_bits
        values = [f1_value]
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1})
        obj = ParseList(name=name, children=[f1], data=byte_data)
        parselist_tests(
            obj=obj,
            name=name,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parselist_create_parse_multi_field(self) -> None:
        name = "test"
        init_value = 0
        init_data = int.to_bytes(init_value, length=1, byteorder="big", signed=False)
        init_bits = bitarray()
        init_bits.frombytes(init_data)
        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1 = UInt8Field(name=f1_name)
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
        byte_data = f3_data + f2_data + f1_data
        bits_data = f3_bits + f2_bits + f1_bits
        values = [f1_value, f2_value, f3_value]
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1, f2.name: f2, f3.name: f3})
        obj = ParseList(name=name, children=[f1, f2, f3], data=byte_data)

        parselist_tests(
            obj=obj,
            name=name,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parselist_set_name(self) -> None:
        name1 = "test"
        name2 = "new_name"
        byte_data = b""
        bits_data = bitarray()
        values: list[Any] = []
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = ParseList(name=name1)
        parselist_tests(
            obj=obj,
            name=name1,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )
        obj.name = name2
        parselist_tests(
            obj=obj,
            name=name2,
            values=values,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_parselist_set_value(self) -> None:
        name = "test"
        f1_value = 0
        f1_data = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f2_value = 2
        f2_data = int.to_bytes(f2_value, length=1, byteorder="big", signed=False)
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f3_value = 20
        f3_data = int.to_bytes(f3_value, length=1, byteorder="big", signed=False)
        f3_bits = bitarray()
        f3_bits.frombytes(f3_data)
        f1_name = "f1"
        f2_name = "f2"
        f1 = UInt8Field(name=f1_name, value=f1_value)
        f2 = UInt8Field(name=f2_name, value=f2_value)
        bits_data1 = bitarray()
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
        parent = None
        children1: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1})
        children3: OrderedDict[str, ParseObject[Any]] = OrderedDict({f2.name: f2})
        children4: OrderedDict[str, ParseObject[Any]] = OrderedDict({f2.name: f2})
        obj = ParseList(name=name)

        parselist_tests(
            obj=obj,
            name=name,
            values=values1,
            bits_data=bits_data1,
            byte_data=byte_data1,
            parent=parent,
            children=children1,
        )

        obj.value = [f1]
        parselist_tests(
            obj=obj,
            name=name,
            values=values2,
            bits_data=bits_data2,
            byte_data=byte_data2,
            parent=parent,
            children=children2,
        )

        obj.value = [f2]
        parselist_tests(
            obj=obj,
            name=name,
            values=values3,
            bits_data=bits_data3,
            byte_data=byte_data3,
            parent=parent,
            children=children3,
        )

        obj.value = [f3_value]
        parselist_tests(
            obj=obj,
            name=name,
            values=values4,
            bits_data=bits_data4,
            byte_data=byte_data4,
            parent=parent,
            children=children4,
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
