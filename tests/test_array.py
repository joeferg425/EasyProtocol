from __future__ import annotations
import pytest
from easyprotocol.fields.array import ArrayField
from easyprotocol.base.parse_list import ParseList
from easyprotocol.fields.unsigned_int import UInt8Field


class TestArray:
    def test_array_create_empty(self) -> None:
        name = "parent"
        f1_name = "count"
        f1 = UInt8Field(name=f1_name)
        f2_name = "array"
        f2 = ArrayField(name=f2_name, count_field=f1, array_item_class=UInt8Field)
        data = b"\x00"
        obj = ParseList(name=name, children=[f1, f2])
        obj.parse(data=data)

        assert f1.value == 0
        assert f2.value == []

    def test_array_create_one(self) -> None:
        name = "parent"
        f1_name = "count"
        f1 = UInt8Field(name=f1_name)
        f2_name = "array"
        f2 = ArrayField(name=f2_name, count_field=f1, array_item_class=UInt8Field)
        data = b"\x01\x00"
        obj = ParseList(name=name, children=[f1, f2])
        obj.parse(data=data)

        assert f1.value == 1
        assert f2.value == [0]

    def test_array_create_three(self) -> None:
        name = "parent"
        f1_name = "count"
        f1 = UInt8Field(name=f1_name)
        f2_name = "array"
        f2 = ArrayField(name=f2_name, count_field=f1, array_item_class=UInt8Field)
        data = b"\x03\x00\x01\x02"
        obj = ParseList(name=name, children=[f1, f2])
        obj.parse(data=data)

        assert f1.value == 3
        assert f2.value == [0, 1, 2]

    def test_array_create_invalid(self) -> None:
        name = "parent"
        f1_name = "count"
        f1 = ParseList(name=f1_name)
        f2_name = "array"
        f2 = ArrayField(name=f2_name, count_field=f1, array_item_class=UInt8Field)  # type:ignore
        data = b"\x02\x01\x00\x03"
        with pytest.raises(TypeError):
            obj = ParseList(name=name, children=[f1, f2])
            obj.parse(data=data)
