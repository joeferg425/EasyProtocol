from __future__ import annotations

from enum import IntEnum
from typing import TypeVar, Union

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.utils import dataT
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

E = TypeVar("E", bound=Union[IntEnum, int])


class EnumField(UIntFieldGeneric[E]):
    def __init__(
        self,
        name: str,
        bit_count: int,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        self._enum_type: type[E] = enum_type
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )

    def get_value(self) -> E:
        v = super().get_value()
        try:
            return self._enum_type(v)
        except:
            return v

    def set_value(self, value: E) -> None:
        if isinstance(value, IntEnum):
            _value = value.value
        else:
            _value = value
        super().set_value(_value)

    @property
    def string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        v = self.value
        if isinstance(v, IntEnum):
            return v.name
        else:
            return f"{v}:?UNDEFINED?"

    @property
    def value(self) -> E:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: E) -> None:
        self.set_value(value)


class UInt8EnumField(EnumField[E]):
    def __init__(
        self,
        name: str,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=8,
            enum_type=enum_type,
            data=data,
            default=default,
            endian=endian,
        )


class UInt16EnumField(EnumField[E]):
    def __init__(
        self,
        name: str,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=16,
            enum_type=enum_type,
            data=data,
            default=default,
            endian=endian,
        )


class UInt24EnumField(EnumField[E]):
    def __init__(
        self,
        name: str,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=24,
            enum_type=enum_type,
            data=data,
            default=default,
            endian=endian,
        )


class UInt32EnumField(EnumField[E]):
    def __init__(
        self,
        name: str,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=32,
            enum_type=enum_type,
            data=data,
            default=default,
            endian=endian,
        )
