from __future__ import annotations
from typing import Literal
from bitarray import bitarray
from easyprotocol.base.parse_object import ParseObject
from easyprotocol.base.utils import InputT, input_to_bytes
import math
import struct


class FloatField(ParseObject[float]):
    """The base parsing object for unsigned floating point values."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        data: InputT | None = None,
        value: float | None = None,
        format: str | None = "{:.3e}",
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
            self.value = 0.0


class Float32IEEField(FloatField):
    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: float | None = None,
        format: str | None = "{:.3e}",
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name,
            bit_count=32,
            data=data,
            value=value,
            format=format,
            endian=endian,
        )

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
        temp_value = int.from_bytes(my_bytes, byteorder="big", signed=False)
        my_bytes = int.to_bytes(temp_value, byte_count, byteorder="little", signed=False)
        if self.endian == "big":
            self._value = struct.unpack(">f", my_bytes)[0]
        else:
            self._value = struct.unpack("<f", my_bytes)[0]
        my_bits = bitarray()
        my_bits.frombytes(my_bytes)
        self._bits = my_bits[-self.bit_count :]  # noqa
        if len(bits) >= self.bit_count:
            return bits[: -self.bit_count]  # noqa
        else:
            return bitarray()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        bits = bitarray()
        if self.endian == "little":
            bytes_val = struct.pack("<f", value)
        else:
            bytes_val = struct.pack(">f", value)
        bits.frombytes(bytes_val)
        self._bits = bits
        self._value = value

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self._bits.tobytes()


class Float32Field(Float32IEEField):
    ...