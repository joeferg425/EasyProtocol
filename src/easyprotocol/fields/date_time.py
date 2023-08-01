"""Date and time related fields."""
from __future__ import annotations

import math
from datetime import datetime

from bitarray import bitarray

from easyprotocol.base.base import DEFAULT_ENDIANNESS, BaseField, endianT
from easyprotocol.base.utils import dataT, input_to_bytes
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

DATE_FIELD_STRING_FORMAT = "{}"
DATE_STRING_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class DateTimeField(
    UIntFieldGeneric[datetime],
    BaseField,
):
    """Time as seconds since 1970."""

    def __init__(
        self,
        name: str,
        default: datetime | int | None = None,
        data: dataT | None = None,
        string_format: str = "{}",
        date_string_format: str = DATE_STRING_FORMAT,
        utc: bool = True,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Get time as seconds since 1970.

        Args:
            name: name of field
            default: default value.
            data: data to parse.
            string_format: string format. Defaults to "{}".
            date_string_format: the date string format
            utc: the uts setting for the timestamp
            endian: Defaults to DEFAULT_ENDIANNESS.
        """
        self._utc = utc
        self._date_string_format = date_string_format
        if default is None:
            if self.utc:
                default = datetime.utcfromtimestamp(0)
            else:
                default = datetime.fromtimestamp(0)
        elif isinstance(default, int):
            if self.utc:
                default = datetime.utcfromtimestamp(default)
            else:
                default = datetime.fromtimestamp(default)
        super().__init__(
            name=name,
            bit_count=32,
            default=default,
            data=data,
            string_format=string_format,
            endian=endian,
        )

    def set_value(self, value: datetime) -> None:
        """Set field value.

        Args:
            value: datetime value
        """
        if self.utc:
            _value = int((value - datetime.utcfromtimestamp(0)).total_seconds())
        else:
            _value = int((value - datetime.fromtimestamp(0)).total_seconds())
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]

    def get_value(self) -> datetime:
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
        i = int.from_bytes(bytes=b, byteorder=self.endian, signed=True)
        if self.utc:
            date = datetime.utcfromtimestamp(i)
        else:
            date = datetime.fromtimestamp(i)
        return date

    def get_value_as_string(self) -> str:
        """Get the string value of this field.

        Returns:
            the string value of this field
        """
        return self._string_format.format(self.value.strftime(self._date_string_format))

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
            raise IndexError(f"Too little data to parse field ({self.chain}).")
        my_bits = (bits & bit_mask)[: self._bit_count]
        self._bits = my_bits[: self._bit_count]
        if len(bits) >= self._bit_count:
            return bits[self._bit_count :]
        else:
            return bitarray(endian="little")

    @property
    def date_string_format(self) -> str:
        """Get the date string format.

        Returns:
            the date string format
        """
        return self._date_string_format

    @date_string_format.setter
    def date_string_format(self, value: str) -> None:
        """Set the date string format.

        Args:
            value: the date string format
        """
        self._date_string_format = value

    @property
    def utc(self) -> bool:
        """Get the utc setting.

        Returns:
            the utc setting
        """
        return self._utc

    @utc.setter
    def utc(self, value: bool) -> None:
        """Set the utc setting.

        Args:
            value: the utc setting
        """
        self._utc = value
