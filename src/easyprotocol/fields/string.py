from __future__ import annotations

import math
from typing import Generic

from bitarray import bitarray

from easyprotocol.base.parse_object import DEFAULT_ENDIANNESS, ParseObject, T
from easyprotocol.base.utils import I, hex
from easyprotocol.fields.array import ArrayFieldGeneric
from easyprotocol.fields.unsigned_int import UIntField, UIntFieldGeneric

DEFAULT_CHAR_FORMAT = '"{}"'
DEFAULT_STRING_FORMAT = '"{}"'
DEFAULT_BYTE_FORMAT = '"{}"(byte)'
DEFAULT_BYTES_FORMAT = '"{}"(bytes)'


class CharField(UIntFieldGeneric[str]):
    def __init__(
        self,
        name: str,
        data: I | None = None,
        value: str | bytes | int | None = None,
        string_encoding: str = "latin1",
        init_to_zero: bool = True,
    ) -> None:
        self._string_encoding: str = string_encoding
        super().__init__(
            name=name,
            bit_count=8,
            data=data,
            value=value,  # type:ignore
            endian=DEFAULT_ENDIANNESS,
            init_to_zero=False,
        )
        if self.value is None and init_to_zero is True:
            self.value = "\x00"

    def _get_value(self) -> str | None:
        if len(self.bits) == 0:
            return None
        b = bytes(self)
        s = b.decode(self._string_encoding)
        return s

    def _set_value(self, value: str | bytes | int | None) -> None:
        if not isinstance(value, (bytes, str, int)):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        if isinstance(value, str):
            _value = ord(value[0])
        elif isinstance(value, bytes):
            _value = value[0]
        else:
            _value = value
        super()._set_value(_value)

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'"{self.value}"'


class StringField(ArrayFieldGeneric[str]):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: I | None = None,
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

    def _get_value(self) -> str:  # type:ignore
        return "".join([(v.value if v.value is not None else "\x00") for v in self._children.values()])

    def _set_value(self, value: str | None) -> None:  # type:ignore
        if value is None:
            return
        for index, item in enumerate(value):
            if isinstance(item, ParseObject):
                if index < len(self._children):
                    self[index] = item
                    item.parent = self
                else:
                    self.append(item)
                    item.parent = self
            else:
                if index < len(self._children):
                    parse_object = self[index]
                    parse_object.value = item
                else:
                    f = self.array_item_class(f"#{index}")
                    f.value = item
                    self.append(f)

    @property  # type:ignore
    def value(self) -> str:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: str | None) -> None:
        self._set_value(value=value)

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'"{self.value}"'


class ByteField(UIntFieldGeneric[bytes]):
    def __init__(
        self,
        name: str,
        data: I | None = None,
        value: bytes | int | None = None,
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
        if self.value is None and init_to_zero is True:
            self.value = b"\x00"

    @property
    def value(self) -> bytes | None:
        if len(self.bits) == 0:
            return None
        return bytes(self)

    @value.setter
    def value(self, value: int | str | bytes | None) -> None:
        if not isinstance(value, (bytes, str)):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        value = int(value[0])
        bits = bitarray(endian="little")
        byte_count = math.ceil(self._bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[: self._bit_count]

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        h = hex(self.value if self.value is not None else b"\x00")
        return f'"{h}"'

    def _set_value(self, value: int | bytes | str | None) -> None:
        if not isinstance(value, bytes):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        if isinstance(value, str):
            _value = ord(value[0])
        else:
            _value = value[0]
        super()._set_value(_value)


class BytesField(ArrayFieldGeneric[bytes]):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: I | None = None,
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
        if self.value is not None and len(self.value) == 0 and value is not None:
            self.value = value

    def _get_value(self) -> bytes:  # type:ignore
        return b"".join([(v.value if v.value is not None else b"\x00") for v in self._children.values()])

    def _set_value(self, value: bytes | None) -> None:  # type:ignore
        if value is None:
            return
        for index, item in enumerate(value):
            if isinstance(item, ParseObject):
                if index < len(self._children):
                    self[index] = item
                    item.parent = self
                else:
                    self.append(item)
                    item.parent = self
            else:
                if index < len(self._children):
                    parse_object = self[index]
                    parse_object.value = item  # type:ignore
                else:
                    f = self.array_item_class(f"#{index}")
                    f.value = bytes([item])
                    self.append(f)

    @property  # type:ignore
    def value(self) -> bytes:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: bytes | None) -> None:
        self._set_value(value=value)

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        h = hex(self.value)
        return f'"{h}"'
