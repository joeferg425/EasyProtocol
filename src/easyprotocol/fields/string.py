"""String and bytes parsing fields."""
from __future__ import annotations

import math
import struct

from bitarray import bitarray

from easyprotocol.base.base import DEFAULT_ENDIANNESS, BaseField
from easyprotocol.base.utils import dataT, input_to_bitarray
from easyprotocol.base.value import ValueFieldGeneric
from easyprotocol.fields.unsigned_int import UIntField, UIntFieldGeneric

DEFAULT_CHAR_FORMAT: str = "{}"
DEFAULT_STRING_FORMAT: str = "{}"
DEFAULT_BYTE_FORMAT: str = '"{}"(byte)'
DEFAULT_BYTES_FORMAT: str = '"{}"(bytes)'


class CharField(
    UIntFieldGeneric[str],
    BaseField,
):
    """Single ASCII character field."""

    def __init__(
        self,
        name: str,
        default: str = "\x00",
        data: dataT | None = None,
        string_format: str = "{}",
        string_encoding: str = "latin1",
    ) -> None:
        """Create eight-bit character field.

        Defaults to ASCII (latin1) decoding.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            string_encoding: encoding for bytes to string conversion (e.g. 'latin1' or 'utf-8'),
        """
        self._string_encoding: str = string_encoding
        super().__init__(
            name=name,
            bit_count=8,
            data=data,
            default=default,
            endian=DEFAULT_ENDIANNESS,
            string_format=string_format,
        )

    def get_value(self) -> str:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        b = bytes(self)
        s = b.decode(self._string_encoding)
        return s

    def set_value(self, value: str) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        _value = ord(value[0])
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]

    def __str__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f'{self._name}: "{self.value_as_string}"'


class UInt8CharField(
    CharField,
    BaseField,
):
    """Single ASCII character field."""

    ...


class StringField(
    ValueFieldGeneric[str],
    BaseField,
):
    """String parsing field."""

    def __init__(
        self,
        name: str,
        byte_count: UIntField | int = 0,
        data: dataT | None = None,
        string_format: str = "{}",
        string_encoding: str = "latin1",
        default: str = "",
    ) -> None:
        """Create string parsing field.

        Args:
            name: name of parsed object
            default: the default value for this class
            byte_count: the number of bytes in this field
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            string_encoding: encoding for bytes to string conversion (e.g. 'latin1' or 'utf-8'),
        """
        self._string_encoding: str = string_encoding
        self._byte_count = byte_count
        super().__init__(
            name=name,
            default=default,
            data=data,
            string_format=string_format,
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
        if isinstance(self._byte_count, UIntFieldGeneric):
            self._bit_count = self._byte_count.value * 8
        else:
            self._bit_count = self._byte_count * 8
        bits = input_to_bitarray(
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
            raise IndexError(f"Too little data to parse field ({self.chain}).")
        my_bits = (bits & bit_mask)[: self._bit_count]
        self._bits = my_bits[: self._bit_count]
        if len(bits) >= self._bit_count:
            return bits[self._bit_count :]
        else:
            return bitarray(endian="little")

    def get_value(self) -> str:
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
        return b.decode(self._string_encoding)

    def set_value(self, value: str) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        my_bytes = value.encode()
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]

    def get_value_concatenated(self) -> str:
        """Get list values as a single concatenated value (if supported).

        Returns:
            list values as a single concatenated value (if supported)
        """
        return self.value

    def get_value_as_string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        s = self.get_value()
        return self.string_format.format(s)

    def __str__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f'{self._name}: "{self.value_as_string}"'


class ByteField(
    UIntFieldGeneric[bytes],
    BaseField,
):
    """Single byte field that returns bytes object instead of int."""

    def __init__(
        self,
        name: str,
        default: bytes = b"\x00",
        data: dataT | None = None,
        string_format: str = '"{}"(bytes)',
    ) -> None:
        """Single byte field that returns bytes object instead of int.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        super().__init__(
            name=name,
            bit_count=8,
            data=data,
            default=default,
            endian=DEFAULT_ENDIANNESS,
            string_format=string_format,
        )

    def get_value(self) -> bytes:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        return self.value_as_bytes

    @property
    def value(self) -> bytes:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        return self.get_value()

    @value.setter
    def value(self, value: int | str | bytes) -> None:
        self.set_value(value)

    def set_value(self, value: int | str | bytes) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        if isinstance(value, bytes):
            _value = value[0]
        elif isinstance(value, str):
            _value = struct.pack("s", value[0])[0]
        else:
            _value = int(value)
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]

    def get_value_as_string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self._string_format.format(self.value.decode("latin1"))


class UInt8ByteField(
    ByteField,
    BaseField,
):
    """Single byte field that returns bytes object instead of int."""

    ...


class BytesField(
    ValueFieldGeneric[bytes],
    BaseField,
):
    """Variable length bytes field that returns bytes."""

    def __init__(
        self,
        name: str,
        byte_count: UIntField | int,
        default: bytes = b"",
        data: dataT | None = None,
        string_format: str = '"{}"(bytes)',
    ) -> None:
        """Create variable length bytes field that returns bytes.

        Args:
            name: name of parsed object
            default: the default value for this class
            byte_count: the number of bytes in this field
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        self._byte_count = byte_count
        super().__init__(
            name=name,
            default=default,
            data=data,
            string_format=string_format,
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
        if isinstance(self._byte_count, UIntFieldGeneric):
            self._bit_count = self._byte_count.value * 8
        else:
            self._bit_count = self._byte_count * 8
        bits = input_to_bitarray(
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
            raise IndexError(f"Too little data to parse field ({self.chain}).")
        my_bits = (bits & bit_mask)[: self._bit_count]
        self._bits = my_bits[: self._bit_count]
        if len(bits) >= self._bit_count:
            return bits[self._bit_count :]
        else:
            return bitarray(endian="little")

    def get_value(self) -> bytes:
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
        return bits.tobytes()

    def set_value(self, value: bytes) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        bits = bitarray(endian="little")
        bits.frombytes(value)
        self._bits = bits[: self._bit_count]

    def get_value_concatenated(self) -> bytes:
        """Get list values as a single concatenated value (if supported).

        Returns:
            list values as a single concatenated value (if supported)
        """
        return self.value

    def get_value_as_string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        s = self.get_value().decode("latin1")
        return self.string_format.format(s)
