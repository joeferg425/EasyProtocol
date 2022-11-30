from __future__ import annotations

import math
import struct
from collections import OrderedDict
from typing import Any, Generic, Literal, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_base import DEFAULT_ENDIANNESS, ParseBaseGeneric
from easyprotocol.base.utils import dataT, input_to_bytes

F = TypeVar("F", bound=Union[float, Any])
FLOAT_STRING_FORMAT = "{:.3e}"


class FloatField(ParseBaseGeneric[F]):
    """The base parsing object for unsigned floating point values."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        data: dataT | None = None,
        value: F | None = None,
        format: str | None = FLOAT_STRING_FORMAT,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
    ) -> None:
        self.bit_count = bit_count
        super().__init__(
            name=name,
            data=data,
            value=value,
            string_format=format,
            endian=endian,
        )


class Float32IEEFieldGeneric(FloatField[F]):
    def __init__(
        self,
        name: str,
        data: dataT | None = None,
        value: F | None = None,
        format: str | None = FLOAT_STRING_FORMAT,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        init_to_zero: bool = True,
    ) -> None:
        super().__init__(
            name,
            bit_count=32,
            data=data,
            value=value,
            format=format,
            endian=endian,
        )
        if value is None and data is None and init_to_zero is True:
            self.value = cast(F, 0.0)

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        bits = input_to_bytes(
            data=data,
            bit_count=self.bit_count,
        )
        _bit_mask = (2**self.bit_count) - 1
        bit_mask = bitarray(endian="little")
        bit_mask.frombytes(
            int.to_bytes(_bit_mask, length=math.ceil(self.bit_count / 8), byteorder="little", signed=False)
        )
        if len(bit_mask) < len(bits):
            bit_mask = bitarray("0" * (len(bits) - len(bit_mask))) + bit_mask
        if len(bits) < len(bit_mask):
            raise IndexError("Too little data to parse field.")
        my_bits = (bits & bit_mask)[: self.bit_count]
        temp_bits = bitarray(my_bits)
        byte_count = math.ceil(self.bit_count / 8)
        if len(temp_bits) < byte_count * 8:
            temp_bits = bitarray("0" * ((byte_count * 8) - len(temp_bits))) + temp_bits
        self._bits = my_bits[: self.bit_count]
        if len(bits) >= self.bit_count:
            return bits[self.bit_count :]
        else:
            return bitarray(endian="little")

    def get_value(self) -> F:
        b = self.bits.tobytes()
        if self.endian == "little":
            return cast(F, struct.unpack("<f", b)[0])
        else:
            return cast(F, struct.unpack(">f", b)[0])

    def set_value(self, value: F) -> None:
        if self.endian == "little":
            bytes_val = bytearray(struct.pack("<f", value))
        else:
            bytes_val = bytearray(struct.pack(">f", value))
        bits = bitarray(endian="little")
        bits.frombytes(bytes_val)
        self._bits = bits

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self._bits.tobytes()

    def set_bits(self, bits: bitarray) -> None:
        if bits.endian() != Literal["little"]:
            v = bits.tobytes()
            _bits = bitarray(endian="little")
            _bits.frombytes(v)
        else:
            _bits = bits
        if len(_bits) < self.bit_count:
            _bits = _bits + bitarray("0" * (self.bit_count - len(_bits)), endian="little")
        self._bits = _bits[: self.bit_count]

    def set_children(
        self,
        children: OrderedDict[str, ParseBaseGeneric[Any]]
        | dict[str, ParseBaseGeneric[Any]]
        | list[ParseBaseGeneric[Any]]
        | None,
    ) -> None:
        raise NotImplementedError()

    def get_string_value(self) -> str:
        return self.string_format.format(self.value)


class Float32IEEField(Float32IEEFieldGeneric[float]):
    ...


class Float32Field(Float32IEEField):
    ...
