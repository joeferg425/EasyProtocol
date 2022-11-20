"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from easyprotocol.base.parse_object import ParseObject
from easyprotocol.base.utils import InputT, input_to_bytes
import math
from bitarray import bitarray
from typing import Literal


class UIntField(ParseObject[int]):
    """The base parsing object for unsigned integers."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = "{:X}(hex)",
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
            bits = bitarray("0" * (len(bit_mask) - len(bits))) + bits
        my_bits = (bits & bit_mask)[-self.bit_count :]  # noqa
        temp_bits = bitarray(my_bits)
        byte_count = math.ceil(self.bit_count / 8)
        if len(temp_bits) < byte_count * 8:
            temp_bits = bitarray("0" * ((byte_count * 8) - len(temp_bits))) + temp_bits
        my_bytes = bytearray(temp_bits.tobytes())
        byte_length = math.ceil(self.bit_count / 8)
        self._value = int.from_bytes(my_bytes, byteorder=self.endian, signed=False)
        my_bytes = int.to_bytes(
            int.from_bytes(my_bytes, byteorder="big"), length=byte_length, byteorder="little", signed=False
        )
        self._bits = bitarray()
        self._bits.frombytes(my_bytes)
        if self.endian == "big":
            self._value = int.from_bytes(my_bytes, byteorder=self.endian, signed=False)
        if len(self._bits) < self.bit_count:
            self._bits = bitarray("0" * (self.bit_count - len(self._bits))) + self._bits
        if len(self._bits) > self.bit_count:
            self._bits = self._bits[-self.bit_count :]  # noqa

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
        bits = bitarray()
        byte_count = math.ceil(self.bit_count / 8)
        bytes_val = int.to_bytes(value, length=byte_count, byteorder="big", signed=False)
        int_val = int.from_bytes(bytes_val, byteorder=self._endian, signed=False)
        bits.frombytes(int.to_bytes(int_val, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits
        self._value = value

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        b = self._bits.tobytes()
        byte_length = math.ceil(self.bit_count / 8)
        if self.endian == "little":
            return int.to_bytes(
                int.from_bytes(b, byteorder="big"), length=byte_length, byteorder="little", signed=False
            )
        else:
            return b


class BoolField(UIntField):
    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=1,
            data=data,
            value=value,
            format="{}",
            endian="big",
        )

    @property
    def value(self) -> bool:
        return bool(self._value)

    @value.setter
    def value(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        value = int(value)
        bits = bitarray()
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[-self.bit_count :]  # noqa
        self._value = value


class UInt8Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = "{:02X}(hex)",
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
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = "{:04X}(hex)",
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
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = "{:06X}(hex)",
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
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = "{:08X}(hex)",
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
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = "{:016X}(hex)",
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
