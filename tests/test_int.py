from collections import OrderedDict
import struct
from typing import Literal
import pytest
from easyprotocol.base.parse_object import ParseObject
from easyprotocol.fields.signed_int import Int8Field, Int16Field, Int32Field, Int64Field, Int24Field, IntField
from bitarray import bitarray
from test_parse_object import check_parseobject, TestData
from test_uint import (
    TEST_VALUES_08_BIT,
    TEST_VALUES_16_BIT,
    TEST_VALUES_24_BIT,
    TEST_VALUES_32_BIT,
    TEST_VALUES_64_BIT,
    get_bitarray,
)


TEST_VALUES_08_BIT_INT_LE = [
    pytest.param(
        v,
        struct.unpack("<b", v)[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_08_BIT
]
TEST_VALUES_08_BIT_INT_BE = [
    pytest.param(
        v,
        struct.unpack(">b", v)[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_08_BIT
]
TEST_VALUES_16_BIT_INT_LE = [
    pytest.param(
        v,
        struct.unpack("<h", v)[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_16_BIT
]
TEST_VALUES_16_BIT_INT_BE = [
    pytest.param(
        v,
        struct.unpack(">h", v)[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_16_BIT
]
TEST_VALUES_24_BIT_INT_LE = [
    pytest.param(
        v,
        struct.unpack("<i", v + (b"\xff" if v[2] & 0x80 else b"\x00"))[0],
        get_bitarray(v + (b"\xff" if v[2] & 0x80 else b"\x00")),
        "little",
    )
    for v in TEST_VALUES_24_BIT
]
TEST_VALUES_24_BIT_INT_BE = [
    pytest.param(
        v,
        struct.unpack(">i", (b"\xff" if v[0] & 0x80 else b"\x00") + v)[0],
        get_bitarray((b"\xff" if v[0] & 0x80 else b"\x00")),
        "big",
    )
    for v in TEST_VALUES_24_BIT
]
TEST_VALUES_32_BIT_INT_LE = [
    pytest.param(
        v,
        struct.unpack("<i", v)[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_32_BIT_INT_BE = [
    pytest.param(
        v,
        struct.unpack(">i", v)[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_32_BIT
]
TEST_VALUES_64_BIT_INT_LE = [
    pytest.param(
        v,
        struct.unpack("<q", v)[0],
        get_bitarray(v),
        "little",
    )
    for v in TEST_VALUES_64_BIT
]
TEST_VALUES_64_BIT_INT_BE = [
    pytest.param(
        v,
        struct.unpack(">q", v)[0],
        get_bitarray(v),
        "big",
    )
    for v in TEST_VALUES_64_BIT
]


class TestIntField:
    def test_intfield_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_intfield_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_name(self) -> None:
        value = 0
        byte_data = struct.pack("b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            value=tst.value,
        )
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

    def test_intfield_set_value(self) -> None:
        value1 = 0
        byte_data1 = struct.pack("b", value1)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        byte_data2 = struct.pack("b", value2)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        tst = TestData(
            name="test",
            value=value1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            value=tst.value,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

        obj.value = value2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_bits(self) -> None:
        value1 = 0
        byte_data1 = struct.pack("b", value1)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        byte_data2 = struct.pack("b", value2)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        tst = TestData(
            name="test",
            value=value1,
            format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            value=tst.value,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

        obj.bits = bits_data2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_parent(self) -> None:
        value = 0
        byte_data = struct.pack("b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            value=tst.value,
        )
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

    def test_intfield_set_children(self) -> None:
        child = ParseObject(name="child")
        value = 0
        byte_data = struct.pack("b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            value=tst.value,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )
        with pytest.raises(NotImplementedError):
            obj.children = OrderedDict({child.name: child})


class TestInt08:
    def test_int8_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=0,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int8Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int8_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            bits_data=bits_data,
            byte_data=byte_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int8Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_INT_BE,
    )
    def test_int8_create_parse_bytes_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        tst = TestData(
            name="test",
            format="{}",
            value=value,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int8Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_INT_LE,
    )
    def test_int8_create_parse_bytes_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        data = bitarray(endian="little")
        data.frombytes(byte_data)
        tst = TestData(
            name="test",
            format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int8Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_INT_BE,
    )
    def test_int8_create_parse_bits_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int8Field(
            name=tst.name,
            data=tst.bits_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_INT_LE,
    )
    def test_int8_create_parse_bits_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int8Field(
            name=tst.name,
            data=tst.bits_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int8_create_parse_bits_short(self) -> None:
        value1 = 0xFFFF
        value2 = 0xFF
        byte_data1 = struct.pack("H", value1)
        byte_data2 = struct.pack("B", value2)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        name = "test"
        obj = Int8Field(
            name=name,
            data=byte_data1,
        )

        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_INT_BE,
    )
    def test_int8_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int8Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_08_BIT_INT_LE,
    )
    def test_int8_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            format="{}",
            value=value,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int8Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int8_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int8Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int8_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100
        obj = Int8Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt16:
    def test_int16_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">h", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int16Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int16_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<h", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int16Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_16_BIT_INT_BE,
    )
    def test_int16_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int16Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_16_BIT_INT_LE,
    )
    def test_int16_create_parse_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int16Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_16_BIT_INT_BE,
    )
    def test_int16_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int16Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_16_BIT_INT_LE,
    )
    def test_int16_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int16Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int16_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int16Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int16_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x10000
        obj = Int16Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt24:
    def test_int24_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">i", value)[1:]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int24Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int24_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<i", value)[:-1]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int24Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_24_BIT_INT_BE,
    )
    def test_int24_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int24Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_24_BIT_INT_LE,
    )
    def test_int24_create_parse_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int24Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_24_BIT_INT_BE,
    )
    def test_int24_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int24Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_24_BIT_INT_LE,
    )
    def test_int24_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int24Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int24_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int24Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int24_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x1000000
        obj = Int24Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt32:
    def test_int32_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">i", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int32_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<i", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_INT_BE,
    )
    def test_int32_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int32Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_INT_LE,
    )
    def test_int32_create_parse_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int32Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_INT_BE,
    )
    def test_int32_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        value = 1
        byte_data = struct.pack(">i", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int32Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_32_BIT_INT_LE,
    )
    def test_int32_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int32Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int32_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int32Field(
            name=name,
        )
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int32_set_value_invalid_value(self) -> None:
        name = "test"
        value = 900000000001
        obj = Int32Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt64:
    def test_int64_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int64Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int64_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int64Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_64_BIT_INT_BE,
    )
    def test_int64_create_parse_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int64Field(
            name=tst.name,
            data=tst.byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_64_BIT_INT_LE,
    )
    def test_int64_create_parse_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int64Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_64_BIT_INT_BE,
    )
    def test_int64_create_init_value_big_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="big",
        )
        obj = Int64Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        ["byte_data", "value", "bits_data", "endian"],
        TEST_VALUES_64_BIT_INT_LE,
    )
    def test_int64_create_init_value_little_endian(
        self, byte_data: bytes, value: int, bits_data: bitarray, endian: Literal["big", "little"]
    ) -> None:
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = TestData(
            name="test",
            value=value,
            format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=OrderedDict(),
            endian="little",
        )
        obj = Int64Field(
            name=tst.name,
            value=tst.value,
            endian=tst.endian,
        )
        check_parseobject(
            obj=obj,
            tst=tst,
        )

    def test_int64_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int64Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int64_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x10000000000000000
        obj = Int64Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value
