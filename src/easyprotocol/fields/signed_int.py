"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

import math
from typing import Any, Generic, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.utils import dataT, input_to_bytes

INT_STRING_FORMAT = "{}"
INT08_STRING_FORMAT = "{}"
INT16_STRING_FORMAT = "{}"
INT24_STRING_FORMAT = "{}"
INT32_STRING_FORMAT = "{}"
INT64_STRING_FORMAT = "{}"

_T = TypeVar("_T", bound=Union[Any, int])


class IntFieldGeneric(
    ParseGenericValue[_T],
    Generic[_T],
):
    """The base parsing object for unsigned integers."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        default: _T = 0,
        data: dataT = None,
        string_format: str = INT_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            default=default,
            bit_count=bit_count,
            data=data,
            string_format=string_format,
            endian=endian,
        )

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        bits = input_to_bytes(
            data=data,
            bit_count=self._bit_count,
        )
        _bit_mask = (2**self._bit_count) - 1
        bit_mask = bitarray(endian="little")
        bit_mask.frombytes(
            int.to_bytes(_bit_mask, length=math.ceil(self._bit_count / 8), byteorder="little", signed=False)
        )
        if len(bit_mask) < len(bits):
            bit_mask = bit_mask + bitarray("0" * (len(bits) - len(bit_mask)), endian="little")
        elif len(bit_mask) > len(bits):
            bit_mask = bit_mask[: len(bits)]
        if len(bits) < len(bit_mask) or len(bits) == 0:
            raise IndexError("Too little data to parse field.")
        my_bits = (bits & bit_mask)[: self._bit_count]
        self._bits = my_bits[: self._bit_count]
        if len(bits) >= self._bit_count:
            return bits[self._bit_count :]
        else:
            return bitarray(endian="little")

    def get_value(self) -> _T:
        _bits = self.bits_lsb
        m = len(_bits) % 8
        if m != 0:
            bits = _bits + bitarray([False] * (8 - m))
        else:
            bits = _bits
        b = bits.tobytes()
        return cast(_T, int.from_bytes(bytes=b, byteorder=self.endian, signed=True))

    def set_value(self, value: _T) -> None:
        if value is None:
            _value = 0
        elif not isinstance(value, int):
            _value = int(value)
        else:
            _value = value
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=True)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]

    def get_string_value(self) -> str:
        return self._string_format.format(self.value)

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self._bits.tobytes()

    @property
    def value(self) -> _T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: _T) -> None:
        self.set_value(value)

    def set_bits_lsb(self, bits: bitarray) -> None:
        if bits.endian() != "little":
            m = len(bits) % 8
            if m != 0:
                bits = bitarray([False] * (8 - m)) + bits
            v = bits.tobytes()
            _bits = bitarray(endian="little")
            _bits.frombytes(v)
        else:
            _bits = bits
        if len(_bits) < self._bit_count:
            _bits = _bits + bitarray("0" * (self._bit_count - len(_bits)), endian="little")
        self._bits = _bits[: self._bit_count]


class IntField(IntFieldGeneric[int]):
    def __init__(
        self,
        name: str,
        bit_count: int,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = INT_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            default=default,
            data=data,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
        )


class Int8Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = INT08_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=8,
            string_format=string_format,
            endian=endian,
        )


class Int16Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = INT16_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=16,
            string_format=string_format,
            endian=endian,
        )


class Int24Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = INT24_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=24,
            string_format=string_format,
            endian=endian,
        )


class Int32Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = INT32_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=32,
            string_format=string_format,
            endian=endian,
        )


class Int64Field(IntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = INT64_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=64,
            string_format=string_format,
            endian=endian,
        )
