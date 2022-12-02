from __future__ import annotations

from enum import IntFlag
from typing import Sequence, TypeVar, Union, cast

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.utils import dataT
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

F = TypeVar("F", bound=Union[IntFlag, int])


class FlagsField(UIntFieldGeneric[F]):
    def __init__(
        self,
        name: str,
        bit_count: int,
        flags_type: type[F],
        default: F,
        data: dataT | None = None,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        self._flags_type: type[F] = flags_type
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )

    def get_value(self) -> F:
        v = super().get_value()
        try:
            return self._flags_type(v)
        except:
            return v

    def set_value(self, value: F) -> None:
        if isinstance(value, IntFlag):
            _value = value.value
        else:
            _value = value
        super().set_value(_value)

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        value = self.value
        flags_dict: dict[str, IntFlag] = dict(
            self._flags_type._member_map_  # pyright:ignore[reportUnknownMemberType,reportUnknownArgumentType,reportGeneralTypeIssues]
        )
        flags: Sequence[IntFlag] = list(flags_dict.values())
        if isinstance(value, IntFlag):
            return "|".join([v.name for v in flags if v in value and v.name])
        else:
            return ""

    @property
    def value(self) -> F:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: F) -> None:
        self.set_value(value)


class UInt8FlagsField(FlagsField[F]):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        default: F,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=8,
            flags_type=enum_type,
            data=data,
            default=default,
            endian=endian,
        )


class UInt16FlagsField(FlagsField[F]):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        default: F,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=16,
            flags_type=enum_type,
            data=data,
            default=default,
            endian=endian,
        )


class UInt24FlagsField(FlagsField[F]):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        default: F,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=24,
            flags_type=enum_type,
            data=data,
            default=default,
            endian=endian,
        )


class UInt32FlagsField(FlagsField[F]):
    def __init__(
        self,
        name: str,
        enum_type: type[F],
        default: F,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=32,
            flags_type=enum_type,
            data=data,
            default=default,
            endian=endian,
        )
