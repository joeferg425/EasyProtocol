from collections import OrderedDict
import struct
from typing import Any, Literal
import pytest
from easyprotocol.fields.signed_int import Int8Field, Int16Field, Int32Field, Int64Field, Int24Field
from bitarray import bitarray
from test_parse_object import parseobject_tests
from easyprotocol.base.parse_object import ParseObject


class TestInt08:
    def test_int8_create_empty_big_endian(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack(">b", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int8Field(
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

    def test_int8_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack("<b", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int8Field(
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
    def test_int8_create_parse_bytes_big_endian(self, value: int) -> None:
        name = "test"
        format = "{}"
        byte_data = struct.pack(">B", value)
        value = struct.unpack(">b", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        data = bitarray()
        data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int8Field(
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
    def test_int8_create_parse_bytes_little_endian(self, value: int) -> None:
        name = "test"
        format = "{}"
        byte_data = struct.pack("<B", value)
        value = struct.unpack("<b", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        data = bitarray()
        data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int8Field(
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
    def test_int8_create_parse_bits_big_endian(self, value: int) -> None:
        name = "test"
        format = "{}"
        byte_data = struct.pack(">B", value)
        value = struct.unpack(">b", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int8Field(
            name=name,
            data=bits_data,
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
    def test_int8_create_parse_bits_little_endian(self, value: int) -> None:
        name = "test"
        format = "{}"
        byte_data = struct.pack("<B", value)
        value = struct.unpack("<b", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int8Field(
            name=name,
            data=bits_data,
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
    def test_int8_create_parse_bits_short_big_endian(self, value: int) -> None:
        name = "test"
        format = "{}"
        byte_data = struct.pack(">B", value)
        value = struct.unpack(">b", byte_data)[0]
        bits_data2 = bitarray()
        bits_data2.frombytes(byte_data)
        bits_data1 = bits_data2[-3:]
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int8Field(
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
    def test_int8_create_parse_bits_short_little_endian(self, value: int) -> None:
        name = "test"
        format = "{}"
        byte_data = struct.pack("<B", value)
        value = struct.unpack("<b", byte_data)[0]
        bits_data2 = bitarray()
        bits_data2.frombytes(byte_data)
        bits_data1 = bits_data2[-3:]
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int8Field(
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
    def test_int8_create_init_value_big_endian(self, value: int) -> None:
        name = "test"
        format = "{}"
        byte_data = struct.pack(">B", value)
        value = struct.unpack(">b", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int8Field(
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
    def test_int8_create_init_value_little_endian(self, value: int) -> None:
        name = "test"
        format = "{}"
        byte_data = struct.pack("<B", value)
        value = struct.unpack("<b", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int8Field(
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
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack(">h", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int16Field(
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

    def test_int16_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack("<h", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int16Field(
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

    def test_int16_create_parse_big_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack(">h", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int16Field(
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

    def test_int16_create_parse_little_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack("<h", value)
        check_int = struct.unpack(">h", byte_data)[0]
        check_data = struct.pack(">h", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int16Field(
            name=name,
            data=byte_data,
            endian=endian,
        )
        parseobject_tests(
            obj=obj,
            name=name,
            value=check_int,
            format=format,
            bits_data=bits_data,
            byte_data=check_data,
            parent=parent,
            children=children,
            endian=endian,
        )

    def test_int16_create_init_value_big_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack(">h", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int16Field(
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

    def test_int16_create_init_value_little_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack("<h", value)
        check_data = struct.pack(">h", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int16Field(
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
            byte_data=check_data,
            parent=parent,
            children=children,
            endian=endian,
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
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack(">i", value)[1:]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int24Field(
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

    def test_int24_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack("<i", value)[:-1]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int24Field(
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

    def test_int24_create_parse_big_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack(">i", value)[1:]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int24Field(
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

    def test_int24_create_parse_little_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack("<i", value)
        check_data = struct.pack(">i", value)[1:]
        temp_int = int(struct.unpack(">i", byte_data)[0] / 256)
        byte_data = byte_data[:-1]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int24Field(
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

    def test_int24_create_init_value_big_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack(">i", value)[1:]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int24Field(
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

    def test_int24_create_init_value_little_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack("<i", value)[:-1]
        check_data = struct.pack(">i", value)[1:]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int24Field(
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
            byte_data=check_data,
            parent=parent,
            children=children,
            endian=endian,
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


class TestUInt32:
    def test_int32_create_empty_big_endian(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack(">i", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int32Field(
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

    def test_int32_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack("<i", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int32Field(
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

    def test_int32_create_parse_big_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack(">i", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int32Field(
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

    def test_int32_create_parse_little_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack("<i", value)
        check_data = struct.pack(">i", value)
        temp_int = struct.unpack(">i", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int32Field(
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

    def test_int32_create_init_value_big_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack(">i", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int32Field(
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

    def test_int32_create_init_value_little_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack("<i", value)
        check_data = struct.pack(">i", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int32Field(
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
            byte_data=check_data,
            parent=parent,
            children=children,
            endian=endian,
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


class TestUInt64:
    def test_int64_create_empty_big_endian(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack(">q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int64Field(
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

    def test_int64_create_empty_little_endian(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_data = struct.pack("<q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int64Field(
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

    def test_int64_create_parse_big_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack(">q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int64Field(
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

    def test_int64_create_parse_little_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack("<q", value)
        check_data = struct.pack(">q", value)
        temp_int = struct.unpack(">q", byte_data)[0]
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int64Field(
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

    def test_int64_create_init_value_big_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack(">q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "big"
        obj = Int64Field(
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

    def test_int64_create_init_value_little_endian(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = struct.pack("<q", value)
        check_data = struct.pack(">q", value)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        endian: Literal["little", "big"] = "little"
        obj = Int64Field(
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
            byte_data=check_data,
            parent=parent,
            children=children,
            endian=endian,
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
