from __future__ import annotations
from easyprotocol.base.parse_object import InputT

from easyprotocol.fields.unsigned_int import UIntField
from typing import Literal, TypeVar, Generic
from enum import IntEnum

E = TypeVar("E", IntEnum, IntEnum)


class EnumField(UIntField, Generic[E]):
    def __init__(
        self,
        name: str,
        bit_count: int,
        enum_type: type[E],
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

    def _get_value(self) -> int | None:
        v = super()._get_value()
        if v is None:
            return None
        return self.enum_type(v)

    def _set_value(self, value: E | int) -> None:
        if isinstance(value, type(E)):
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

    @property
    def value(self) -> E | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: E | int) -> None:
        self._set_value(value)


class UInt8EnumField(EnumField):
    def __init__(
        self,
        name: str,
        enum_type: type[E],
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


class UInt16EnumField(EnumField):
    def __init__(
        self,
        name: str,
        enum_type: type[E],
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


class UInt24EnumField(EnumField):
    def __init__(
        self,
        name: str,
        enum_type: type[E],
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


class UInt32EnumField(EnumField):
    def __init__(
        self,
        name: str,
        enum_type: type[E],
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
