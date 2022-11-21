from easyprotocol.fields.flags import FlagsField
from enum import IntFlag
import pytest


class TestFlags:
    def test_enum_create_empty(self) -> None:
        class TestFlags(IntFlag):
            NONE = 0
            ONE = 1
            TWO = 2
            FOUR = 4
            EIGHT = 8

        name = "flags"
        obj = FlagsField(name=name, bit_count=2, enum_type=TestFlags)
        assert obj.name == name
        assert obj.value == TestFlags.NONE

    def test_enum_create_parse(self) -> None:
        class TestFlags(IntFlag):
            ONE = 1
            TWO = 2
            FOUR = 4
            EIGHT = 8

        name = "flags"
        obj = FlagsField(name=name, bit_count=2, enum_type=TestFlags, data=b"\x01")
        assert obj.name == name
        assert obj.value == TestFlags.ONE

    def test_enum_create_invalid1(self) -> None:
        class TestFlags(IntFlag):
            ONE = 1
            TWO = 2
            FOUR = 4
            EIGHT = 8

        name = "flags"
        obj = FlagsField(name=name, bit_count=2, enum_type=TestFlags, data=b"\x0f")
        assert obj.name == name
        assert obj.value == TestFlags.ONE | TestFlags.TWO

    def test_enum_create_invalid2(self) -> None:
        class TestFlags(IntFlag):
            ONE = 1
            TWO = 2
            FOUR = 4

        name = "flags"
        ff = FlagsField(name=name, bit_count=4, enum_type=TestFlags, data=b"\x0f")
        with pytest.raises(TypeError):
            ff.value = "pickles"
