from easyprotocol.fields.enum import EnumField
from enum import IntEnum
import pytest


class TestEnums:
    def test_enum_create_empty(self) -> None:
        class TestEnum(IntEnum):
            ZERO = 0
            ONE = 1
            TWO = 2
            THREE = 3

        name = "enum"
        obj = EnumField(name=name, bit_count=2, enum_type=TestEnum)
        assert obj.name == name
        assert obj.value == TestEnum.ZERO

    def test_enum_create_parse(self) -> None:
        class TestEnum(IntEnum):
            ZERO = 0
            ONE = 1
            TWO = 2
            THREE = 3

        name = "enum"
        obj = EnumField(name=name, bit_count=2, enum_type=TestEnum, data=b"\x01")
        assert obj.name == name
        assert obj.value == TestEnum.ONE

    def test_enum_create_invalid1(self) -> None:
        class TestEnum(IntEnum):
            ZERO = 0
            ONE = 1
            TWO = 2
            THREE = 3

        name = "enum"
        obj = EnumField(name=name, bit_count=2, enum_type=TestEnum, data=b"\x0f")
        assert obj.name == name
        assert obj.value == TestEnum.THREE

    def test_enum_create_invalid2(self) -> None:
        class TestEnum(IntEnum):
            ZERO = 0
            ONE = 1
            TWO = 2
            THREE = 3

        name = "enum"
        with pytest.raises(ValueError):
            EnumField(name=name, bit_count=4, enum_type=TestEnum, data=b"\x0f")
