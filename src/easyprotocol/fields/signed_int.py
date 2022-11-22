"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from typing import Literal
from bitarray import bitarray
from easyprotocol.base.parse_object import ParseObject
from easyprotocol.base.utils import InputT, input_to_bytes
import math


class IntField(ParseObject[int]):
    """The base parsing object for unsigned integers."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        data: InputT | None = None,
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

    def parse(self, data: InputT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        bits = input_to_bytes(
            data=data,
            bit_count=self.bit_count,
        )
        _bit_mask = (2**self.bit_count) - 1
        bit_mask = bitarray()
        bit_mask.frombytes(int.to_bytes(_bit_mask, length=math.ceil(self.bit_count / 8), byteorder="big", signed=False))
        if len(bit_mask) < len(bits):
            bit_mask = bitarray("0" * (len(bits) - len(bit_mask))) + bit_mask
        if len(bits) < len(bit_mask):
            raise IndexError("Too little data to parse field.")
        my_bits = (bits & bit_mask)[-self.bit_count :]  # noqa
        temp_bits = bitarray(my_bits)
        byte_count = math.ceil(self.bit_count / 8)
        if len(temp_bits) < byte_count * 8:
            temp_bits = bitarray("0" * ((byte_count * 8) - len(temp_bits))) + temp_bits
        my_bytes = bytearray(temp_bits.tobytes())
        self._value = int.from_bytes(my_bytes, byteorder="big", signed=True)
        my_bytes = int.to_bytes(self._value, byte_count, byteorder="little", signed=True)
        if self.endian == "big":
            self._value = int.from_bytes(my_bytes, byteorder=self.endian, signed=True)
        my_bits = bitarray()
        my_bits.frombytes(my_bytes)
        self._bits = my_bits[-self.bit_count :]  # noqa
        if len(bits) >= self.bit_count:
            return bits[: -self.bit_count]  # noqa
        else:
            return bitarray()

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        byte_count = math.ceil(self.bit_count / 8)
        my_bytes = int.to_bytes(value, length=byte_count, byteorder=self.endian, signed=True)
        bits = bitarray()
        bits.frombytes(my_bytes)
        self._bits = bits
        self._value = value

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self._bits.tobytes()


class Int8Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
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
        data: InputT | None = None,
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
        data: InputT | None = None,
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
        data: InputT | None = None,
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
        data: InputT | None = None,
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
