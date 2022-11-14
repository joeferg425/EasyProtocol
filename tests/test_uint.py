from collections import OrderedDict
from typing import Any
import pytest
from easyprotocol.fields.unsigned_int import UInt8Field, UInt16Field, UInt32Field, UInt64Field, UInt24Field
from easyprotocol.parse_object import ParseObject
from bitarray import bitarray
from test_parse_object import parseobject_tests


class TestUInt08:
    def test_uint8_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{:02X}"
        byte_count = 1
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint8_create_parse(self) -> None:
        name = "test"
        value = 1
        format = "{:02X}"
        byte_count = 1
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(name=name, data=byte_data)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint8_create_parse_short(self) -> None:
        name = "test"
        value = 1
        format = "{:02X}"
        byte_count = 1
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data1 = bitarray("001")
        bits_data2 = bitarray()
        bits_data2.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt8Field(name=name, data=bits_data1)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data2,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint8_create_init_value(self) -> None:
        name = "test"
        value = 1
        format = "{:02X}"
        byte_data = b"\x01"
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        obj = UInt8Field(name=name, value=value)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint8_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt8Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint8_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100
        obj = UInt8Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt16:
    def test_uint16_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{:04X}"
        byte_count = 2
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint16_create_parse(self) -> None:
        name = "test"
        value = 1
        format = "{:04X}"
        byte_count = 2
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(name=name, data=byte_data)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint16_create_init_value(self) -> None:
        name = "test"
        value = 1
        format = "{:04X}"
        byte_count = 2
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt16Field(name=name, value=value)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint16_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt16Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint16_assign_invalid_value(self) -> None:
        name = "test"
        value = 0x10000
        obj = UInt16Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt24:
    def test_uint24_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{:06X}"
        byte_count = 3
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt24Field(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint24_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt16Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint24_assign_invalid_value(self) -> None:
        name = "test"
        value = 0x1000000
        obj = UInt16Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt32:
    def test_uint32_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{:08X}"
        byte_count = 4
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint32_create_parse(self) -> None:
        name = "test"
        value = 1
        format = "{:08X}"
        byte_count = 4
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(name=name, data=byte_data)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint32_create_init_value(self) -> None:
        name = "test"
        value = 1
        format = "{:08X}"
        byte_count = 4
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt32Field(name=name, value=value)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint32_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt32Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint32_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100000000
        obj = UInt32Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt64:
    def test_uint64_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{:016X}"
        byte_count = 8
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(name=name)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint64_parse(self) -> None:
        name = "test"
        value = 1
        format = "{:016X}"
        byte_count = 8
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(name=name, data=bits_data)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint64_init_value(self) -> None:
        name = "test"
        value = 1
        format = "{:016X}"
        byte_count = 8
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = UInt64Field(name=name, value=value)
        parseobject_tests(
            obj=obj,
            name=name,
            value=value,
            format=format,
            bits_data=bits_data,
            byte_data=byte_data,
            parent=parent,
            children=children,
        )

    def test_uint64_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = UInt64Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_uint64_set_value_invalid_value(self) -> None:
        name = "test"
        value = -900000000001
        obj = UInt64Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value
