"""Unsigned integer parsing fields."""
from __future__ import annotations

import math
from typing import Any, Generic, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_base import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.utils import dataT, input_to_bytes

UINT_STRING_FORMAT = "{:X}(hex)"
UINT08_STRING_FORMAT = "{:02X}(hex)"
UINT16_STRING_FORMAT = "{:04X}(hex)"
UINT24_STRING_FORMAT = "{:06X}(hex)"
UINT32_STRING_FORMAT = "{:08X}(hex)"
UINT64_STRING_FORMAT = "{:016X}(hex)"

T = TypeVar("T", bound=Union[Any, int])


class UIntFieldGeneric(
    ParseGenericValue[T],
    Generic[T],
):
    """Base unsigned integer parsing class."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        default: T = 0,
        data: dataT = None,
        string_format: str = UINT_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create base unsigned integer parsing field.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            default=default,
            bit_count=bit_count,
            data=data,
            string_format=string_format,
            endian=endian,
        )

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field

        Raises:
            IndexError: if there is too little data to parse this field
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
        if len(bits) < len(bit_mask) or len(bits) == 0 or len(bits) < self._bit_count:
            raise IndexError("Too little data to parse field.")
        my_bits = (bits & bit_mask)[: self._bit_count]
        self._bits = my_bits[: self._bit_count]
        if len(bits) >= self._bit_count:
            return bits[self._bit_count :]
        else:
            return bitarray(endian="little")

    def get_value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        _bits = self.bits_lsb
        m = len(_bits) % 8
        if m != 0:
            bits = _bits + bitarray([False] * (8 - m))
        else:
            bits = _bits
        b = bits.tobytes()
        return cast(T, int.from_bytes(bytes=b, byteorder=self.endian, signed=False))

    def set_value(self, value: T) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        if value is None:
            _value = 0
        elif isinstance(value, ParseGenericValue):
            _value = int(cast(ParseGenericValue[T], value).value)
        elif not isinstance(value, int):
            _value = int(value)
        else:
            _value = value
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]

    def get_string_value(self) -> str:
        """Get the string value of this field.

        Returns:
            the string value of this field
        """
        return self._string_format.format(self.value)

    @property
    def value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: T) -> None:
        self.set_value(value)

    def set_bits_lsb(self, bits: bitarray) -> None:
        """Set the bits of this field in least-significant-bit first format.

        Args:
            bits: lsb bits
        """
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


class UIntField(UIntFieldGeneric[int]):
    """Unsigned integer parsing class."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = UINT_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create unsigned integer parsing class.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            default=default,
            data=data,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
        )


class BoolField(UIntFieldGeneric[bool]):
    """Boolean parsing class."""

    def __init__(
        self,
        name: str,
        default: bool = False,
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        """Create boolean parsing class.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        super().__init__(
            name=name,
            bit_count=1,
            data=data,
            default=default,
            string_format=string_format,
            endian="little",
        )

    @property
    def value(self) -> bool:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return bool(super().value)

    @value.setter
    def value(self, value: bool) -> None:
        _value = int(value)
        bits = bitarray(endian="little")
        byte_count = math.ceil(self._bit_count / 8)
        bits.frombytes(int.to_bytes(_value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[: self._bit_count]


class UInt8Field(UIntField):
    """Unsigned eight bit integer parsing class."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = UINT08_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Unsigned eight bit integer parsing class.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=8,
            string_format=string_format,
            endian=endian,
        )


class UInt16Field(UIntField):
    """Unsigned sixteen bit integer parsing class."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = UINT16_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Unsigned sixteen bit integer parsing class.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=16,
            string_format=string_format,
            endian=endian,
        )


class UInt24Field(UIntField):
    """Unsigned twenty-four bit integer parsing class."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = UINT24_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Unsigned twenty-four bit integer parsing class.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=24,
            string_format=string_format,
            endian=endian,
        )


class UInt32Field(UIntField):
    """Unsigned thirty-two bit integer parsing class."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = UINT32_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Unsigned thirty-two bit integer parsing class.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=32,
            string_format=string_format,
            endian=endian,
        )


class UInt64Field(UIntField):
    """Unsigned sixty-four bit integer parsing class."""

    def __init__(
        self,
        name: str,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = UINT64_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Unsigned sixty-four bit integer parsing class.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            data=data,
            default=default,
            bit_count=64,
            string_format=string_format,
            endian=endian,
        )
