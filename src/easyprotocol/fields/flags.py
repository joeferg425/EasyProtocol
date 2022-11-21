from __future__ import annotations
import math
from easyprotocol.base.parse_object import InputT

from easyprotocol.fields.unsigned_int import UIntField
from typing import Literal, TypeVar, Generic
from enum import IntFlag
from bitarray import bitarray

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

    @property
    def value(self) -> F:
        if self._value is None:
            return self.enum_type(0)
        else:
            return self.enum_type(self._value)

    @value.setter
    def value(self, value: int | F) -> None:
        if not isinstance(value, (int, F)):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        bits = bitarray()
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[-self.bit_count :]  # noqa
        mask = (2**self.bit_count) - 1
        self._value = value & mask

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


class UInt16EnumField(FlagsField):
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


class UInt24EnumField(FlagsField):
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


class UInt32EnumField(FlagsField):
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
