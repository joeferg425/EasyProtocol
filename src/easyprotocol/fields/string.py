from __future__ import annotations

import math
from collections import OrderedDict
from typing import Generic, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_base import DEFAULT_ENDIANNESS, ParseBaseGeneric
from easyprotocol.base.utils import dataT, hex
from easyprotocol.fields.array import ArrayField
from easyprotocol.fields.unsigned_int import UIntField, UIntFieldGeneric

DEFAULT_CHAR_FORMAT = '"{}"'
DEFAULT_STRING_FORMAT = '"{}"'
DEFAULT_BYTE_FORMAT = '"{}"(byte)'
DEFAULT_BYTES_FORMAT = '"{}"(bytes)'


class CharField(UIntFieldGeneric[str]):
    def __init__(
        self,
        name: str,
        data: dataT | None = None,
        value: str | None = None,
        string_encoding: str = "latin1",
        init_to_zero: bool = True,
    ) -> None:
        self._string_encoding: str = string_encoding
        super().__init__(
            name=name,
            bit_count=8,
            data=data,
            value=value,
            endian=DEFAULT_ENDIANNESS,
            init_to_zero=False,
        )
        if self.value is None and init_to_zero is True:
            self.value = "\x00"

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


class StringField(ArrayField[str]):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: dataT | None = None,
        value: str | None = None,
        string_encoding: str = "latin1",
    ) -> None:
        self._string_encoding: str = string_encoding
        super().__init__(
            name=name,
            count=count,
            array_item_class=CharField,
            data=data,
            parent=None,
            children=None,
        )
        if self.value is not None and len(self.value) == 0 and value is not None:
            self.value = value

    def get_string(self) -> str:
        return "".join([(v.value if v.value is not None else "\x00") for v in self._children.values()])

    def set_string(self, value: str) -> None:
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
    def value_string(self) -> str:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_string()

    @value_string.setter
    def value(self, value: str) -> None:
        self.set_string(value=value)

    @property
    def string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'"{self.value}"'


class ByteField(UIntFieldGeneric[bytes]):
    def __init__(
        self,
        name: str,
        data: dataT | None = None,
        value: bytes | None = None,
        init_to_zero: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=8,
            data=data,
            value=value,
            endian=DEFAULT_ENDIANNESS,
            init_to_zero=False,
        )
        if value is None and data is None and init_to_zero is True:
            self.value = b"\x00"

    @property
    def value(self) -> bytes:
        return self.bytes

    @value.setter
    def value(self, value: int | str | bytes | None) -> None:
        if not isinstance(value, (bytes, str)):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        value = int(value[0])
        bits = bitarray(endian="little")
        byte_count = math.ceil(self._bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[: self._bit_count]

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        h = hex(self.value if self.value is not None else b"\x00")
        return f'"{h}"'

    def set_value(self, value: bytes) -> None:
        _value = value[0]
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]


class BytesField(ArrayField[bytes]):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: dataT | None = None,
        value: bytes | None = None,
    ) -> None:
        super().__init__(
            name=name,
            count=count,
            array_item_class=ByteField,
            data=data,
            parent=None,
            children=None,
        )
        if value is not None and data is None:
            self.value = value

    def get_string(self) -> bytes:
        return b"".join([(v.value if v.value is not None else b"\x00") for v in self._children.values()])

    def set_string(self, value: bytes) -> None:
        if value is None:
            return
        for index, item in enumerate(value):
            if isinstance(item, ParseBaseGeneric):
                if index < len(self._children):
                    kid = cast(ByteField, self[index])
                    kid.value = item
                    item.parent = self
                else:
                    self._children[item.name] = item
                    item.parent = self
            else:
                if index < len(self._children):
                    kid = cast(ByteField, self[index])
                    kid.value = item
                else:
                    f = self.array_item_class(f"#{index}")
                    f.value = bytes([item])
                    self._children[f.name] = f

    @property
    def string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        h = hex(self.value)
        return f'"{h}"'
