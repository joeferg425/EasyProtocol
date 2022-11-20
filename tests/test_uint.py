from collections import OrderedDict
from typing import Any, Literal
import pytest
from easyprotocol.fields.unsigned_int import UInt8Field, UInt16Field, UInt32Field, UInt64Field, UInt24Field
from easyprotocol.base.parse_object import ParseObject
from bitarray import bitarray
from test_parse_object import parseobject_tests
import struct


class TestUInt08:
    def test_uint8_create_empty_big_endian(self) -> None:
        name = "test"
        value = 0
        format = "{:02X}(hex)"
        byte_data = struct.pack(">B", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    def test_uint8_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{:02X}(hex)"
        byte_data = struct.pack("<B", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00,
            0x01,
            0x10,
            0x80,
            0xFF,
        ],
    )
    def test_uint8_create_parse_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:02X}(hex)"
        byte_data = struct.pack(">B", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00,
            0x01,
            0x10,
            0x80,
            0xFF,
        ],
    )
    def test_uint8_create_parse_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:02X}(hex)"
        byte_data = struct.pack("<B", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00,
            0x01,
            0x2,
            0x03,
        ],
    )
    def test_uint8_create_parse_short_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:02X}(hex)"
        byte_data = struct.pack(">B", value)
        bits_data2 = bitarray()
        bits_data2.frombytes(byte_data)
        bits_data1 = bits_data2[-3:]
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(
            name=name,
            data=bits_data1,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data2,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00,
            0x01,
            0x2,
            0x03,
        ],
    )
    def test_uint8_create_parse_short_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:02X}(hex)"
        byte_data = struct.pack("<B", value)
        bits_data2 = bitarray()
        bits_data2.frombytes(byte_data)
        bits_data1 = bits_data2[-3:]
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(
            name=name,
            data=bits_data1,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data2,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00,
            0x01,
            0x10,
            0x80,
            0xFF,
        ],
    )
    def test_uint8_create_init_value_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:02X}(hex)"
        byte_data = struct.pack(">B", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = UInt8Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00,
            0x01,
            0x10,
            0x80,
            0xFF,
        ],
    )
    def test_uint8_create_init_value_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:02X}(hex)"
        byte_data = struct.pack("<B", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = UInt8Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
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
        name = "test"
        value = 0
        format = "{:04X}(hex)"
        byte_data = struct.pack(">H", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    def test_uint16_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{:04X}(hex)"
        byte_data = struct.pack("<H", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x0000,
            0x0001,
            0x0010,
            0x0080,
            0x00FF,
            0x0100,
            0x0800,
            0x1000,
            0x8000,
            0xFF00,
        ],
    )
    def test_uint16_create_parse_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:04X}(hex)"
        byte_data = struct.pack(">H", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x0000,
            0x0001,
            0x0010,
            0x0080,
            0x00FF,
            0x0100,
            0x0800,
            0x1000,
            0x8000,
            0xFF00,
        ],
    )
    def test_uint16_create_parse_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:04X}(hex)"
        byte_data = struct.pack("<H", value)
        check_int = struct.unpack(">H", byte_data)[0]
        check_bytes = struct.pack(">H", value)
        check_bits = bitarray()
        check_bits.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=check_int,
            format=format,
            bits_data=check_bits,
            byte_data=check_bytes,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x0000,
            0x0001,
            0x0010,
            0x0080,
            0x00FF,
            0x0100,
            0x0800,
            0x1000,
            0x8000,
            0xFF00,
        ],
    )
    def test_uint16_create_init_value_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:04X}(hex)"
        byte_data = struct.pack("<H", value)
        check_data = struct.pack(">H", value)
        bits_data = bitarray()
        bits_data.frombytes(check_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x0000,
            0x0001,
            0x0010,
            0x0080,
            0x00FF,
            0x0100,
            0x0800,
            0x1000,
            0x8000,
            0xFF00,
        ],
    )
    def test_uint16_create_init_value_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:04X}(hex)"
        byte_data = struct.pack(">H", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
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
        name = "test"
        value = 0
        format = "{:06X}(hex)"
        byte_data = struct.pack(">I", value)[1:]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt24Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    def test_uint24_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{:06X}(hex)"
        byte_data = struct.pack("<I", value)[:-1]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt24Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x000000,
            0x000001,
            0x000010,
            0x000080,
            0x0000FF,
            0x000100,
            0x001000,
            0x008000,
            0x00FF00,
            0x010000,
            0x100000,
            0x800000,
            0xFF0000,
        ],
    )
    def test_uint24_create_parse_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:06X}(hex)"
        byte_data = struct.pack(">I", value)[1:]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt24Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x000000,
            0x000001,
            0x000010,
            0x000080,
            0x0000FF,
            0x000100,
            0x001000,
            0x008000,
            0x00FF00,
            0x010000,
            0x100000,
            0x800000,
            0xFF0000,
        ],
    )
    def test_uint24_create_parse_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:06X}(hex)"
        byte_data = struct.pack("<I", value)
        check_data = struct.pack(">I", value)[1:]
        temp_int = int(struct.unpack(">I", byte_data)[0] / 256)
        byte_data = byte_data[:-1]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt24Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=temp_int,
            format=format,
            bits_data=bits_data,
            byte_data=check_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x000000,
            0x000001,
            0x000010,
            0x000080,
            0x0000FF,
            0x000100,
            0x001000,
            0x008000,
            0x00FF00,
            0x010000,
            0x100000,
            0x800000,
            0xFF0000,
        ],
    )
    def test_uint24_create_init_value_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:06X}(hex)"
        byte_data = struct.pack(">I", value)[1:]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt24Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x000000,
            0x000001,
            0x000010,
            0x000080,
            0x0000FF,
            0x000100,
            0x001000,
            0x008000,
            0x00FF00,
            0x010000,
            0x100000,
            0x800000,
            0xFF0000,
        ],
    )
    def test_uint24_create_init_value_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:06X}(hex)"
        byte_data = struct.pack("<I", value)[:-1]
        check_data = struct.pack(">I", value)[1:]
        bits_data = bitarray()
        bits_data.frombytes(check_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt24Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
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
        name = "test"
        value = 0
        format = "{:08X}(hex)"
        byte_data = struct.pack(">I", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    def test_uint32_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{:08X}(hex)"
        byte_data = struct.pack("<I", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00000000,
            0x00000001,
            0x00000010,
            0x00000080,
            0x000000FF,
            0x00000100,
            0x00001000,
            0x00008000,
            0x0000FF00,
            0x00010000,
            0x00100000,
            0x00800000,
            0x00FF0000,
            0x01000000,
            0x10000000,
            0x80000000,
            0xFF000000,
        ],
    )
    def test_uint32_create_parse_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:08X}(hex)"
        byte_data = struct.pack(">I", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00000000,
            0x00000001,
            0x00000010,
            0x00000080,
            0x000000FF,
            0x00000100,
            0x00001000,
            0x00008000,
            0x0000FF00,
            0x00010000,
            0x00100000,
            0x00800000,
            0x00FF0000,
            0x01000000,
            0x10000000,
            0x80000000,
            0xFF000000,
        ],
    )
    def test_uint32_create_parse_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:08X}(hex)"
        byte_data = struct.pack("<I", value)
        check_data = struct.pack(">I", value)
        temp_int = struct.unpack(">I", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=temp_int,
            format=format,
            bits_data=bits_data,
            byte_data=check_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00000000,
            0x00000001,
            0x00000010,
            0x00000080,
            0x000000FF,
            0x00000100,
            0x00001000,
            0x00008000,
            0x0000FF00,
            0x00010000,
            0x00100000,
            0x00800000,
            0x00FF0000,
            0x01000000,
            0x10000000,
            0x80000000,
            0xFF000000,
        ],
    )
    def test_uint32_create_init_value_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:08X}(hex)"
        byte_data = struct.pack(">I", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x00000000,
            0x00000001,
            0x00000010,
            0x00000080,
            0x000000FF,
            0x00000100,
            0x00001000,
            0x00008000,
            0x0000FF00,
            0x00010000,
            0x00100000,
            0x00800000,
            0x00FF0000,
            0x01000000,
            0x10000000,
            0x80000000,
            0xFF000000,
        ],
    )
    def test_uint32_create_init_value_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:08X}(hex)"
        byte_data = struct.pack("<I", value)
        check_data = struct.pack(">I", value)
        bits_data = bitarray()
        bits_data.frombytes(check_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
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
        name = "test"
        value = 0
        format = "{:016X}(hex)"
        byte_data = struct.pack(">Q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    def test_uint64_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{:016X}(hex)"
        byte_data = struct.pack("<Q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(
            name=name,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x0000000000000000,
            0x0000000000000001,
            0x0000000000000010,
            0x0000000000000080,
            0x00000000000000FF,
            0x0000000000000100,
            0x0000000000001000,
            0x0000000000008000,
            0x000000000000FF00,
            0x0000000000010000,
            0x0000000000100000,
            0x0000000000800000,
            0x0000000000FF0000,
            0x0000000001000000,
            0x0000000010000000,
            0x0000000080000000,
            0x00000000FF000000,
            0x0000000000000000,
            0x0000000100000000,
            0x0000001000000000,
            0x0000008000000000,
            0x000000FF00000000,
            0x0000010000000000,
            0x0000100000000000,
            0x0000800000000000,
            0x0000FF0000000000,
            0x0001000000000000,
            0x0010000000000000,
            0x0080000000000000,
            0x00FF000000000000,
            0x0100000000000000,
            0x1000000000000000,
            0x8000000000000000,
            0xFF00000000000000,
        ],
    )
    def test_uint64_create_parse_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:016X}(hex)"
        byte_data = struct.pack(">Q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x0000000000000000,
            0x0000000000000001,
            0x0000000000000010,
            0x0000000000000080,
            0x00000000000000FF,
            0x0000000000000100,
            0x0000000000001000,
            0x0000000000008000,
            0x000000000000FF00,
            0x0000000000010000,
            0x0000000000100000,
            0x0000000000800000,
            0x0000000000FF0000,
            0x0000000001000000,
            0x0000000010000000,
            0x0000000080000000,
            0x00000000FF000000,
            0x0000000000000000,
            0x0000000100000000,
            0x0000001000000000,
            0x0000008000000000,
            0x000000FF00000000,
            0x0000010000000000,
            0x0000100000000000,
            0x0000800000000000,
            0x0000FF0000000000,
            0x0001000000000000,
            0x0010000000000000,
            0x0080000000000000,
            0x00FF000000000000,
            0x0100000000000000,
            0x1000000000000000,
            0x8000000000000000,
            0xFF00000000000000,
        ],
    )
    def test_uint64_create_parse_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:016X}(hex)"
        byte_data = struct.pack("<Q", value)
        check_data = struct.pack(">Q", value)
        temp_int = struct.unpack(">Q", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=temp_int,
            format=format,
            bits_data=bits_data,
            byte_data=check_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x0000000000000000,
            0x0000000000000001,
            0x0000000000000010,
            0x0000000000000080,
            0x00000000000000FF,
            0x0000000000000100,
            0x0000000000001000,
            0x0000000000008000,
            0x000000000000FF00,
            0x0000000000010000,
            0x0000000000100000,
            0x0000000000800000,
            0x0000000000FF0000,
            0x0000000001000000,
            0x0000000010000000,
            0x0000000080000000,
            0x00000000FF000000,
            0x0000000000000000,
            0x0000000100000000,
            0x0000001000000000,
            0x0000008000000000,
            0x000000FF00000000,
            0x0000010000000000,
            0x0000100000000000,
            0x0000800000000000,
            0x0000FF0000000000,
            0x0001000000000000,
            0x0010000000000000,
            0x0080000000000000,
            0x00FF000000000000,
            0x0100000000000000,
            0x1000000000000000,
            0x8000000000000000,
            0xFF00000000000000,
        ],
    )
    def test_uint64_create_init_value_big_endian(self, value: int) -> None:
        name = "test"
        format = "{:016X}(hex)"
        byte_data = struct.pack(">Q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        endian: Literal["little", "big"] = "big"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    @pytest.mark.parametrize(
        "value",
        [
            0x0000000000000000,
            0x0000000000000001,
            0x0000000000000010,
            0x0000000000000080,
            0x00000000000000FF,
            0x0000000000000100,
            0x0000000000001000,
            0x0000000000008000,
            0x000000000000FF00,
            0x0000000000010000,
            0x0000000000100000,
            0x0000000000800000,
            0x0000000000FF0000,
            0x0000000001000000,
            0x0000000010000000,
            0x0000000080000000,
            0x00000000FF000000,
            0x0000000000000000,
            0x0000000100000000,
            0x0000001000000000,
            0x0000008000000000,
            0x000000FF00000000,
            0x0000010000000000,
            0x0000100000000000,
            0x0000800000000000,
            0x0000FF0000000000,
            0x0001000000000000,
            0x0010000000000000,
            0x0080000000000000,
            0x00FF000000000000,
            0x0100000000000000,
            0x1000000000000000,
            0x8000000000000000,
            0xFF00000000000000,
        ],
    )
    def test_uint64_create_init_value_little_endian(self, value: int) -> None:
        name = "test"
        format = "{:016X}(hex)"
        byte_data = struct.pack("<Q", value)
        check_data = struct.pack(">Q", value)
        bits_data = bitarray()
        bits_data.frombytes(check_data)
        parent = None
        endian: Literal["little", "big"] = "little"
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(
            name=name,
            value=value,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
            endian=endian,
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
