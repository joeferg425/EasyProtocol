from collections import OrderedDict
from typing import Any
import pytest
from easyprotocol.parse_object import ParseObject
from bitarray import bitarray


class TestParseObject:
    def test_parseobject_create_empty(self) -> None:
        name = "test"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        po = ParseObject(name=name)
        assert po is not None
        assert po.name == name
        assert po.value is None
        assert po.bits is not None
        assert po.bits == bitarray()
        assert po.parent is None
        assert po.children is not None
        assert po.children == children
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseObject.__name__ in repr(po)

    def test_parseobject_create_parse(self) -> None:
        name = "test"
        data = b"\x00"
        with pytest.raises(NotImplementedError):
            ParseObject(name=name, data=data)

    def test_parseobject_create_value(self) -> None:
        name = "test"
        value = 11
        with pytest.raises(NotImplementedError):
            ParseObject(name=name, value=value)

    def test_parseobject_name(self) -> None:
        name1 = "test"
        name2 = "new_name"
        po = ParseObject(name=name1)
        assert po.name == name1
        po.name = name2
        assert po.name == name2

    def test_parseobject_value(self) -> None:
        name = "test"
        value = 1
        po = ParseObject(name=name)
        assert po.value is None
        po._value = value
        assert po.value == value
        with pytest.raises(NotImplementedError):
            po.value = value

    def test_parseobject_bits(self) -> None:
        name = "test"
        data = b"\x01"
        bits = bitarray()
        bits.frombytes(data)
        po = ParseObject(name=name)
        assert po.bits is not None
        po._bits = bits
        assert po.bits == bits
        with pytest.raises(AttributeError):
            po.bits = data  # type:ignore

    def test_parseobject_parent(self) -> None:
        name = "test"
        p = ParseObject(name="parent")
        po = ParseObject(name=name)
        assert po.parent is None
        po.parent = p
        assert po.parent == p

    def test_parseobject_children(self) -> None:
        name = "test"
        p = ParseObject(name="child")
        children1: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObject[Any]] = OrderedDict({p.name: p})
        po = ParseObject(name=name)
        assert po.children is not None
        assert len(po.children) == 0
        assert po.children == children1
        po.children = children2
        assert len(po.children) == 1
        assert po.children == children2
