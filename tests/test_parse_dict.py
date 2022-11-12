from __future__ import annotations
from collections import OrderedDict
from typing import Any
import pytest
from easyprotocol.parse_dict import ParseDict
from easyprotocol.parse_object import ParseObject
from easyprotocol.unsigned_int import UInt8


class TestParseDict:
    def test_parsedict_create_empty(self) -> None:
        name = "test"
        value: dict[str, Any] = dict()
        data = b""
        po = ParseDict(name=name)
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert po.value == value
        assert po.data is not None
        assert po.data == data
        assert po.parent is None
        assert po.children is not None
        assert len(po.children) == 0
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseDict.__name__ in repr(po)

    def test_parsedict_create_parse(self) -> None:
        name = "test"
        name2 = "child"
        data = b"\x00"
        c = UInt8(name=name2)
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({c.name: c})
        value: OrderedDict[str, Any] = OrderedDict({c.name: c.value})
        po = ParseDict(name=name, children=children, data=data)
        po[c.name] = c
        assert c.parent == po
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert len(po.value) == 1
        assert po.value == value
        assert po.data is not None
        assert po.data == data
        assert po.parent is None
        assert po.children is not None
        assert len(po.children) == 1
        assert po.children == children
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseDict.__name__ in repr(po)

    def test_parsedict_create_children(self) -> None:
        name = "test"
        name2 = "child"
        c = UInt8(name=name2)
        value: OrderedDict[str, Any] = OrderedDict({c.name: c.value})
        data = c.data
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict({c.name: c})
        po = ParseDict(name=name, children=children)
        assert c.parent == po
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert po.value == value
        assert po.data is not None
        assert po.data == data
        assert po.parent is None
        assert po.children is not None
        assert len(po.children) == 1
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseDict.__name__ in repr(po)

    def test_parsedict_name(self) -> None:
        name1 = "test"
        name2 = "new_name"
        po = ParseDict(name=name1)
        assert po is not None
        assert po.name == name1
        po.name = name2
        assert po.name == name2

    def test_parsedict_value(self) -> None:
        name = "test"
        name2 = "object"
        p = UInt8(name=name2)
        value1: dict[str, Any] = dict()
        value2: OrderedDict[str, Any] = OrderedDict({p.name: p})
        value3: OrderedDict[str, Any] = OrderedDict({p.name: p.value})
        value4: OrderedDict[str, Any] = OrderedDict({p.name: 12})
        po = ParseDict(name=name)
        assert p.parent == po
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert len(po.value) == 0
        assert po.value == value1
        assert po.children is not None
        assert len(po.children) == 0
        assert po.children == value1
        assert po.data == b""

        po.value = value2
        assert po.value is not None
        assert len(po.value) == 1
        assert po.value == value3
        assert po.children is not None
        assert len(po.children) == 1
        assert po.children == value2
        assert po.data == b"\x00"

        po.value = value4
        assert po.value is not None
        assert len(po.value) == 1
        assert po.value == value4
        assert po.children is not None
        assert len(po.children) == 1
        assert po.children == value2
        assert po.data == b"\x0C"

        value = 1
        po = ParseDict(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_parsedict_parent(self) -> None:
        name = "test"
        name2 = "parent"
        po = ParseDict(name=name)
        p = UInt8(name=name2)
        value1: dict[str, Any] = dict()
        value2: OrderedDict[str, Any] = OrderedDict({p.name: p})
        value3: OrderedDict[str, Any] = OrderedDict({p.name: p.value})

        assert p.parent == po
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert len(po.value) == 0
        assert po.value == value1
        assert po.children is not None
        assert len(po.children) == 0
        assert po.children == value1
        assert po.data == b""

        po.children = value2
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert len(po.value) == 1
        assert po.value == value3
        assert po.children is not None
        assert len(po.children) == 1
        assert po.children == value2
        assert po.data == b"\x00"

    def test_parsedict_set_item(self) -> None:
        name = "test"
        po = ParseDict(name=name)
        with pytest.raises(TypeError):
            po["x"] = "popcorn"  # type:ignore

    def test_parsedict_parse_1(self) -> None:
        p_name = "test"
        p_data = b"\xff"
        f1_name = "f1"
        f1_value = 255
        f1_data = b"\xff"
        left_over = b""
        f1 = UInt8(name=f1_name)
        p_value1 = {f1_name: f1.value}
        p_value2 = {f1_name: 255}
        p = ParseDict(name=p_name)
        p[f1.name] = f1

        assert f1.parent == p
        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == b"\x00"
        assert f1.value is not None
        assert f1.value == 0
        assert p.value == p_value1

        remainder = p.parse(p_data)

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == f1_data
        assert f1.value is not None
        assert f1.value == f1_value

        assert remainder == left_over
        assert p is not None
        assert p.name == p_name
        assert p.data is not None
        assert p.data == p_data
        assert p.value is not None
        assert p.value == p_value2
        assert isinstance(p.formatted_value, str)
        assert isinstance(bytes(p), bytes)
        assert isinstance(str(p), str)
        assert p_name in str(p)
        assert f1_name in str(p)
        assert isinstance(repr(p), str)
        assert p_name in repr(p)
        assert f1_name in repr(p)
        assert ParseDict.__name__ in repr(p)

    def test_parsedict_parse_3(self) -> None:
        p_name = "test"
        p_data = b"\xaa\xbb\xcc"
        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1 = UInt8(name=f1_name)
        f2_name = "f2"
        f2_value = 187
        f2_data = b"\xbb"
        f2 = UInt8(name=f2_name)
        f3_name = "f3"
        f3_value = 204
        f3_data = b"\xcc"
        f3 = UInt8(name=f3_name)
        left_over = b""
        p_value1 = OrderedDict({f1_name: 0, f2_name: 0, f3_name: 0})
        p_value2 = OrderedDict({f1_name: f1_value, f2_name: f2_value, f3_name: f3_value})
        p = ParseDict(name=p_name)
        p[f1.name] = f1
        p[f2.name] = f2
        p[f3.name] = f3

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == b"\x00"
        assert f1.value is not None
        assert f1.value == 0

        assert f2.name == f2_name
        assert f2.data is not None
        assert f2.data == b"\x00"
        assert f2.value is not None
        assert f2.value == 0

        assert f3.name == f3_name
        assert f3.data is not None
        assert f3.data == b"\x00"
        assert f3.value is not None
        assert f3.value == 0

        assert p.value == p_value1
        remainder = p.parse(p_data)

        assert f1.parent == p
        assert f2.parent == p
        assert f3.parent == p
        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == f1_data
        assert f1.value is not None
        assert f1.value == f1_value

        assert f2.name == f2_name
        assert f2.data is not None
        assert f2.data == f2_data
        assert f2.value is not None
        assert f2.value == f2_value

        assert f3.name == f3_name
        assert f3.data is not None
        assert f3.data == f3_data
        assert f3.value is not None
        assert f3.value == f3_value

        assert remainder == left_over
        assert p is not None
        assert p.name == p_name
        assert p.data is not None
        assert p.data == p_data
        assert p.value is not None
        assert p.value == p_value2
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
        assert ParseDict.__name__ in repr(p)
