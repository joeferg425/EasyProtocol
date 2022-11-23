from __future__ import annotations
from easyprotocol.base.parse_object import InputT

from easyprotocol.fields.unsigned_int import UIntField
from typing import Literal, TypeVar, Generic
from enum import IntFlag

F = TypeVar("F", IntFlag, IntFlag)


class FlagsField(UIntField, Generic[F]):
    def __init__(
        self,
        name: str,
        bit_count: int,
        enum_type: type[F],
        data: InputT | None = None,
        value: int | None = None,
        endian: Literal["little", "big"] = "big",
    ) -> None:
        self.enum_type = enum_type
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            value=value,
            endian=endian,
        )

    def _get_value(self) -> F | None:
        v = super()._get_value()
        if v is None:
            return None
        else:
            return self.enum_type(v)

    def _set_value(self, value: F | int) -> None:
        if isinstance(value, type(F)):
            _value = value.value
        else:
            _value = value
        super()._set_value(_value)

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.value.name


class UInt8FlagsField(FlagsField):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        data: InputT | None = None,
        value: int | None = None,
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            bit_count=8,
            enum_type=enum_type,
            data=data,
            value=value,
            endian=endian,
        )


class UInt16FlagsField(FlagsField):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        data: InputT | None = None,
        value: int | None = None,
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            bit_count=16,
            enum_type=enum_type,
            data=data,
            value=value,
            endian=endian,
        )


class UInt24FlagsField(FlagsField):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        data: InputT | None = None,
        value: int | None = None,
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            bit_count=24,
            enum_type=enum_type,
            data=data,
            value=value,
            endian=endian,
        )


class UInt32FlagsField(FlagsField):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        data: InputT | None = None,
        value: int | None = None,
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            bit_count=32,
            enum_type=enum_type,
            data=data,
            value=value,
            endian=endian,
        )
