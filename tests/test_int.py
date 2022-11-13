import pytest
from easyprotocol.fields import Int8, Int16, Int32, Int64
from bitarray import bitarray

from easyprotocol.fields.signed_int import Int24


class TestInt08:
    def test_int8_create_empty(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00")
        po = Int8(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int8.__name__ in repr(po)

    def test_int8_getters(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00")
        po = Int8(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int8.__name__ in repr(po)

    def test_int8_setter(self) -> None:
        name = "test"
        initial_value = 0
        initial_data = bitarray()
        initial_data.frombytes(b"\x00")
        value = 1
        data = bitarray()
        data.frombytes(b"\x01")
        po = Int8(name=name)
        assert po.value == initial_value
        assert po.bits == initial_data
        po.value = value
        assert po.value == value
        assert po.bits == data

    def test_int8_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        po = Int8(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_int8_assign_invalid_value(self) -> None:
        name = "test"
        value = 9001
        po = Int8(name=name)
        with pytest.raises(OverflowError):
            po.value = value

    def test_int8_parse_bytes(self) -> None:
        name = "test"
        value = 1
        byte_data = b"\x01"
        data = bitarray()
        data.frombytes(byte_data)
        po = Int8(name=name, data=byte_data)
        assert po.value == value
        assert po.bits == data

    def test_int8_parse_bits(self) -> None:
        name = "test"
        value = 1
        byte_data = b"\x01"
        bit_data = bitarray()
        bit_data.frombytes(byte_data)
        po = Int8(name=name, data=bit_data)
        assert po.value == value
        assert po.bits == bit_data

    def test_int8_parse_bits2(self) -> None:
        name = "test"
        value = 1
        byte_data = b"\x01"
        bit_data1 = bitarray("001")
        bit_data2 = bitarray()
        bit_data2.frombytes(byte_data)
        po = Int8(name=name, data=bit_data1)
        assert po.value == value
        assert po.bits == bit_data2

    def test_int8_init_value(self) -> None:
        name = "test"
        value = 1
        data = bitarray()
        data.frombytes(b"\x01")
        po = Int8(name=name, value=value)
        assert po.value == value
        assert po.bits == data


class TestUInt16:
    def test_int16_create(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00\x00")
        po = Int16(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int16.__name__ in repr(po)

    def test_int16_getters(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00\x00")
        po = Int16(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int16.__name__ in repr(po)

    def test_int16_setter(self) -> None:
        name = "test"
        initial_value = 0
        initial_data = bitarray()
        initial_data.frombytes(b"\x00\x00")
        value = 1
        data = bitarray()
        data.frombytes(b"\x00\x01")
        po = Int16(name=name)
        assert po.value == initial_value
        assert po.bits == initial_data
        po.value = value
        assert po.value == value
        assert po.bits == data

    def test_int16_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        po = Int16(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_int16_assign_invalid_value(self) -> None:
        name = "test"
        value = 90000001
        po = Int16(name=name)
        with pytest.raises(OverflowError):
            po.value = value

    def test_int16_parse(self) -> None:
        name = "test"
        value = 1
        byte_data = b"\x00\x01"
        data = bitarray()
        data.frombytes(byte_data)
        po = Int16(name=name, data=byte_data)
        assert po.value == value
        assert po.bits == data

    def test_int16_init_value(self) -> None:
        name = "test"
        value = 1
        data = bitarray()
        data.frombytes(b"\x00\x01")
        po = Int16(name=name, value=value)
        assert po.value == value
        assert po.bits == data


class TestInt24:
    def test_int8_create_empty(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00\x00\x00")
        po = Int24(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int24.__name__ in repr(po)


class TestUInt32:
    def test_int32_create(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00\x00\x00\x00")
        po = Int32(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int32.__name__ in repr(po)

    def test_int32_getters(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00\x00\x00\x00")
        po = Int32(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int32.__name__ in repr(po)

    def test_int32_setter(self) -> None:
        name = "test"
        initial_value = 0
        initial_data = bitarray()
        initial_data.frombytes(b"\x00\x00\x00\x00")
        value = 1
        data = bitarray()
        data.frombytes(b"\x00\x00\x00\x01")
        po = Int32(name=name)
        assert po.value == initial_value
        assert po.bits == initial_data
        po.value = value
        assert po.value == value
        assert po.bits == data

    def test_int32_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        po = Int32(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_int32_assign_invalid_value(self) -> None:
        name = "test"
        value = 900000000001
        po = Int32(name=name)
        with pytest.raises(OverflowError):
            po.value = value

    def test_int32_parse(self) -> None:
        name = "test"
        value = 1
        byte_data = b"\x00\x00\x00\x01"
        data = bitarray()
        data.frombytes(byte_data)
        po = Int32(name=name, data=byte_data)
        assert po.value == value
        assert po.bits == data

    def test_int32_init_value(self) -> None:
        name = "test"
        value = 1
        data = bitarray()
        data.frombytes(b"\x00\x00\x00\x01")
        po = Int32(name=name, value=value)
        assert po.value == value
        assert po.bits == data


class TestUInt64:
    def test_int64_create(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00\x00\x00\x00\x00\x00\x00\x00")
        po = Int64(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int64.__name__ in repr(po)

    def test_int64_getters(self) -> None:
        name = "test"
        value = 0
        data = bitarray()
        data.frombytes(b"\x00\x00\x00\x00\x00\x00\x00\x00")
        po = Int64(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.bits == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert Int64.__name__ in repr(po)

    def test_int64_setter(self) -> None:
        name = "test"
        initial_value = 0
        initial_data = bitarray()
        initial_data.frombytes(b"\x00\x00\x00\x00\x00\x00\x00\x00")
        value = 1
        data = bitarray()
        data.frombytes(b"\x00\x00\x00\x00\x00\x00\x00\x01")
        po = Int64(name=name)
        assert po.value == initial_value
        assert po.bits == initial_data
        po.value = value
        assert po.value == value
        assert po.bits == data

    def test_int64_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        po = Int64(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_int64_assign_invalid_value(self) -> None:
        name = "test"
        value = -900000000000000000000000000000000000000000000000000000000000000000000
        po = Int64(name=name)
        with pytest.raises(OverflowError):
            po.value = value

    def test_int64_parse(self) -> None:
        name = "test"
        value = 1
        byte_data = b"\x00\x00\x00\x00\x00\x00\x00\x01"
        data = bitarray()
        data.frombytes(byte_data)
        po = Int64(name=name, data=byte_data)
        assert po.value == value
        assert po.bits == data

    def test_int64_init_value(self) -> None:
        name = "test"
        value = 1
        byte_data = b"\x00\x00\x00\x00\x00\x00\x00\x01"
        data = bitarray()
        data.frombytes(byte_data)
        po = Int64(name=name, value=value)
        assert po.value == value
        assert po.bits == data
