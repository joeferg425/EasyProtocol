from __future__ import annotations
from collections import OrderedDict
from typing import Any, Literal
import pytest
from easyprotocol.base.parse_object import ParseObject
from bitarray import bitarray


def parseobject_properties(
    obj: ParseObject[Any],
    name: str,
    format: str,
    bits_data: bitarray,
    byte_data: bytes,
    parent: ParseObject[Any] | None,
    endian: Literal["little", "big"],
) -> None:
    assert obj is not None, "Object is None"
    assert obj.name == name, f"{obj}: obj.name is not the expected value ({obj.name} != expected value: {name})"
    assert (
        obj.format == format
    ), f"{obj}: obj.format is not the expected value ({obj.format} != expected value: {format})"
    assert (
        obj.bits == bits_data
    ), f"{obj}: obj.bits is not the expected value ({obj.bits} != expected value: {bits_data})"
    assert (
        obj.parent == parent
    ), f"{obj}: obj.parent is not the expected value ({obj.parent} != expected value: {parent})"
    assert (
        bytes(obj) == byte_data
    ), f"{obj}: bytes(obj) is not the expected value ({bytes(obj)!r} != expected value: {byte_data!r})"
    assert (
        obj.endian == endian
    ), f"{obj}: obj.endian is not the expected value ({obj.endian} != expected value: {endian})"


def parseobject_children(
    obj: ParseObject[Any],
    name: str,
    children: OrderedDict[str, ParseObject[Any]],
    parent: ParseObject[Any] | None,
) -> None:
    assert len(obj.children) == len(children), (
        f"{obj}: len(obj.children) is not the expected value "
        + f"({len(obj.children)} != expected value: {len(children)})"
    )
    assert obj.children.keys() == children.keys(), (
        f"{obj}: obj.children.keys() is not the expected value "
        + f"({obj.children.keys()} != expected value: {children.keys()})"
    )
    for key in children.keys():
        assert obj.children[key] == children[key], (
            f"{obj}: obj.children[key] is not the expected value "
            + f"({obj.children[key]} != expected value: {children[key]})"
        )
        assert obj.children[key].parent == obj, (
            f"{obj}: obj.children[key].parent is not the expected value "
            + f"({obj.children[key].parent} != expected value: {obj})"
        )

    for v in children.values():
        assert v.formatted_value in obj.formatted_value
        assert v.formatted_value in str(obj)
        assert v.formatted_value in repr(obj)
    assert name in str(obj)
    assert name in repr(obj)


def parseobject_value(
    obj: ParseObject[Any],
    value: Any | None,
) -> None:
    assert (
        obj.value == value
    ), f"{obj}: obj.value is not the expected value ({obj.value:X} != expected value: {value:X})"


def parseobject_strings(
    obj: ParseObject[Any],
    name: str,
    value: Any | None,
    format: str,
) -> None:
    assert format.format(value) == obj.formatted_value, (
        f"{obj}: obj.formatted_value is not the expected value "
        + f"({format.format(value)} != expected value: {obj.formatted_value})"
    )
    assert name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.formatted_value in str(
        obj
    ), f"{obj}: obj.formatted_value is not in the object's string vale ({obj.formatted_value} not in {str(obj)})"
    assert name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.formatted_value in repr(
        obj
    ), f"{obj}: obj.formatted_value is not in the object's repr vale ({obj.formatted_value} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def parseobject_tests(
    obj: ParseObject[Any],
    name: str,
    value: Any | None,
    format: str,
    bits_data: bitarray,
    byte_data: bytes,
    parent: ParseObject[Any] | None,
    children: OrderedDict[str, ParseObject[Any]],
    endian: Literal["little", "big"],
) -> None:
    parseobject_properties(
        obj=obj,
        name=name,
        format=format,
        bits_data=bits_data,
        byte_data=byte_data,
        parent=parent,
        endian=endian,
    )
    parseobject_children(
        obj=obj,
        name=name,
        children=children,
        parent=parent,
    )
    parseobject_value(
        obj=obj,
        value=value,
    )
    parseobject_strings(
        obj=obj,
        name=name,
        value=value,
        format=format,
    )


class TestParseObject:
    def test_parseobject_create_empty(self) -> None:
        name = "test"
        value = None
        format = "{}"
        byte_data = b""
        bits_data = bitarray()
        parent = None
        endian: Literal["big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = ParseObject(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

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

    def test_parseobject_set_name(self) -> None:
        name1 = "test"
        name2 = "new_name"
        value = None
        format = "{}"
        byte_data = b""
        bits_data = bitarray()
        parent = None
        endian: Literal["big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = ParseObject(name=name1)
        parseobject_tests(
            obj=obj,
            name=name1,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )
        obj.name = name2
        parseobject_tests(
            obj=obj,
            name=name2,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    def test_parseobject_set_value(self) -> None:
        name = "test"
        value1 = None
        value2 = 1
        format = "{}"
        byte_data = b""
        bits_data = bitarray()
        parent = None
        endian: Literal["big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = ParseObject(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value1,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )
        obj._value = value2
        parseobject_tests(
            obj=obj,
            name=name,
            value=value2,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )
        with pytest.raises(NotImplementedError):
            obj.value = value2

    def test_parseobject_set_bits(self) -> None:
        name = "test"
        format = "{}"
        value = None
        byte_data1 = b""
        byte_data2 = b"\x01"
        bits_data1 = bitarray()
        bits_data2 = bitarray()
        bits_data2.frombytes(byte_data2)
        parent = None
        endian: Literal["big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = ParseObject(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data1,
            byte_data=byte_data1,
            parent=parent,
            children=children,
            endian=endian,
        )
        obj._bits = bits_data2
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data2,
            byte_data=byte_data2,
            parent=parent,
            children=children,
            endian=endian,
        )
        with pytest.raises(AttributeError):
            obj.bits = byte_data2  # type:ignore

    def test_parseobject_set_parent(self) -> None:
        name = "test"
        format = "{}"
        value = None
        byte_data = b""
        bits_data = bitarray()
        parent1 = None
        parent2 = ParseObject(name="parent")
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["big"] = "big"
        obj = ParseObject(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent1,
            children=children,
            endian=endian,
        )
        obj.parent = parent2
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent2,
            children=children,
            endian=endian,
        )

    def test_parseobject_set_children(self) -> None:
        name = "test"
        format = "{}"
        value = None
        byte_data = b""
        bits_data = bitarray()
        parent = None
        child = ParseObject(name="child")
        endian: Literal["big"] = "big"
        children1: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        children2: OrderedDict[str, ParseObject[Any]] = OrderedDict({child.name: child})
        obj = ParseObject(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children1,
            endian=endian,
        )
        obj.children = children2
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children2,
            endian=endian,
        )
