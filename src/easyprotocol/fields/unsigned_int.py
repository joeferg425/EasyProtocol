"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from collections import OrderedDict
from typing import Any, Literal
from bitarray import bitarray
from easyprotocol.base.parse_object import DEFAULT_ENDIANNESS, ParseObject
from easyprotocol.base.utils import InputT, input_to_bytes
import math

UINT_STRING_FORMAT = "{:X}(hex)"
UINT8_STRING_FORMAT = "{:02X}(hex)"
UINT16_STRING_FORMAT = "{:04X}(hex)"
UINT24_STRING_FORMAT = "{:06X}(hex)"
UINT32_STRING_FORMAT = "{:08X}(hex)"
UINT64_STRING_FORMAT = "{:016X}(hex)"


class UIntField(ParseObject[int]):
    """The base parsing object for unsigned integers."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = UINT_STRING_FORMAT,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        init_to_zero: bool = True,
    ) -> None:
        self.bit_count = bit_count
        super().__init__(
            name=name,
            data=data,
            value=value,
            fmt=format,
            endian=endian,
        )
        if self.value is None and init_to_zero is True:
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
        bit_mask = bitarray(endian="little")
        bit_mask.frombytes(
            int.to_bytes(_bit_mask, length=math.ceil(self.bit_count / 8), byteorder="little", signed=False)
        )
        if len(bit_mask) < len(bits):
            bit_mask = bit_mask + bitarray("0" * (len(bits) - len(bit_mask)), endian="little")
        elif len(bit_mask) > len(bits):
            bit_mask = bit_mask[: len(bits)]
        if len(bits) < len(bit_mask):
            raise IndexError("Too little data to parse field.")
        my_bits = (bits & bit_mask)[: self.bit_count]
        temp_bits = bitarray(my_bits, endian="little")
        byte_count = math.ceil(self.bit_count / 8)
        if len(temp_bits) < byte_count * 8:
            temp_bits = temp_bits + bitarray("0" * ((byte_count * 8) - len(temp_bits)), endian="little")
        self._bits = my_bits[: self.bit_count]
        if len(bits) >= self.bit_count:
            return bits[self.bit_count :]
        else:
            return bitarray(endian="little")

    def _get_value(self) -> int | None:
        if len(self.bits) == 0:
            return None
        b = self.bits.tobytes()
        return int.from_bytes(bytes=b, byteorder=self.endian, signed=False)

    def _set_value(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        byte_count = math.ceil(self.bit_count / 8)
        my_bytes = int.to_bytes(value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self.bit_count]

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self._bits.tobytes()

    @property
    def value(self) -> int | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: int) -> None:
        self._set_value(value)

    def _set_bits(self, bits: bitarray) -> None:
        if not bits.endian == "little":
            v = bits.tobytes()
            _bits = bitarray(endian="little")
            _bits.frombytes(v)
        else:
            _bits = bits
        if len(_bits) < self.bit_count:
            _bits = _bits + bitarray("0" * (self.bit_count - len(_bits)), endian="little")
        self._bits = _bits[: self.bit_count]

    def _set_children(self, children: OrderedDict[str, ParseObject[Any]] | list[ParseObject[Any]]) -> None:
        raise NotImplementedError()


class BoolField(UIntField):
    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: int | None = None,
        init_to_false: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=1,
            data=data,
            value=value,
            format="{}",
            endian="little",
            init_to_zero=False,
        )
        if self.value is None and init_to_false is True:
            self.value = False

    @property
    def value(self) -> bool | None:
        v = super().value
        if v is None:
            return None
        return bool(v)

    @value.setter
    def value(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        value = int(value)
        bits = bitarray(endian="little")
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[: self.bit_count]


class UInt8Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = UINT8_STRING_FORMAT,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        init_to_zero: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=8,
            format=format,
            endian=endian,
            init_to_zero=init_to_zero,
        )


class UInt16Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = UINT16_STRING_FORMAT,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        init_to_zero: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=16,
            format=format,
            endian=endian,
            init_to_zero=init_to_zero,
        )


class UInt24Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = UINT24_STRING_FORMAT,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        init_to_zero: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=24,
            format=format,
            endian=endian,
            init_to_zero=init_to_zero,
        )


class UInt32Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = UINT32_STRING_FORMAT,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        init_to_zero: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=32,
            format=format,
            endian=endian,
            init_to_zero=init_to_zero,
        )


class UInt64Field(UIntField):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: int | None = None,
        format: str | None = UINT64_STRING_FORMAT,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        init_to_zero: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=64,
            format=format,
            endian=endian,
            init_to_zero=init_to_zero,
        )
