"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from easyprotocol.base.parse_object import ParseObject
import math
from bitarray import bitarray
from bitarray.util import int2ba, ba2int
from typing import Literal


class UIntField(ParseObject[int]):
    """The base parsing object for unsigned integers."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{:X}",
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
            data = bytearray(data)
            data.reverse()
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
        _bits = (bits & bit_mask)[-self.bit_count :]  # noqa
        _value = ba2int(_bits, signed=False)
        byte_length = math.ceil(self.bit_count / 8)
        _bytes = bytearray(int.to_bytes(_value, length=byte_length, byteorder=self.endian))
        self._value = int.from_bytes(_bytes, byteorder=self._endian, signed=False)
        self._bits = bitarray()
        if self.endian == "little":
            self._bits.frombytes(_bytes)
        else:
            _int = int.from_bytes(_bytes, byteorder="big")
            _bytes = bytearray(int.to_bytes(_int, length=byte_length, byteorder="little"))
            self._bits.frombytes(_bytes)
        if len(self._bits) < self.bit_count:
            self._bits = bitarray("0" * (self.bit_count - len(self._bits))) + self._bits

        if len(bits) > self.bit_count:
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
        bits = bitarray()
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits
        self._value = value

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        b = self._bits.tobytes()
        byte_length = math.ceil(self.bit_count / 8)
        i = int.from_bytes(b, byteorder="big")
        return int.to_bytes(i, length=byte_length, byteorder=self._endian)


class UInt8Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{:02X}",
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


class UInt16Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{:04X}",
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


class UInt24Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{:06X}",
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


class UInt32Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{:08X}",
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


class UInt64Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{:016X}",
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
