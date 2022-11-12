from __future__ import annotations
from typing import Any
import pytest
from easyprotocol.parse_dict import ParseDict
from easyprotocol.unsigned_int import UInt8


class TestParseDict:
    def test_parsedict_create(self) -> None:
        name = "test"
        po = ParseDict(name=name)
        assert po is not None
        assert po.name == name
        assert po.value is not None
        assert po.data is not None
        assert isinstance(po.formatted_value, str)
        assert isinstance(bytes(po), bytes)
        assert isinstance(str(po), str)
        assert name in str(po)
        assert isinstance(repr(po), str)
        assert name in repr(po)
        assert ParseDict.__name__ in repr(po)

    def test_parsedict_getters(self) -> None:
        name = "test"
        value: dict[str, Any] = dict()
        data = b""
        po = ParseDict(name=name)
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
        assert ParseDict.__name__ in repr(po)

    def test_parsedict_setter_invalid(self) -> None:
        name = "test"
        value = 1
        po = ParseDict(name=name)
        with pytest.raises(TypeError):
            po.value = value  # type:ignore

    def test_parsedict_setter_invalid2(self) -> None:
        name = "test"
        value = 1
        po = ParseDict(name=name)
        with pytest.raises(TypeError):
            po["x"] = "popcorn"  # type:ignore

    def test_parsedict_setter(self) -> None:
        name = "test"
        f1_name = "f1"
        f1 = UInt8(name=f1_name)
        po = ParseDict(name=name)

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == b"\x00"
        assert f1.value is not None
        assert f1.value == 0

        assert po.data is not None
        assert po.data == b""
        assert po.value is not None
        assert po.value == {}

        po.value = {f1.name: f1}

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == b"\x00"
        assert f1.value is not None
        assert f1.value == 0

        assert po.data is not None
        assert po.data == b"\x00"
        assert po.value is not None
        assert po.value == {f1.name: f1}

        po.value = {f1.name: 1}

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == b"\x01"
        assert f1.value is not None
        assert f1.value == 1

        assert po.data is not None
        assert po.data == b"\x01"
        assert po.value is not None
        assert po.value == {f1.name: f1}

    def test_parsedict_parse(self) -> None:
        name = "test"
        data = b"\x00"
        ParseDict(name=name, data=data)

    def test_parsedict_init_value(self) -> None:
        name = "test"
        value = 11
        with pytest.raises(TypeError):
            ParseDict(name=name, value=value)  # type:ignore

    def test_parsing_single_field(self) -> None:
        p_name = "test"
        p_data = b"\xff"
        f1_name = "f1"
        f1_value = 255
        f1_data = b"\xff"
        left_over = b""
        f1 = UInt8(name=f1_name)
        p_value = {f1_name: f1}
        p = ParseDict(name=p_name)
        p[f1.name] = f1

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == b"\x00"
        assert f1.value is not None
        assert f1.value == 0

        remainder = p.parse(p_data)

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == f1_data
        assert f1.value is not None
        assert f1.value == f1_value

        assert remainder == left_over
        assert p is not None
        assert p.name == p_name
        assert p.data is not None
        assert p.data == p_data
        assert p.value is not None
        assert p.value == p_value
        assert isinstance(p.formatted_value, str)
        assert isinstance(bytes(p), bytes)
        assert isinstance(str(p), str)
        assert p_name in str(p)
        assert f1_name in str(p)
        assert isinstance(repr(p), str)
        assert p_name in repr(p)
        assert f1_name in repr(p)
        assert ParseDict.__name__ in repr(p)

    def test_parsing_multi_field(self) -> None:
        p_name = "test"
        p_data = b"\xaa\xbb\xcc"
        f1_name = "f1"
        f1_value = 170
        f1_data = b"\xaa"
        f1 = UInt8(name=f1_name)
        f2_name = "f2"
        f2_value = 187
        f2_data = b"\xbb"
        f2 = UInt8(name=f2_name)
        f3_name = "f3"
        f3_value = 204
        f3_data = b"\xcc"
        f3 = UInt8(name=f3_name)
        left_over = b""
        p_value = {f1_name: f1, f2_name: f2, f3_name: f3}
        p = ParseDict(name=p_name)
        p[f1.name] = f1
        p[f2.name] = f2
        p[f3.name] = f3

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == b"\x00"
        assert f1.value is not None
        assert f1.value == 0

        assert f2.name == f2_name
        assert f2.data is not None
        assert f2.data == b"\x00"
        assert f2.value is not None
        assert f2.value == 0

        assert f3.name == f3_name
        assert f3.data is not None
        assert f3.data == b"\x00"
        assert f3.value is not None
        assert f3.value == 0

        remainder = p.parse(p_data)

        assert f1.name == f1_name
        assert f1.data is not None
        assert f1.data == f1_data
        assert f1.value is not None
        assert f1.value == f1_value

        assert f2.name == f2_name
        assert f2.data is not None
        assert f2.data == f2_data
        assert f2.value is not None
        assert f2.value == f2_value

        assert f3.name == f3_name
        assert f3.data is not None
        assert f3.data == f3_data
        assert f3.value is not None
        assert f3.value == f3_value

        assert remainder == left_over
        assert p is not None
        assert p.name == p_name
        assert p.data is not None
        assert p.data == p_data
        assert p.value is not None
        assert p.value == p_value
        assert isinstance(p.formatted_value, str)
        assert isinstance(bytes(p), bytes)
        assert isinstance(str(p), str)
        assert p_name in str(p)
        assert f1_name in str(p)
        assert f2_name in str(p)
        assert f3_name in str(p)
        assert isinstance(repr(p), str)
        assert p_name in repr(p)
        assert f1_name in repr(p)
        assert f2_name in repr(p)
        assert f3_name in repr(p)
        assert ParseDict.__name__ in repr(p)
