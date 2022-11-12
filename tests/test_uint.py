import pytest
from easyprotocol.unsigned_int import UInt8, UInt16, UInt32, UInt64


class TestUInt08:
    def test_uint8_create(self) -> None:
        name = "test"
        value = 0
        data = b"\x00"
        po = UInt8(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.data == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert UInt8.__name__ in repr(po)

    def test_uint8_getters(self) -> None:
        name = "test"
        value = 0
        data = b"\x00"
        po = UInt8(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.data == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert UInt8.__name__ in repr(po)

    def test_uint8_setter(self) -> None:
        name = "test"
        initial_value = 0
        initial_data = b"\x00"
        value = 1
        data = b"\x01"
        po = UInt8(name=name)
        assert po.value == initial_value
        assert po.data == initial_data
        po.value = value
        assert po.value == value
        assert po.data == data

    def test_uint8_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        po = UInt8(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_uint8_assign_invalid_value(self) -> None:
        name = "test"
        value = 9001
        po = UInt8(name=name)
        with pytest.raises(ValueError):
            po.value = value

    def test_uint8_parse(self) -> None:
        name = "test"
        value = 1
        data = b"\x01"
        po = UInt8(name=name, data=data)
        assert po.value == value
        assert po.data == data

    def test_uint8_init_value(self) -> None:
        name = "test"
        value = 1
        data = b"\x01"
        po = UInt8(name=name, value=value)
        assert po.value == value
        assert po.data == data


class TestUInt16:
    def test_uint16_create(self) -> None:
        name = "test"
        value = 0
        data = b"\x00\x00"
        po = UInt16(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.data == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert UInt16.__name__ in repr(po)

    def test_uint16_getters(self) -> None:
        name = "test"
        value = 0
        data = b"\x00\x00"
        po = UInt16(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.data == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert UInt16.__name__ in repr(po)

    def test_uint16_setter(self) -> None:
        name = "test"
        initial_value = 0
        initial_data = b"\x00\x00"
        value = 1
        data = b"\x00\x01"
        po = UInt16(name=name)
        assert po.value == initial_value
        assert po.data == initial_data
        po.value = value
        assert po.value == value
        assert po.data == data

    def test_uint16_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        po = UInt16(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_uint16_assign_invalid_value(self) -> None:
        name = "test"
        value = 90000001
        po = UInt16(name=name)
        with pytest.raises(ValueError):
            po.value = value

    def test_uint16_parse(self) -> None:
        name = "test"
        value = 1
        data = b"\x00\x01"
        po = UInt16(name=name, data=data)
        assert po.value == value
        assert po.data == data

    def test_uint16_init_value(self) -> None:
        name = "test"
        value = 1
        data = b"\x00\x01"
        po = UInt16(name=name, value=value)
        assert po.value == value
        assert po.data == data


class TestUInt32:
    def test_uint32_create(self) -> None:
        name = "test"
        value = 0
        data = b"\x00\x00\x00\x00"
        po = UInt32(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.data == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert UInt32.__name__ in repr(po)

    def test_uint32_getters(self) -> None:
        name = "test"
        value = 0
        data = b"\x00\x00\x00\x00"
        po = UInt32(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.data == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert UInt32.__name__ in repr(po)

    def test_uint32_setter(self) -> None:
        name = "test"
        initial_value = 0
        initial_data = b"\x00\x00\x00\x00"
        value = 1
        data = b"\x00\x00\x00\x01"
        po = UInt32(name=name)
        assert po.value == initial_value
        assert po.data == initial_data
        po.value = value
        assert po.value == value
        assert po.data == data

    def test_uint32_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        po = UInt32(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_uint32_assign_invalid_value(self) -> None:
        name = "test"
        value = 900000000001
        po = UInt32(name=name)
        with pytest.raises(ValueError):
            po.value = value

    def test_uint32_parse(self) -> None:
        name = "test"
        value = 1
        data = b"\x00\x00\x00\x01"
        po = UInt32(name=name, data=data)
        assert po.value == value
        assert po.data == data

    def test_uint32_init_value(self) -> None:
        name = "test"
        value = 1
        data = b"\x00\x00\x00\x01"
        po = UInt32(name=name, value=value)
        assert po.value == value
        assert po.data == data


class TestUInt64:
    def test_uint64_create(self) -> None:
        name = "test"
        value = 0
        data = b"\x00\x00\x00\x00\x00\x00\x00\x00"
        po = UInt64(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.data == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert UInt64.__name__ in repr(po)

    def test_uint64_getters(self) -> None:
        name = "test"
        value = 0
        data = b"\x00\x00\x00\x00\x00\x00\x00\x00"
        po = UInt64(name=name)
        assert po is not None
        assert po.name == name
        assert po.value == value
        assert po.data == data
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert UInt64.__name__ in repr(po)

    def test_uint64_setter(self) -> None:
        name = "test"
        initial_value = 0
        initial_data = b"\x00\x00\x00\x00\x00\x00\x00\x00"
        value = 1
        data = b"\x00\x00\x00\x00\x00\x00\x00\x01"
        po = UInt64(name=name)
        assert po.value == initial_value
        assert po.data == initial_data
        po.value = value
        assert po.value == value
        assert po.data == data

    def test_uint64_assign_invalid_type(self) -> None:
        name = "test"
        value = "invalid"
        po = UInt64(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_uint64_assign_invalid_value(self) -> None:
        name = "test"
        value = -900000000001
        po = UInt64(name=name)
        with pytest.raises(ValueError):
            po.value = value

    def test_uint64_parse(self) -> None:
        name = "test"
        value = 1
        data = b"\x00\x00\x00\x00\x00\x00\x00\x01"
        po = UInt64(name=name, data=data)
        assert po.value == value
        assert po.data == data

    def test_uint64_init_value(self) -> None:
        name = "test"
        value = 1
        data = b"\x00\x00\x00\x00\x00\x00\x00\x01"
        po = UInt64(name=name, value=value)
        assert po.value == value
        assert po.data == data
