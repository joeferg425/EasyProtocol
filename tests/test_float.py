from __future__ import annotations
from dataclasses import dataclass
import pytest
import struct
from bitarray import bitarray
from collections import OrderedDict
from easyprotocol.base.parse_object import ParseObject
from typing import Any, Literal
from easyprotocol.fields.float import Float32Field
from test_parse_object import parseobject_children, parseobject_properties, parseobject_strings, TestData
from test_uint import TEST_VALUES_32_BIT

TEST_BYTES_32_BIT = [struct.pack(">I", v) for v in TEST_VALUES_32_BIT]


def float_value(
    obj: ParseObject[Any],
    tst: TestData,
) -> None:
    assert (
        obj.value == tst.value
    ), f"{obj}: obj.value is not the expected value ({obj.value:.3e} != expected value: {tst.value:.3e})"


def float_tests(
    obj: ParseObject[Any],
    tst: TestData,
) -> None:
    parseobject_properties(
        obj=obj,
        tst=tst,
    )
    parseobject_children(
        obj=obj,
        tst=tst,
    )
    float_value(
        obj=obj,
        tst=tst,
    )
    parseobject_strings(
        obj=obj,
        tst=tst,
    )


class TestFloat32:
    def test_float32_create_empty_big_endian(self) -> None:
        value = 0.0
        byte_data = struct.pack(">f", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:.3e}",
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
        float_tests(
            obj=obj,
            tst=tst,
        )

    def test_float32_create_empty_little_endian(self) -> None:
        value = 0.0
        byte_data = struct.pack("<f", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:.3e}",
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
        float_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        "byte_data",
        TEST_BYTES_32_BIT,
    )
    def test_float32_create_parse_bytes_big_endian(self, byte_data: bytes) -> None:
        temp = bytearray(byte_data)
        temp.reverse()
        value = struct.unpack(">f", temp)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:.3e}",
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
        float_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        "byte_data",
        TEST_BYTES_32_BIT,
    )
    def test_float32_create_parse_bytes_little_endian(self, byte_data: bytes) -> None:
        temp = bytearray(byte_data)
        temp.reverse()
        value = struct.unpack("<f", temp)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:.3e}",
            byte_data=temp,
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
        float_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        "byte_data",
        TEST_BYTES_32_BIT,
    )
    def test_float32_create_init_value_big_endian(self, byte_data: bytes) -> None:
        temp = bytearray(byte_data)
        value = struct.unpack(">f", temp)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:.3e}",
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
        float_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        "byte_data",
        TEST_BYTES_32_BIT,
    )
    def test_float32_create_init_value_little_endian(self, byte_data: bytes) -> None:
        temp = bytearray(byte_data)
        value = struct.unpack("<f", temp)[0]
        temp_bytes = struct.pack(">f", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:.3e}",
            byte_data=temp_bytes,
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
        float_tests(
            obj=obj,
            tst=tst,
        )
