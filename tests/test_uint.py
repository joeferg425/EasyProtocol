from collections import OrderedDict
from typing import Literal
import pytest
from easyprotocol.fields.unsigned_int import UInt8Field, UInt16Field, UInt32Field, UInt64Field, UInt24Field
from bitarray import bitarray
from test_parse_object import parseobject_tests, TestData
import struct


def get_bitarray(b: bytes) -> bitarray:
    bits = bitarray(endian="little")
    bits.frombytes(b)
    return bits


TEST_VALUES_08_BIT = [
    b"\x00",
    b"\x01",
    b"\x10",
    b"\x80",
    b"\xFF",
]
TEST_VALUES_08_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<B", v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_08_BIT
]
TEST_VALUES_08_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">B", v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_08_BIT
]
TEST_VALUES_16_BIT = [
    b"\x00\x00",
    b"\x00\x01",
    b"\x00\x10",
    b"\x00\x80",
    b"\x00\xFF",
    b"\x01\x00",
    b"\x08\x00",
    b"\x10\x00",
    b"\x80\x00",
    b"\xFF\x00",
]
TEST_VALUES_16_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<H", v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_16_BIT
]
TEST_VALUES_16_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">H", v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_16_BIT
]
TEST_VALUES_24_BIT = [
    b"\x00\x00\x00",
    b"\x00\x00\x01",
    b"\x00\x00\x10",
    b"\x00\x00\x80",
    b"\x00\x00\xFF",
    b"\x00\x01\x00",
    b"\x00\x10\x00",
    b"\x00\x80\x00",
    b"\x00\xFF\x00",
    b"\x01\x00\x00",
    b"\x10\x00\x00",
    b"\x80\x00\x00",
    b"\xFF\x00\x00",
]
TEST_VALUES_24_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<I", v + b"\x00")[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_24_BIT
]
TEST_VALUES_24_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">I", b"\x00" + v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_24_BIT
]
TEST_VALUES_32_BIT = [
    b"\x00\x00\x00\x00",
    b"\x00\x00\x00\x01",
    b"\x00\x00\x00\x10",
    b"\x00\x00\x00\x80",
    b"\x00\x00\x00\xFF",
    b"\x00\x00\x01\x00",
    b"\x00\x00\x10\x00",
    b"\x00\x00\x80\x00",
    b"\x00\x00\xFF\x00",
    b"\x00\x01\x00\x00",
    b"\x00\x10\x00\x00",
    b"\x00\x80\x00\x00",
    b"\x00\xFF\x00\x00",
    b"\x01\x00\x00\x00",
    b"\x10\x00\x00\x00",
    b"\x80\x00\x00\x00",
    b"\xFF\x00\x00\x00",
]
TEST_VALUES_32_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<I", v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_32_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">I", v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_64_BIT = [
    b"\x00\x00\x00\x00\x00\x00\x00\x00",
    b"\x00\x00\x00\x00\x00\x00\x00\x01",
    b"\x00\x00\x00\x00\x00\x00\x00\x10",
    b"\x00\x00\x00\x00\x00\x00\x00\x80",
    b"\x00\x00\x00\x00\x00\x00\x00\xFF",
    b"\x00\x00\x00\x00\x00\x00\x01\x00",
    b"\x00\x00\x00\x00\x00\x00\x10\x00",
    b"\x00\x00\x00\x00\x00\x00\x80\x00",
    b"\x00\x00\x00\x00\x00\x00\xFF\x00",
    b"\x00\x00\x00\x00\x00\x01\x00\x00",
    b"\x00\x00\x00\x00\x00\x10\x00\x00",
    b"\x00\x00\x00\x00\x00\x80\x00\x00",
    b"\x00\x00\x00\x00\x00\xFF\x00\x00",
    b"\x00\x00\x00\x00\x01\x00\x00\x00",
    b"\x00\x00\x00\x00\x10\x00\x00\x00",
    b"\x00\x00\x00\x00\x80\x00\x00\x00",
    b"\x00\x00\x00\x00\xFF\x00\x00\x00",
    b"\x00\x00\x00\x00\x00\x00\x00\x00",
    b"\x00\x00\x00\x01\x00\x00\x00\x00",
    b"\x00\x00\x00\x10\x00\x00\x00\x00",
    b"\x00\x00\x00\x80\x00\x00\x00\x00",
    b"\x00\x00\x00\xFF\x00\x00\x00\x00",
    b"\x00\x00\x01\x00\x00\x00\x00\x00",
    b"\x00\x00\x10\x00\x00\x00\x00\x00",
    b"\x00\x00\x80\x00\x00\x00\x00\x00",
    b"\x00\x00\xFF\x00\x00\x00\x00\x00",
    b"\x00\x01\x00\x00\x00\x00\x00\x00",
    b"\x00\x10\x00\x00\x00\x00\x00\x00",
    b"\x00\x80\x00\x00\x00\x00\x00\x00",
    b"\x00\xFF\x00\x00\x00\x00\x00\x00",
    b"\x01\x00\x00\x00\x00\x00\x00\x00",
    b"\x10\x00\x00\x00\x00\x00\x00\x00",
    b"\x80\x00\x00\x00\x00\x00\x00\x00",
    b"\xFF\x00\x00\x00\x00\x00\x00\x00",
]
TEST_VALUES_64_BIT_UINT_LE = [
    pytest.param(
        v,
        struct.unpack("<Q", v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_64_BIT
]
TEST_VALUES_64_BIT_UINT_BE = [
    pytest.param(
        v,
        struct.unpack(">Q", v)[0],
        get_bitarray(v),
    )
    for v in TEST_VALUES_64_BIT
]


class TestUInt08:
    def test_uint8_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:02X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt8Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint8_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:02X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt8Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_08_BIT_UINT_BE,
    )
    def test_uint8_create_parse_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:02X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt8Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_08_BIT_UINT_LE,
    )
    def test_uint8_create_parse_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:02X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt8Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint8_create_parse_short_big_endian(self) -> None:
        byte_data = b"\x00"
        bits_data_full = bitarray(endian="little")
        bits_data_full.frombytes(byte_data)
        bits_data = bits_data_full[-3:]
        name = "test"
        endian: Literal["big", "little"] = "big"
        with pytest.raises(IndexError):
            UInt8Field(
                name=name,
                data=bits_data,
                endian=endian,
            )

    def test_uint8_create_parse_short_little_endian(self) -> None:
        name = "test"
        byte_data = b"\x00"
        bits_data_full = bitarray(endian="little")
        bits_data_full.frombytes(byte_data)
        bits_data = bits_data_full[-3:]
        endian: Literal["little", "big"] = "little"
        with pytest.raises(IndexError):
            UInt8Field(
                name=name,
                data=bits_data,
                endian=endian,
            )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_08_BIT_UINT_BE,
    )
    def test_uint8_create_init_value_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:02X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = UInt8Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_08_BIT_UINT_LE,
    )
    def test_uint8_create_init_value_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:02X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = UInt8Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint8_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt8Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint8_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100
        obj = UInt8Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt16:
    def test_uint16_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">H", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:04X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint16_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<H", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:04X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_16_BIT_UINT_BE,
    )
    def test_uint16_create_parse_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:04X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_16_BIT_UINT_LE,
    )
    def test_uint16_create_parse_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:04X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_16_BIT_UINT_LE,
    )
    def test_uint16_create_init_value_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:04X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_16_BIT_UINT_BE,
    )
    def test_uint16_create_init_value_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:04X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt16Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint16_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint16_assign_invalid_value(self) -> None:
        name = "test"
        value = 0x10000
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt24:
    def test_uint24_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">I", value)[1:]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:06X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint24_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<I", value)[:-1]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:06X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_24_BIT_UINT_BE,
    )
    def test_uint24_create_parse_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:06X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_24_BIT_UINT_LE,
    )
    def test_uint24_create_parse_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:06X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_24_BIT_UINT_BE,
    )
    def test_uint24_create_init_value_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:06X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_24_BIT_UINT_LE,
    )
    def test_uint24_create_init_value_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:06X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt24Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint24_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint24_assign_invalid_value(self) -> None:
        name = "test"
        value = 0x1000000
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt32:
    def test_uint32_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">I", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:08X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint32_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<I", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:08X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_UINT_BE,
    )
    def test_uint32_create_parse_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:08X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_UINT_LE,
    )
    def test_uint32_create_parse_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:08X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_UINT_BE,
    )
    def test_uint32_create_init_value_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:08X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_32_BIT_UINT_LE,
    )
    def test_uint32_create_init_value_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:08X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt32Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint32_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt32Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint32_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100000000
        obj = UInt32Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt64:
    def test_uint64_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">Q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:016X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint64_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<Q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{:016X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_64_BIT_UINT_BE,
    )
    def test_uint64_create_parse_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:016X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_64_BIT_UINT_LE,
    )
    def test_uint64_create_parse_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:016X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_64_BIT_UINT_BE,
    )
    def test_uint64_create_init_value_big_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:016X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data"],
        TEST_VALUES_64_BIT_UINT_LE,
    )
    def test_uint64_create_init_value_little_endian(self, byte_data: bytes, value: int, bits_data: bitarray) -> None:
        tst = TestData(
            name="test",
            value=value,
            format="{:016X}(hex)",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = UInt64Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        parseobject_tests(
            obj=obj,
            tst=tst,
        )

    def test_uint64_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt64Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint64_set_value_invalid_value(self) -> None:
        name = "test"
        value = -900000000001
        obj = UInt64Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value
