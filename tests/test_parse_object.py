import pytest
from easyprotocol.parse_object import ParseObject


class TestParseObject:
    def test_parseobject_create(self) -> None:
        name = "test"
        po = ParseObject(name=name)
        assert po is not None
        assert po.name == name
        assert po.value is None
        assert po.data is None
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseObject.__name__ in repr(po)

    def test_parseobject_getters(self) -> None:
        name = "test"
        value = 1
        data = b""
        po = ParseObject(name=name)
        po._value = value
        po._data = data
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
        assert ParseObject.__name__ in repr(po)

    def test_parseobject_setter(self) -> None:
        name = "test"
        value = 1
        po = ParseObject(name=name)
        assert po.value is None
        with pytest.raises(NotImplementedError):
            po.value = value

    def test_parseobject_parse(self) -> None:
        name = "test"
        data = b"\x00"
        with pytest.raises(NotImplementedError):
            ParseObject(name=name, data=data)

    def test_parseobject_init_value(self) -> None:
        name = "test"
        value = 11
        with pytest.raises(NotImplementedError):
            ParseObject(name=name, value=value)
