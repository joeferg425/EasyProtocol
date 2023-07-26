# flake8:noqa
import struct

import pytest
from bitarray import bitarray
from parse_data import (
    PARAMETER_NAMES,
    TEST_VALUES_08_BIT_UINT_BE,
    TEST_VALUES_08_BIT_UINT_LE,
    TEST_VALUES_16_BIT_UINT_BE,
    TEST_VALUES_16_BIT_UINT_LE,
    TEST_VALUES_24_BIT_UINT_BE,
    TEST_VALUES_24_BIT_UINT_LE,
    TEST_VALUES_32_BIT_UINT_BE,
    TEST_VALUES_32_BIT_UINT_LE,
    TEST_VALUES_64_BIT_UINT_BE,
    TEST_VALUES_64_BIT_UINT_LE,
    TEST_VALUES_N_BIT_UINT_BE_VARIABLE,
    TEST_VALUES_N_BIT_UINT_LE_VARIABLE,
    ParseData,
)

from easyprotocol.base.base_field import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.base_value_field import BaseValueField
from easyprotocol.fields.unsigned_int import (
    UINT08_STRING_FORMAT,
    UINT16_STRING_FORMAT,
    UINT24_STRING_FORMAT,
    UINT32_STRING_FORMAT,
    UINT64_STRING_FORMAT,
    UINT_STRING_FORMAT,
    UInt8Field,
    UInt16Field,
    UInt24Field,
    UInt32Field,
    UInt64Field,
    UIntField,
)


def check_int_properties(
    obj: BaseValueField[int],
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
        obj._parent == tst.parent  # pyright:ignore[reportPrivateUsage]
    ), f"{obj}: obj.parent is not the expected value ({obj._parent} != expected value: {tst.parent})"  # pyright:ignore[reportPrivateUsage]
    assert (
        obj.byte_value == tst.byte_data
    ), f"{obj}: bytes(obj) is not the expected value ({bytes(obj)!r} != expected value: {tst.byte_data!r})"
    assert (
        obj.endian == tst.endian
    ), f"{obj}: obj.endian is not the expected value ({obj.endian} != expected value: {tst.endian})"


def check_int_children(
    obj: BaseValueField[int],
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


def check_int_value(
    obj: BaseValueField[int],
    tst: ParseData,
) -> None:
    assert (
        obj.value == tst.value
    ), f"{obj}: obj.value is not the expected value ({obj.value} != expected value: {tst.value})"


def check_int_strings(
    obj: BaseValueField[int],
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


def check_int(
    obj: BaseValueField[int],
    tst: ParseData,
) -> None:
    check_int_value(
        obj=obj,
        tst=tst,
    )
    check_int_properties(
        obj=obj,
        tst=tst,
    )
    check_int_children(
        obj=obj,
        tst=tst,
    )
    check_int_strings(
        obj=obj,
        tst=tst,
    )


class TestUIntField:
    def test_uintfield_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uintfield_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uintfield_set_name(self) -> None:
        value = 0
        byte_data = struct.pack("B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        tst.name = "new_name"
        obj.name = tst.name
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uintfield_set_value(self) -> None:
        value1 = 0
        byte_data1 = struct.pack("B", value1)
        bits_data1 = bitarray(endian="big")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        byte_data2 = struct.pack("B", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
            name="test",
            value=value1,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian="big",
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        obj.value = value2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uintfield_set_bits(self) -> None:
        value1 = 0
        byte_data1 = struct.pack("B", value1)
        bits_data1 = bitarray(endian="big")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        byte_data2 = struct.pack("b", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
            name="test",
            value=value1,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian="big",
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        obj.bits_lsb = bits_data2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uintfield_set_parent(self) -> None:
        value = 0
        byte_data = struct.pack("B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )
        tst.parent = UInt8Field(name="parent")
        obj._parent = tst.parent  # pyright:ignore[reportPrivateUsage]
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_N_BIT_UINT_BE_VARIABLE,
    )
    def test_uintfield_create_parse_n_bit_big_endian(
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
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=bit_count,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_N_BIT_UINT_LE_VARIABLE,
    )
    def test_uintfield_create_parse_n_bit_little_endian(
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
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=bit_count,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_N_BIT_UINT_BE_VARIABLE,
    )
    def test_uintfield_create_init_value_big_endian(
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
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=bit_count,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_N_BIT_UINT_LE_VARIABLE,
    )
    def test_uintfield_create_init_value_little_endian(
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
            string_format=UINT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UIntField(
            name=tst.name,
            bit_count=bit_count,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )


class TestUInt08:
    def test_uint8field_create_empty_big_endian(self) -> None:
        endian: endianT = "big"
        value = 0
        byte_data = struct.pack(">B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT08_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt8Field(
            name=tst.name,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint8field_create_empty_little_endian(self) -> None:
        endian: endianT = "little"
        value = 0
        byte_data = struct.pack("<B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT08_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt8Field(
            name=tst.name,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_UINT_BE,
    )
    def test_uint8field_create_parse_big_endian(
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
            string_format=UINT08_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt8Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_UINT_LE,
    )
    def test_uint8field_create_parse_little_endian(
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
            string_format=UINT08_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt8Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_UINT_BE,
    )
    def test_uint8field_create_init_value_big_endian(
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
            string_format=UINT08_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = UInt8Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_08_BIT_UINT_LE,
    )
    def test_uint8field_create_init_value_little_endian(
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
            string_format=UINT08_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            children=dict(),
            endian=endian,
        )
        obj = UInt8Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint8field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFF
        value2 = 0xFF
        byte_data1 = struct.pack("H", value1)
        byte_data2 = struct.pack("B", value2)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = UInt8Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_uint8field_create_parse_too_little_data(self) -> None:
        value = 0x0F
        byte_data = struct.pack("B", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = UInt8Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_uint8field_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt8Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint8field_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100
        obj = UInt8Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt16:
    def test_uint16field_create_empty_big_endian(self) -> None:
        endian: endianT = "big"
        value = 0
        byte_data = struct.pack(">H", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt16Field(
            name=tst.name,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint16field_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<H", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=dict(),
        )
        obj = UInt16Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_16_BIT_UINT_BE,
    )
    def test_uint16field_create_parse_big_endian(
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
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt16Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_16_BIT_UINT_LE,
    )
    def test_uint16field_create_parse_little_endian(
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
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt16Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_16_BIT_UINT_LE,
    )
    def test_uint16field_create_init_value_little_endian(
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
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt16Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_16_BIT_UINT_BE,
    )
    def test_uint16field_create_init_value_big_endian(
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
            string_format=UINT16_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt16Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint16field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFF
        value2 = 0xFFFF
        byte_data1 = struct.pack("I", value1)
        byte_data2 = struct.pack("H", value2)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = UInt16Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_uint16field_create_parse_too_little_data(self) -> None:
        value = 0x0FFF
        byte_data = struct.pack("H", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = UInt16Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_uint16field_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint16field_assign_invalid_value(self) -> None:
        name = "test"
        value = 0x10000
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt24:
    def test_uint24field_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">I", value)[1:]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=dict(),
        )
        obj = UInt24Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint24field_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<I", value)[:-1]
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=dict(),
        )
        obj = UInt24Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_24_BIT_UINT_BE,
    )
    def test_uint24field_create_parse_big_endian(
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
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt24Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_24_BIT_UINT_LE,
    )
    def test_uint24field_create_parse_little_endian(
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
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt24Field(
            name=tst.name,
            data=byte_data,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_24_BIT_UINT_BE,
    )
    def test_uint24field_create_init_value_big_endian(
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
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt24Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_24_BIT_UINT_LE,
    )
    def test_uint24field_create_init_value_little_endian(
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
            string_format=UINT24_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt24Field(
            name=tst.name,
            default=value,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint24field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFF
        value2 = 0xFFFFFFFF
        value3 = 0xFF
        byte_data1 = struct.pack("I", value1)
        byte_data2 = struct.pack("I", value2)[:-1]
        byte_data3 = struct.pack("B", value3)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        bits_data3 = bitarray(endian="little")
        bits_data3.frombytes(byte_data3)
        extra = bitarray(bits_data3)
        name = "test"
        obj = UInt24Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_uint24field_create_parse_too_little_data(self) -> None:
        value = 0x0FFFFF
        byte_data = struct.pack("I", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-9]
        name = "test"
        obj = UInt24Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_uint24field_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint24field_assign_invalid_value(self) -> None:
        name = "test"
        value = 0x1000000
        obj = UInt16Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt32:
    def test_uint32field_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">I", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=dict(),
        )
        obj = UInt32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint32field_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<I", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=dict(),
        )
        obj = UInt32Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_UINT_BE,
    )
    def test_uint32field_create_parse_big_endian(
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
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt32Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_UINT_LE,
    )
    def test_uint32field_create_parse_little_endian(
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
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt32Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_UINT_BE,
    )
    def test_uint32field_create_init_value_big_endian(
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
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt32Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_32_BIT_UINT_LE,
    )
    def test_uint32field_create_init_value_little_endian(
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
            string_format=UINT32_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt32Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint32field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFFFFFFFFFF
        value2 = 0xFFFFFFFF
        byte_data1 = struct.pack("Q", value1)
        byte_data2 = struct.pack("I", value2)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = UInt32Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_uint32field_create_parse_too_little_data(self) -> None:
        value = 0x0FFFFFFF
        byte_data = struct.pack("I", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = UInt32Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_uint32field_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt32Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint32field_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100000000
        obj = UInt32Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt64:
    def test_uint64field_create_empty_big_endian(self) -> None:
        value = 0
        byte_data = struct.pack(">Q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="big",
            children=dict(),
        )
        obj = UInt64Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint64field_create_empty_little_endian(self) -> None:
        value = 0
        byte_data = struct.pack("<Q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian="little",
            children=dict(),
        )
        obj = UInt64Field(
            name=tst.name,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_64_BIT_UINT_BE,
    )
    def test_uint64field_create_parse_big_endian(
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
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt64Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_64_BIT_UINT_LE,
    )
    def test_uint64field_create_parse_little_endian(
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
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt64Field(
            name=tst.name,
            data=byte_data,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_64_BIT_UINT_BE,
    )
    def test_uint64field_create_init_value_big_endian(
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
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt64Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    @pytest.mark.parametrize(
        PARAMETER_NAMES,
        TEST_VALUES_64_BIT_UINT_LE,
    )
    def test_uint64field_create_init_value_little_endian(
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
            string_format=UINT64_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=dict(),
        )
        obj = UInt64Field(
            name=tst.name,
            default=value,
            endian=endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_uint64field_create_parse_too_much_data(self) -> None:
        value1 = 0xFFFFFFFFFFFFFFFF
        value2 = 0xFFFFFFFF
        byte_data1 = struct.pack("Q", value1) + struct.pack("Q", value1)
        byte_data2 = struct.pack("I", value2) + struct.pack("I", value2)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        bits_data2 = bitarray(endian="little")
        bits_data2.frombytes(byte_data2)
        extra = bitarray(bits_data2)
        name = "test"
        obj = UInt64Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        remainder = obj.parse(bits_data1)
        assert remainder == extra
        assert obj.bits == bits_data2
        assert obj.byte_value == byte_data2

    def test_uint64field_create_parse_too_little_data(self) -> None:
        value = 0x0FFFFFFFFFFFFFFF
        byte_data = struct.pack("Q", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        bits_data = bits_data[:-1]
        name = "test"
        obj = UInt64Field(
            name=name,
            endian=DEFAULT_ENDIANNESS,
        )
        with pytest.raises(IndexError):
            obj.parse(bits_data)

    def test_uint64field_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt64Field(
            name=name,
        )
        with pytest.raises(ValueError):
            obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

    def test_uint64field_set_value_invalid_value(self) -> None:
        name = "test"
        value = -900000000001
        obj = UInt64Field(
            name=name,
        )
        with pytest.raises(OverflowError):
            obj.value = value
