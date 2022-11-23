from __future__ import annotations
from easyprotocol.base.parse_object import DEFAULT_ENDIANNESS, InputT

from easyprotocol.fields.unsigned_int import UIntField
from typing import Literal, TypeVar, Generic
from enum import IntFlag

F = TypeVar("F", IntFlag, IntFlag)


class FlagsField(UIntField, Generic[F]):
    def __init__(
        self,
        name: str,
        bit_count: int,
        flags_type: type[F],
        data: InputT | None = None,
        value: int | None = None,
        format: str = "{}",
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        init_value: bool = True,
    ) -> None:
        self._flags_type = flags_type
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            value=value,
            endian=endian,
            format=format,
            init_to_zero=False,
        )
        if self.value is None and init_value is True:
            self.value = flags_type[flags_type._member_names_[0]]

    def _get_value(self) -> F | None:
        v = super()._get_value()
        if v is None:
            return None
        else:
            return self._flags_type(v)

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
        return "|".join([v.name for v in self._flags_type._member_map_.values() if v in self.value])

    @property
    def value(self) -> F | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: F | int) -> None:
        self._set_value(value)


class UInt8FlagsField(FlagsField):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        data: InputT | None = None,
        value: int | None = None,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=8,
            flags_type=enum_type,
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
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=16,
            flags_type=enum_type,
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
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=24,
            flags_type=enum_type,
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
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=32,
            flags_type=enum_type,
            data=data,
            value=value,
            endian=endian,
        )
