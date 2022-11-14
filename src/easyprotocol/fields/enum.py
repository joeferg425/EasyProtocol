from __future__ import annotations
import math

from easyprotocol.fields.unsigned_int import UintField
from typing import TypeVar, Generic
from enum import IntEnum
from bitarray import bitarray

T = TypeVar("T", IntEnum, IntEnum)


class EnumField(UintField, Generic[T]):
    def __init__(
        self,
        name: str,
        bit_count: int,
        enum_type: type[T],
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        self.enum_type = enum_type
        super().__init__(
            name,
            bit_count,
            data,
            value,
        )

    @property
    def value(self) -> T:
        if self._value is None:
            return self.enum_type(0)
        else:
            return self.enum_type(self._value)

    @value.setter
    def value(self, value: int | T) -> None:
        if not isinstance(value, int, T):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        bits = bitarray()
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder="big", signed=False))
        self._bits = bits
        self._value = value
