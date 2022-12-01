from __future__ import annotations

import math
from collections import OrderedDict
from typing import Generic, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.parse_value_generic import ParseValueGeneric
from easyprotocol.base.utils import dataT, hex
from easyprotocol.fields.array import ParseArrayField
from easyprotocol.fields.unsigned_int import UIntField, UIntFieldGeneric

DEFAULT_CHAR_FORMAT = '"{}"'
DEFAULT_STRING_FORMAT = '"{}"'
DEFAULT_BYTE_FORMAT = '"{}"(byte)'
DEFAULT_BYTES_FORMAT = '"{}"(bytes)'


class CharField(UIntFieldGeneric[str]):
    def __init__(
        self,
        name: str,
        default: str = "\x00",
        data: dataT | None = None,
        string_format: str = '"{}"',
        string_encoding: str = "latin1",
    ) -> None:
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
        b = bytes(self)
        s = b.decode(self._string_encoding)
        return s

    def set_value(self, value: str) -> None:
        _value = ord(value[0])
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]


class StringField(ParseArrayField[str]):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: dataT | None = None,
        string_format: str = '"{}"',
        string_encoding: str = "latin1",
    ) -> None:
        self._string_encoding: str = string_encoding
        super().__init__(
            name=name,
            count=count,
            array_item_class=CharField,
            data=data,
            string_format=string_format,
        )

    def get_value(self) -> str:  # pyright:ignore[reportIncompatibleMethodOverride]
        return "".join([v.value for v in self.children.values()])

    def set_value(self, value: str) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
        if value is None:
            return
        for index, item in enumerate(value):
            if index < len(self._children):
                kid = cast(CharField, self[index])
                kid.value = item
            else:
                f = self.array_item_class(f"#{index}")
                f.value = item
                self._children[f.name] = f

    @property
    def value(self) -> str:  # pyright:ignore[reportIncompatibleMethodOverride]
        return self.get_value()

    @value.setter
    def value(self, value: str) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
        self.set_value(value=value)

    def get_string_value(self) -> str:
        return self._string_format.format(self.value)


class ByteField(UIntFieldGeneric[bytes]):
    def __init__(
        self,
        name: str,
        default: bytes = b"\x00",
        data: dataT | None = None,
        string_format: str = '"{}"(bytes)',
    ) -> None:
        super().__init__(
            name=name,
            bit_count=8,
            data=data,
            default=default,
            endian=DEFAULT_ENDIANNESS,
            string_format=string_format,
        )

    def get_value(self) -> bytes:
        return self.bytes

    @property
    def value(self) -> bytes:
        return self.get_value()

    @value.setter
    def value(self, value: int | str | bytes | None) -> None:
        if not isinstance(value, (bytes, str)):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        value = int(value[0])
        bits = bitarray(endian="little")
        byte_count = math.ceil(self._bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[: self._bit_count]

    def set_value(self, value: bytes) -> None:
        _value = value[0]
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]

    def get_string_value(self) -> str:
        return self._string_format.format(self.hex)


class BytesField(ParseArrayField[bytes]):
    def __init__(
        self, name: str, count: UIntField | int, data: dataT | None = None, string_format: str = '"{}"(bytes)'
    ) -> None:
        super().__init__(
            name=name,
            count=count,
            array_item_class=ByteField,
            data=data,
            string_format=string_format,
        )

    def get_value(self) -> bytes:  # pyright:ignore[reportIncompatibleMethodOverride]
        return b"".join([v.value for v in self.children.values()])

    def set_value(self, value: bytes) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
        for index, item in enumerate(value):
            if index < len(self._children):
                kid = cast(ByteField, self[index])
                kid.value = item
            else:
                f = self.array_item_class(f"#{index}")
                f.value = bytes([item])
                self._children[f.name] = f

    def get_string_value(self) -> str:
        return self.string_format.format(self.get_hex_value())
