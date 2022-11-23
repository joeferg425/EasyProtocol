from __future__ import annotations
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Literal
import pytest
from easyprotocol.base.parse_object import ParseObject
from bitarray import bitarray


@dataclass
class TestData:
    name: str
    value: Any
    endian: Literal["big", "little"]
    format: str
    bits_data: bitarray
    byte_data: bytes | bytearray
    parent: ParseObject[Any] | None
    children: OrderedDict[str, ParseObject[Any]]


def check_parseobject_properties(
    obj: ParseObject[Any],
    tst: TestData,
) -> None:
    assert obj is not None, "Object is None"
    assert obj.name == tst.name, f"{obj}: obj.name is not the expected value ({obj.name} != expected value: {tst.name})"
    assert (
        obj.format == tst.format
    ), f"{obj}: obj.format is not the expected value ({obj.format} != expected value: {tst.format})"
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


def check_parseobject_children(
    obj: ParseObject[Any],
    tst: TestData,
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
        assert v.formatted_value in obj.formatted_value
        assert v.formatted_value in str(obj)
        assert v.formatted_value in repr(obj)
    assert tst.name in str(obj)
    assert tst.name in repr(obj)


def check_parseobject_value(
    obj: ParseObject[Any],
    tst: TestData,
) -> None:
    assert (
        obj.value == tst.value
    ), f"{obj}: obj.value is not the expected value ({obj.value} != expected value: {tst.value})"


def check_parseobject_strings(
    obj: ParseObject[Any],
    tst: TestData,
) -> None:
    assert tst.format.format(tst.value) == obj.formatted_value, (
        f"{obj}: obj.formatted_value is not the expected value "
        + f"({tst.format.format(tst.value)} != expected value: {obj.formatted_value})"
    )
    assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.formatted_value in str(
        obj
    ), f"{obj}: obj.formatted_value is not in the object's string vale ({obj.formatted_value} not in {str(obj)})"
    assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.formatted_value in repr(
        obj
    ), f"{obj}: obj.formatted_value is not in the object's repr vale ({obj.formatted_value} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def check_parseobject(
    obj: ParseObject[Any],
    tst: TestData,
) -> None:
    check_parseobject_value(
        obj=obj,
        tst=tst,
    )
    check_parseobject_properties(
        obj=obj,
        tst=tst,
    )
    check_parseobject_children(
        obj=obj,
        tst=tst,
    )
    check_parseobject_strings(
        obj=obj,
        tst=tst,
    )


class TestParseObject:
    def test_parseobject_create_empty(self) -> None:
        endian: Literal["big", "little"] = "little"
        tst = TestData(
            name="test",
            value=None,
            format="{}",
            byte_data=b"",
            bits_data=bitarray(endian="little"),
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = ParseObject(name=tst.name)
        check_parseobject(
            obj=obj,
            tst=tst,
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
        endian: Literal["big", "little"] = "little"
        tst = TestData(
            name="test",
            value=None,
            format="{}",
            byte_data=b"",
            bits_data=bitarray(endian="little"),
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = ParseObject(name=tst.name)
        check_parseobject(
            obj=obj,
            tst=tst,
        )
        tst.name = "new_name"
        obj.name = tst.name

        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_parseobject_set_value(self) -> None:
        endian: Literal["big", "little"] = "little"
        tst = TestData(
            name="test",
            value=None,
            format="{}",
            byte_data=b"",
            bits_data=bitarray(endian="little"),
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = ParseObject(name=tst.name)
        check_parseobject(
            obj=obj,
            tst=tst,
        )
        with pytest.raises(NotImplementedError):
            obj.value = 1

    def test_parseobject_set_bits(self) -> None:
        endian: Literal["big", "little"] = "little"
        tst = TestData(
            name="test",
            format="{}",
            value=None,
            byte_data=b"",
            bits_data=bitarray(endian="little"),
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = ParseObject(name=tst.name)
        check_parseobject(
            obj=obj,
            tst=tst,
        )
        tst.byte_data = b"\x01"
        tst.bits_data = bitarray(endian="little")
        tst.bits_data.frombytes(tst.byte_data)
        obj._bits = tst.bits_data
        check_parseobject(
            obj=obj,
            tst=tst,
        )
        with pytest.raises(NotImplementedError):
            obj.bits = tst.bits_data

    def test_parseobject_set_parent(self) -> None:
        endian: Literal["big", "little"] = "little"
        tst = TestData(
            name="test",
            format="{}",
            value=None,
            byte_data=b"",
            bits_data=bitarray(endian="little"),
            parent=None,
            children=OrderedDict(),
            endian=endian,
        )
        obj = ParseObject(name=tst.name)
        check_parseobject(
            obj=obj,
            tst=tst,
        )
        tst.parent = ParseObject(name="parent")
        obj.parent = tst.parent
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_parseobject_set_children(self) -> None:
        endian: Literal["big", "little"] = "little"
        child = ParseObject(name="child")
        tst = TestData(
            name="test",
            format="{}",
            value=None,
            byte_data=b"",
            bits_data=bitarray(endian="little"),
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = ParseObject(name=tst.name)
        check_parseobject(
            obj=obj,
            tst=tst,
        )
        tst.children = OrderedDict({child.name: child})
        obj.children = tst.children
        check_parseobject(
            obj=obj,
            tst=tst,
        )
