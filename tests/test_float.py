from __future__ import annotations
import pytest
import struct
from bitarray import bitarray
from collections import OrderedDict
from easyprotocol.base.parse_object import ParseObject
from typing import Any
from easyprotocol.fields.float import Float32Field
from test_parse_object import parseobject_children, parseobject_properties, parseobject_strings, TestData
from test_uint import TEST_VALUES_32_BIT, get_bitarray

TEST_VALUES_32_BIT_FLOAT_LE = [
    pytest.param(
        v,
        struct.unpack(
            "<f",
            v,
        )[0],
        get_bitarray(v),
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
    )
    for v in TEST_VALUES_32_BIT
]


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
        bits_data = bitarray(endian="little")
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
        bits_data = bitarray(endian="little")
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
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_FLOAT_BE,
    )
    def test_float32_create_parse_bytes_big_endian(self, byte_data: bytes, value: float, bits_data: bitarray) -> None:
        bits_data = bitarray(endian="little")
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
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_FLOAT_LE,
    )
    def test_float32_create_parse_bytes_little_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray
    ) -> None:
        bits_data = bitarray(endian="little")
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
            data=byte_data,
            endian=tst.endian,
        )
        float_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_FLOAT_BE,
    )
    def test_float32_create_init_value_big_endian(self, byte_data: bytes, value: float, bits_data: bitarray) -> None:
        bits_data = bitarray(endian="little")
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
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_FLOAT_LE,
    )
    def test_float32_create_init_value_little_endian(self, byte_data: bytes, value: float, bits_data: bitarray) -> None:
        bits_data = bitarray(endian="little")
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
            value=tst.value,
            endian=tst.endian,
        )
        float_tests(
            obj=obj,
            tst=tst,
        )
