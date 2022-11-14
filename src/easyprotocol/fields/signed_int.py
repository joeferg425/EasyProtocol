"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from typing import Literal
from bitarray import bitarray
from easyprotocol.base.parse_object import ParseObject
from bitarray.util import int2ba, ba2int
import math


class IntField(ParseObject[int]):
    """The base parsing object for unsigned integers."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{}",
        endian: Literal["little", "big"] = "big",
    ) -> None:
        self.bit_count = bit_count
        super().__init__(
            name=name,
            data=data,
            value=value,
            format=format,
            endian=endian,
        )
        if self.value is None:
            self.value = 0

    def parse(self, data: bytes | bitarray) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        if isinstance(data, (bytes, bytearray)):
            i = int.from_bytes(data, byteorder="big", signed=False)
            bits = int2ba(i)
            if len(bits) < (8 * len(data)):
                bits = bitarray("0" * ((8 * len(data)) - len(bits))) + bits
        else:
            bits = bitarray(data)
        if len(bits) < self.bit_count:
            bits = bitarray("0" * (self.bit_count - len(bits))) + bits
        _bit_mask = (2**self.bit_count) - 1
        bit_mask = bitarray()
        bit_mask.frombytes(
            int.to_bytes(_bit_mask, length=math.ceil(self.bit_count / 8), byteorder=self._endian, signed=False)
        )
        if len(bit_mask) < len(bits):
            bit_mask = bitarray("0" * (len(bits) - len(bit_mask))) + bit_mask
        if len(bits) < len(bit_mask):
            bits = bitarray("0" * (len(bit_mask) - len(bits))) + bits
        self._bits = (bits & bit_mask)[-self.bit_count :]  # noqa
        self._value = ba2int(self._bits, signed=False)
        byte_length = math.ceil(self.bit_count / 8)
        self._value = int.from_bytes(
            int.to_bytes(self._value, length=byte_length, byteorder="big"), byteorder=self._endian, signed=True
        )

        if len(bits) > self.bit_count:
            return bits[-self.bit_count :]  # noqa
        else:
            return bitarray()

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        bits = bitarray()
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=True))
        self._bits = bits
        self._value = value


class Int8Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{}",
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=8,
            format=format,
            endian=endian,
        )


class Int16Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{}",
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=16,
            format=format,
            endian=endian,
        )


class Int24Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{}",
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=24,
            format=format,
            endian=endian,
        )


class Int32Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{}",
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=32,
            format=format,
            endian=endian,
        )


class Int64Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | None = None,
        value: int | None = None,
        format: str | None = "{}",
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=64,
            format=format,
            endian=endian,
        )
