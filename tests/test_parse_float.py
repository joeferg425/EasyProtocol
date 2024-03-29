# flake8:noqa
from __future__ import annotations

import math
import struct
from collections import OrderedDict
from typing import Any, Literal

import pytest
from bitarray import bitarray
from parse_data import PARAMETER_NAMES, TEST_VALUES_32_BIT_UINT, ParseData

from easyprotocol.base.parse_base import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.utils import hex
from easyprotocol.fields.float import FLOAT_STRING_FORMAT, Float32Field, FloatField


def get_float_value(value: int) -> float:
    return struct.unpack("<f", struct.pack("<I", value))[0]


def get_bytes(value: float, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">f", struct.unpack(">f", struct.pack(">I", value))[0])
    else:
        return struct.pack("<f", struct.unpack("<f", struct.pack("<I", value))[0])


def get_bitarray(value: float, endian: Literal["little", "big"]) -> bitarray:
    byte_val = get_bytes(value=value, endian=endian)
    bits = bitarray(endian="big")
    bits.frombytes(byte_val)
    return bits


TEST_VALUES_32_BIT_FLOAT_LE = [
    pytest.param(
        get_float_value(value),
        32,
        get_bytes(value, "little"),
        get_bitarray(value, "little"),
        "little",
        id=f'{get_float_value(value)}, "{hex(get_bytes(value, "little"))}", "{get_bitarray(value, "little").to01()}", "little"',
    )
    for value in TEST_VALUES_32_BIT_UINT
]
TEST_VALUES_32_BIT_FLOAT_BE = [
    pytest.param(
        get_float_value(value),
        32,
        get_bytes(value, "big"),
        get_bitarray(value, "big"),
        "big",
        id=f'{get_float_value(value)}, "{hex(get_bytes(value, "big"))}", "{get_bitarray(value, "big").to01()}", "big"',
    )
    for value in TEST_VALUES_32_BIT_UINT
]


def check_float_value(
    obj: FloatField[Any],
    tst: ParseData,
) -> None:
    if not math.isnan(obj.value):
        assert (
            obj.value == tst.value
        ), f"{obj}: obj.value is not the expected value ({obj.value:.3e} != expected value: {tst.value:.3e})"
    else:
        assert math.isnan(obj.value) and math.isnan(
            tst.value
        ), f"{obj}: obj.value is not the expected value ({obj.value:.3e} != expected value: {tst.value:.3e})"


def check_float_properties(
    obj: FloatField[int],
    tst: ParseData,
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
        obj.byte_value == tst.byte_data
    ), f"{obj}: bytes(obj) is not the expected value ({bytes(obj)!r} != expected value: {tst.byte_data!r})"
    assert (
        obj.endian == tst.endian
    ), f"{obj}: obj.endian is not the expected value ({obj.endian} != expected value: {tst.endian})"


def check_float_children(
    obj: FloatField[int],
    tst: ParseData,
) -> None:
    assert len(obj._children) == len(tst.children), (  # pyright:ignore[reportPrivateUsage]
        f"{obj}: len(obj.children) is not the expected value "
        + f"({len(obj._children)} != expected value: {len(tst.children)})"  # pyright:ignore[reportPrivateUsage]
    )
    assert obj._children.keys() == tst.children.keys(), (  # pyright:ignore[reportPrivateUsage]
        f"{obj}: obj.children.keys() is not the expected value "
        + f"({obj._children.keys()} != expected value: {tst.children.keys()})"  # pyright:ignore[reportPrivateUsage]
    )
    for key in tst.children.keys():
        assert obj._children[key] == tst.children[key], (  # pyright:ignore[reportPrivateUsage]
            f"{obj}: obj.children[key] is not the expected value "
            + f"({obj._children[key]} != expected value: {tst.children[key]})"  # pyright:ignore[reportPrivateUsage]
        )
        assert obj._children[key]._parent == obj, (  # pyright:ignore[reportPrivateUsage]
            f"{obj}: obj.children[key].parent is not the expected value "
            + f"({obj._children[key]._parent} != expected value: {obj})"  # pyright:ignore[reportPrivateUsage]
        )

    for v in tst.children.values():
        assert v.string_value in obj.string_value
        assert v.string_value in str(obj)
        assert v.string_value in repr(obj)
    assert tst.name in str(obj)
    assert tst.name in repr(obj)


def check_float_strings(
    obj: FloatField[int],
    tst: ParseData,
) -> None:
    assert tst.string_format.format(tst.value) == obj.string_value, (
        f"{obj}: obj.string_value is not the expected value "
        + f"({tst.string_format.format(tst.value)} != expected value: {obj.string_value})"
    )
    assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.string_value in str(
        obj
    ), f"{obj}: obj.string_value is not in the object's string vale ({obj.string_value} not in {str(obj)})"
    assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.string_value in repr(
        obj
    ), f"{obj}: obj.string_value is not in the object's repr vale ({obj.string_value} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def check_float(
    obj: FloatField[Any],
    tst: ParseData,
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
        tst = ParseData(
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
        tst = ParseData(
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
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_FLOAT_BE,
    )
    def test_float32field_create_parse_bytes_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
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
            data=byte_data,
            endian=endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_FLOAT_LE,
    )
    def test_float32field_create_parse_bytes_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
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
            endian=endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_FLOAT_BE,
    )
    def test_float32field_create_init_value_big_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
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
            default=value,
            endian=endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_FLOAT_LE,
    )
    def test_float32field_create_init_value_little_endian(
        self,
        value: int,
        bit_count: int,
        byte_data: bytes,
        bits_data: bitarray,
        endian: endianT,
    ) -> None:
        tst = ParseData(
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
            default=value,
            endian=endian,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

    def test_float32field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFF
        value2 = 0xFFFFFFFF
        byte_data1 = struct.pack("f", struct.unpack("f", struct.pack("I", value1))[0])
        byte_data1 += byte_data1
        byte_data2 = struct.pack("f", struct.unpack("f", struct.pack("I", value2))[0])
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = Float32Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_float32field_create_parse_too_little_data(self) -> None:
        value = 0xFFFFFFFF
        byte_data = struct.pack("f", struct.unpack("f", struct.pack("I", value))[0])
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = Float32Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_float32field_set_name(self) -> None:
        value = 0.0
        byte_data = struct.pack(">f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
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
            default=tst.value,
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
        bits_data1 = bitarray(endian="big")
        bits_data1.frombytes(byte_data1)
        value2 = 7.0
        byte_data2 = struct.pack(">f", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
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
            default=tst.value,
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
        bits_data1 = bitarray(endian="big")
        bits_data1.frombytes(byte_data1)
        value2 = 7.0
        byte_data2 = struct.pack(">f", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
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
            default=tst.value,
        )
        check_float(
            obj=obj,
            tst=tst,
        )

        obj.bits_lsb = bits_data2
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
        tst = ParseData(
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
            default=tst.value,
        )
        check_float(
            obj=obj,
            tst=tst,
        )
        tst.parent = Float32Field(
            name="parent",
            endian=tst.endian,
            default=tst.value,
        )
        obj.parent = tst.parent
        check_float(
            obj=obj,
            tst=tst,
        )
