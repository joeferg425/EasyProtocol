# flake8:noqa
from __future__ import annotations

import struct
from typing import Any

import pytest
from bitarray import bitarray
from parse_data import ParseData

from easyprotocol.base.base import DEFAULT_ENDIANNESS, UNDEFINED, BaseField
from easyprotocol.fields.array import ArrayFieldGeneric
from easyprotocol.fields.unsigned_int import BoolField, UInt8Field


class TestBase:
    def test_base_parse(self) -> None:
        with pytest.raises(NotImplementedError):
            f = BaseField(name="test")
            f.parse(bitarray())

    def test_base_name(self) -> None:
        name = "test"
        f = BaseField(name=name)
        assert f.name == name
        name2 = "new name"
        f.name = name2
        assert f.name == name2

    def test_base_assign_bits_lsb(self) -> None:
        name = "test"
        bits = bitarray()
        f = BaseField(name=name)
        with pytest.raises(NotImplementedError):
            assert f.set_bits_lsb(bits=bits)

    def test_base_set_children_list(self) -> None:
        name = "test"
        name1 = "child1"
        name2 = "child2"
        name3 = "child3"
        f = BaseField(name=name)
        f1 = BaseField(name=name1)
        f2 = BaseField(name=name2)
        f3 = BaseField(name=name3)
        children = {name1: f1, name2: f2, name3: f3}

        assert f.children == {}
        f.children = [f1, f2, f3]
        assert f.children == children

    def test_base_set_children_dict(self) -> None:
        name = "test"
        name1 = "child1"
        name2 = "child2"
        name3 = "child3"
        f = BaseField(name=name)
        f1 = BaseField(name=name1)
        f2 = BaseField(name=name2)
        f3 = BaseField(name=name3)
        children = {name1: f1, name2: f2, name3: f3}

        assert f.children == {}
        f.children = {name1: f1, name2: f2, name3: f3}
        assert f.children == children

    def test_base_set_children_invalid(self) -> None:
        name = "test"
        f = BaseField(name=name)
        with pytest.raises(TypeError):
            f.children = 0  # pyright:ignore[reportGeneralTypeIssues]

    def test_base_value_as_string(self) -> None:
        name = "test"
        f = BaseField(name=name)
        assert f.value_as_string == UNDEFINED

    def test_base_get_bytes(self) -> None:
        name = "test"
        f = BaseField(name=name)
        assert f.value_as_bytes == b""

    def test_base_get_hex_string(self) -> None:
        name = "test"
        bts = b"\xAB\xCD\xEF"
        hex_string = "AB CD EF"
        bits = bitarray()
        bits.frombytes(bts)
        f = BaseField(name=name)
        f._bits = bits  # pyright:ignore[reportPrivateUsage]
        assert f.value_as_hex_string == hex_string

    def test_base_get_bits_string(self) -> None:
        name = "test"
        bts = b"\x11"
        bit_string = "00010001:<b"
        bits = bitarray()
        bits.frombytes(bts)
        f = BaseField(name=name)
        f._bits = bits  # pyright:ignore[reportPrivateUsage]
        assert f.value_as_binary_string == bit_string

    def test_base_get_bits_string_lsb(self) -> None:
        name = "test"
        bts = b"\x11"
        bit_string = "b>:00010001"
        bits = bitarray()
        bits.frombytes(bts)
        f = BaseField(name=name)
        f._bits = bits  # pyright:ignore[reportPrivateUsage]
        assert f.value_as_binary_string_lsb == bit_string

    def test_base_string_format(self) -> None:
        name = "test"
        format1 = "{}"
        format2 = "test: {}"
        f = BaseField(name=name)
        assert f.string_format == format1
        f.string_format = format2
        assert f.string_format == format2

    def test_base_value_get(self) -> None:
        name = "test"
        f = BaseField(name=name)
        with pytest.raises(NotImplementedError):
            f.value

    def test_base_value_set(self) -> None:
        name = "test"
        f = BaseField(name=name)
        with pytest.raises(NotImplementedError):
            f.value = 0
