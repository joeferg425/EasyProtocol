from __future__ import annotations
from collections import OrderedDict
from typing import Any
import pytest
from easyprotocol.parse_list import ParseList
from easyprotocol.parse_object import ParseObject
from easyprotocol.fields import UInt8
from bitarray import bitarray


class TestParseList:
    def test_parselist_create_empty(self) -> None:
        name = "test"
        data = b""
        bits = bitarray()
        value: list[Any] = []
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        po = ParseList(name=name)
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert len(po.value) == 0
        assert po.value == value
        assert po.children is not None
        assert len(po.children) == 0
        assert po.children == children
        assert po.bits is not None
        assert po.bits == bits
        assert bytes(po) == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseList.__name__ in repr(po)

    def test_parselist_create_children_list(self) -> None:
        name = "test"
        f1_name = "f1"
        f2_name = "f2"
        f1 = UInt8(name=f1_name)
        assert f1.parent is None
        f2 = UInt8(name=f2_name)
        assert f2.parent is None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1, f2.name: f2})
        children_list: list[ParseObject[Any]] = [f1, f2]
        value: list[Any] = [f1.value, f2.value]
        data = f1.bits + f2.bits
        po = ParseList(name=name, children=children_list)
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert len(po.value) == 2
        assert po.value == value
        assert po.children is not None
        assert len(po.children) == 2
        assert po.children == children
        assert f1.parent == po
        assert f2.parent == po
        assert po.bits is not None
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseList.__name__ in repr(po)

    def test_parselist_create_children_dict(self) -> None:
        name = "test"
        f1_name = "f1"
        f2_name = "f2"
        f1 = UInt8(name=f1_name)
        assert f1.parent is None
        f2 = UInt8(name=f2_name)
        assert f2.parent is None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({f1.name: f1, f2.name: f2})
        value: list[Any] = [f1.value, f2.value]
        data = f1.bits + f2.bits
        po = ParseList(name=name, children=children)
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert len(po.value) == 2
        assert po.value == value
        assert po.children is not None
        assert len(po.children) == 2
        assert po.children == children
        assert f1.parent == po
        assert f2.parent == po
        assert po.bits is not None
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseList.__name__ in repr(po)

    def test_parselist_create_parse_single_field(self) -> None:
        p_name = "test"
        p_data = b"\xff"
        p_bits = bitarray()
        p_bits.frombytes(p_data)
        f1_name = "f1"
        f1_value = 255
        f1_data = b"\xff"
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        left_over = b""
        f1 = UInt8(name=f1_name)
        assert f1.parent is None
        p_value = [f1_value]
        po = ParseList(name=p_name, children=[f1], data=p_data)
        remainder = b""

        assert f1.name == f1_name
        assert f1.bits is not None
        assert f1.bits == f1_bits
        assert bytes(f1) == f1_data
        assert f1.value is not None
        assert f1.value == f1_value
        assert f1.parent == po

        assert remainder == left_over
        assert po is not None
        assert po.name == p_name
        assert po.bits is not None
        assert po.bits == p_bits
        assert bytes(po) == p_data
        assert po.value is not None
        assert po.value == p_value
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert p_name in str(po)
        assert f1_name in str(po)
        assert isinstance(repr(po), str)
        assert p_name in repr(po)
        assert f1_name in repr(po)
        assert ParseList.__name__ in repr(po)

    def test_parselist_create_parse_multi_field(self) -> None:
        p_name = "test"
        p_data = b"\xaa\xbb\xcc"
        p_bits = bitarray()
        p_bits.frombytes(p_data)
        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1_bits = bitarray()
        f1_bits.frombytes(f1_data)
        f1 = UInt8(name=f1_name)
        f2_name = "f2"
        f2_value = 187
        f2_data = b"\xbb"
        f2_bits = bitarray()
        f2_bits.frombytes(f2_data)
        f2 = UInt8(name=f2_name)
        f3_name = "f3"
        f3_value = 204
        f3_data = b"\xcc"
        f3_bits = bitarray()
        f3_bits.frombytes(f3_data)
        f3 = UInt8(name=f3_name)
        p_value = [f1_value, f2_value, f3_value]
        p = ParseList(name=p_name, children=[f1, f2, f3], data=p_data)

        assert f1.name == f1_name
        assert f1.bits is not None
        assert f1.bits == f1_bits
        assert bytes(f1) == f1_data
        assert f1.value is not None
        assert f1.value == f1_value
        assert f1.parent == p

        assert f2.name == f2_name
        assert f2.bits is not None
        assert f2.bits == f2_bits
        assert bytes(f2) == f2_data
        assert f2.value is not None
        assert f2.value == f2_value
        assert f2.parent == p

        assert f3.name == f3_name
        assert f3.bits is not None
        assert f3.bits == f3_bits
        assert bytes(f3) == f3_data
        assert f3.value is not None
        assert f3.value == f3_value
        assert f3.parent == p

        assert p is not None
        assert p.name == p_name
        assert p.bits is not None
        assert p.bits == p_bits
        assert bytes(p) == p_data
        assert p.value is not None
        assert p.value == p_value
        assert isinstance(p.formatted_value, str)
        assert isinstance(bytes(p), bytes)
        assert isinstance(str(p), str)
        assert p_name in str(p)
        assert f1_name in str(p)
        assert f2_name in str(p)
        assert f3_name in str(p)
        assert isinstance(repr(p), str)
        assert p_name in repr(p)
        assert f1_name in repr(p)
        assert f2_name in repr(p)
        assert f3_name in repr(p)
        assert ParseList.__name__ in repr(p)

    def test_parselist_name(self) -> None:
        name = "test"
        name2 = "new_name"
        po = ParseList(name=name)
        assert po is not None
        assert po.name == name
        po.name = name2
        assert po.name == name2

    def test_parselist_value(self) -> None:
        name = "test"
        po = ParseList(name=name)
        d1 = b"\x00"
        b1 = bitarray()
        b1.frombytes(d1)
        d2 = b"\x02"
        b2 = bitarray()
        b2.frombytes(d2)
        f1_name = "f1"
        f2_name = "f2"
        f1 = UInt8(name=f1_name)
        f2 = UInt8(name=f2_name)

        assert po.bits is not None
        assert po.bits == bitarray()
        assert bytes(po) == b""
        assert po.value is not None
        assert po.value == []

        po.value = [f1]
        assert po.bits == b1
        assert bytes(po) == d1
        assert po.value == [f1.value]
        assert f1.parent == po

        po.value = [f2]
        assert po.bits == b1
        assert bytes(po) == d1
        assert po.value == [f2.value]
        assert f2.parent == po

        assert f2.name == f2_name
        assert f2.bits == b1
        assert bytes(f2) == d1
        assert f2.value == 0
        assert f2.parent == po

        po.value = [2]
        assert f2.name == f2_name
        assert f2.bits == b2
        assert bytes(f2) == d2
        assert f2.value == 2
        assert f2.parent == po

        value = 1
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_parselist_len(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8(name=f1_name)
        po = ParseList(name=name, children=[f1])
        assert len(po) == 1

    def test_parselist_remove(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8(name=f1_name)
        f2_name = "f2"
        f2 = UInt8(name=f2_name)
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
        f1 = UInt8(name=f1_name, value=1)
        f2_name = "f2"
        f2 = UInt8(name=f2_name, value=2)
        f3_name = "f3"
        f3 = UInt8(name=f3_name, value=3)
        f3_also = UInt8(name=f3_name, value=17)
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
        f1 = UInt8(name=f1_name, value=1)
        f2_name = "f2"
        f2 = UInt8(name=f2_name, value=2)
        f3_name = "f3"
        f3 = UInt8(name=f3_name, value=3)
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
