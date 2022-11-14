from collections import OrderedDict
from typing import Any
import pytest
from easyprotocol.fields.signed_int import Int8Field, Int16Field, Int32Field, Int64Field, Int24Field
from bitarray import bitarray
from test_parse_object import parseobject_tests
from easyprotocol.base.parse_object import ParseObject


class TestInt08:
    def test_int8_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_count = 1
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int8Field(name=name)
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

    def test_int8_create_parse_bytes(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 1
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        data = bitarray()
        data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int8Field(name=name, data=byte_data)
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

    def test_int8_create_parse_bits(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 1
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int8Field(name=name, data=bits_data)
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

    def test_int8_create_parse_bits_short(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 1
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data1 = bitarray("001")
        bits_data2 = bitarray()
        bits_data2.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int8Field(name=name, data=bits_data1)
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

    def test_int8_create_init_value(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 1
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int8Field(name=name, value=value)
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

    def test_int8_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int8Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int8_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x100
        obj = Int8Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt16:
    def test_int16_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_count = 2
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int16Field(name=name)
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

    def test_int16_create_parse(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 2
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int16Field(name=name, data=byte_data)
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

    def test_int16_create_init_value(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 2
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int16Field(name=name, value=value)
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

    def test_int16_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int16Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int16_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x10000
        obj = Int16Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value


class TestInt24:
    def test_int24_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_count = 3
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int24Field(name=name)
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

    def test_int24_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int24Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int24_set_value_invalid_value(self) -> None:
        name = "test"
        value = 0x1000000
        obj = Int24Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt32:
    def test_int32_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_count = 4
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int32Field(name=name)
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

    def test_int32_create_parse(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 4
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int32Field(name=name, data=byte_data)
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

    def test_int32_create_init_value(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 4
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int32Field(name=name, value=value)
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

    def test_int32_set_value_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        obj = Int32Field(name=name)
        with pytest.raises(TypeError):
            obj.value = value  # type:ignore

    def test_int32_set_value_invalid_value(self) -> None:
        name = "test"
        value = 900000000001
        obj = Int32Field(name=name)
        with pytest.raises(OverflowError):
            obj.value = value


class TestUInt64:
    def test_int64_create_empty(self) -> None:
        name = "test"
        value = 0
        format = "{}"
        byte_count = 8
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int64Field(name=name)
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

    def test_int64_create_parse(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_count = 8
        byte_data = int.to_bytes(value, length=byte_count, byteorder="big", signed=True)
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int64Field(name=name, data=byte_data)
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

    def test_int64_create_init_value(self) -> None:
        name = "test"
        value = 1
        format = "{}"
        byte_data = b"\x00\x00\x00\x00\x00\x00\x00\x01"
        bits_data = bitarray()
        bits_data.frombytes(byte_data)
        parent = None
        children: OrderedDict[str, ParseObject[Any]] = OrderedDict()
        obj = Int64Field(name=name, value=value)
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
