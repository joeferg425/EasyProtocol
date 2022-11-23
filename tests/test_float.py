from __future__ import annotations
import pytest
import struct
from bitarray import bitarray
from collections import OrderedDict
from easyprotocol.base.parse_object import ParseObject
from typing import Any
from easyprotocol.fields.float import Float32Field, FloatField, FLOAT_STRING_FORMAT
from test_parse_object import (
    check_parseobject_children,
    check_parseobject_properties,
    check_parseobject_strings,
    TestData,
)
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


def check_float_value(
    obj: ParseObject[Any],
    tst: TestData,
) -> None:
    assert (
        obj.value == tst.value
    ), f"{obj}: obj.value is not the expected value ({obj.value:.3e} != expected value: {tst.value:.3e})"


def check_float(
    obj: ParseObject[Any],
    tst: TestData,
) -> None:
    check_parseobject_properties(
        obj=obj,
        tst=tst,
    )
    check_parseobject_children(
        obj=obj,
        tst=tst,
    )
    check_float_value(
        obj=obj,
        tst=tst,
    )
    check_parseobject_strings(
        obj=obj,
        tst=tst,
    )


class TestFloatField:
    def test_floatfield_create_empty_big_endian(self) -> None:
        value = 0.0
        byte_data = struct.pack(">f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        with pytest.raises(NotImplementedError):
            FloatField(
                name=tst.name,
                bit_count=32,
                endian=tst.endian,
            )

    def test_floatfield_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format=FLOAT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        with pytest.raises(NotImplementedError):
            FloatField(
                name=tst.name,
                bit_count=32,
                endian=tst.endian,
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
            format=FLOAT_STRING_FORMAT,
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
            format=FLOAT_STRING_FORMAT,
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
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_FLOAT_BE,
    )
    def test_float32field_create_parse_bytes_big_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format=FLOAT_STRING_FORMAT,
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
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_FLOAT_LE,
    )
    def test_float32field_create_parse_bytes_little_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format=FLOAT_STRING_FORMAT,
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
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_FLOAT_BE,
    )
    def test_float32field_create_init_value_big_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format=FLOAT_STRING_FORMAT,
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
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_FLOAT_LE,
    )
    def test_float32field_create_init_value_little_endian(
        self, byte_data: bytes, value: float, bits_data: bitarray
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format=FLOAT_STRING_FORMAT,
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
            format=FLOAT_STRING_FORMAT,
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
            format=FLOAT_STRING_FORMAT,
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
            format=FLOAT_STRING_FORMAT,
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
            format=FLOAT_STRING_FORMAT,
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
        tst.parent = ParseObject(name="parent")
        obj.parent = tst.parent
        check_float(
            obj=obj,
            tst=tst,
        )

    def test_float32field_set_children(self) -> None:
        child = ParseObject(name="child")
        value = 0.0
        byte_data = struct.pack(">f", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format=FLOAT_STRING_FORMAT,
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
