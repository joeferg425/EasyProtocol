from __future__ import annotations

import struct
from collections import OrderedDict
from typing import Any, Literal

import pytest
from bitarray import bitarray
from test_parse_object import TestData
from test_uint import TEST_VALUES_32_BIT, get_bitarray

from easyprotocol.base.parse_base import ParseBase
from easyprotocol.fields.float import FLOAT_STRING_FORMAT, Float32Field, FloatField

TEST_VALUES_32_BIT_FLOAT_LE = [
    pytest.param(
        v,
        struct.unpack(
            "<f",
            v,
        )[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_32_BIT_FLOAT_BE = [
    pytest.param(
        v,
        struct.unpack(
            ">f",
            v,
        )[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_32_BIT
]


def check_float_value(
    obj: FloatField[Any],
    tst: TestData,
) -> None:
    assert (
        obj.value == tst.value
    ), f"{obj}: obj.value is not the expected value ({obj.value:.3e} != expected value: {tst.value:.3e})"


def check_float_properties(
    obj: FloatField[int],
    tst: TestData,
) -> None:
    assert obj is not None, "Object is None"
    assert obj.name == tst.name, f"{obj}: obj.name is not the expected value ({obj.name} != expected value: {tst.name})"
    assert (
        obj.string_format == tst.string_format
    ), f"{obj}: obj.format is not the expected value ({obj.string_format} != expected value: {tst.string_format})"
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


def check_float_children(
    obj: FloatField[int],
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
        assert v.string in obj.string
        assert v.string in str(obj)
        assert v.string in repr(obj)
    assert tst.name in str(obj)
    assert tst.name in repr(obj)


def check_float_strings(
    obj: FloatField[int],
    tst: TestData,
) -> None:
    assert tst.string_format.format(tst.value) == obj.string, (
        f"{obj}: obj.string is not the expected value "
        + f"({tst.string_format.format(tst.value)} != expected value: {obj.string})"
    )
    assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.string in str(
        obj
    ), f"{obj}: obj.string is not in the object's string vale ({obj.string} not in {str(obj)})"
    assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.string in repr(
        obj
    ), f"{obj}: obj.string is not in the object's repr vale ({obj.string} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def check_float(
    obj: FloatField[Any],
    tst: TestData,
) -> None:
    check_float_properties(
        obj=obj,
        tst=tst,
    )
    check_float_children(
        obj=obj,
        tst=tst,
    )
    check_float_value(
        obj=obj,
        tst=tst,
    )
    check_float_strings(
        obj=obj,
        tst=tst,
    )


class TestFloat32:
    def test_float32field_create_empty_big_endian(self) -> None:
        value = 0.0
        byte_data = struct.pack(">f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Float32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    def test_float32field_create_empty_little_endian(self) -> None:
        value = 0.0
        byte_data = struct.pack("<f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Float32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_FLOAT_BE,
    )
    def test_float32field_create_parse_bytes_big_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Float32Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_FLOAT_LE,
    )
    def test_float32field_create_parse_bytes_little_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Float32Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_FLOAT_BE,
    )
    def test_float32field_create_init_value_big_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Float32Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_FLOAT_LE,
    )
    def test_float32field_create_init_value_little_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Float32Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    def test_float32field_set_name(self) -> None:
        value = 0.0
        byte_data = struct.pack(">f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = Float32Field(
            name=tst.name,
            endian=tst.endian,
            value=tst.value,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

        tst.name = "new_name"
        obj.name = tst.name
        check_float(
            obj=obj,
            tst=tst,
        )

    def test_float32field_set_value(self) -> None:
        value1 = 0.0
        byte_data1 = struct.pack(">f", value1)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 7.0
        byte_data2 = struct.pack(">f", value2)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        tst = TestData(
            name="test",
            value=value1,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = Float32Field(
            name=tst.name,
            endian=tst.endian,
            value=tst.value,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

        obj.value = value2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_float(
            obj=obj,
            tst=tst,
        )

    def test_float32field_set_bits(self) -> None:
        value1 = 0.0
        byte_data1 = struct.pack(">f", value1)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 7.0
        byte_data2 = struct.pack(">f", value2)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        tst = TestData(
            name="test",
            value=value1,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = Float32Field(
            name=tst.name,
            endian=tst.endian,
            value=tst.value,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

        obj.bits = bits_data2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_float(
            obj=obj,
            tst=tst,
        )

    def test_float32field_set_parent(self) -> None:
        value = 0.0
        byte_data = struct.pack(">f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = Float32Field(
            name=tst.name,
            endian=tst.endian,
            value=tst.value,
        )
        check_float(
            obj=obj,
            tst=tst,
        )
        tst.parent = ParseBase(name="parent")
        obj.parent = tst.parent
        check_float(
            obj=obj,
            tst=tst,
        )

    def test_float32field_set_children(self) -> None:
        child = ParseBase(name="child")
        value = 0.0
        byte_data = struct.pack(">f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            string_format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = Float32Field(
            name=tst.name,
            endian=tst.endian,
            value=tst.value,
        )
        check_float(
            obj=obj,
            tst=tst,
        )
        with pytest.raises(NotImplementedError):
            obj.children = OrderedDict({child.name: child})
