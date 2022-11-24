from __future__ import annotations

import math

from bitarray import bitarray

from easyprotocol.base.parse_object import DEFAULT_ENDIANNESS, ParseObject
from easyprotocol.base.utils import InputT, hex
from easyprotocol.fields.array import ArrayField
from easyprotocol.fields.unsigned_int import UInt8Field, UIntField

DEFAULT_CHAR_FORMAT = '"{}"'
DEFAULT_STRING_FORMAT = '"{}"'
DEFAULT_BYTE_FORMAT = '"{}"(byte)'
DEFAULT_BYTES_FORMAT = '"{}"(bytes)'


class CharField(UInt8Field):
    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: str | bytes | None = None,
        format: str | None = DEFAULT_CHAR_FORMAT,
        string_encoding: str = "latin1",
        init_to_zero: bool = True,
    ) -> None:
        self._string_encoding = string_encoding
        super().__init__(
            name=name,
            data=data,
            value=value,
            format=format,
            endian=DEFAULT_ENDIANNESS,
            init_to_zero=False,
        )
        if self.value is None and init_to_zero is True:
            self.value = "\x00"

    def _get_value(self) -> str | None:
        if len(self.bits) == 0:
            return None
        return bytes(self).decode(self._string_encoding)

    def _set_value(self, value: str | bytes) -> None:
        if not isinstance(value, (bytes, str)):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        if isinstance(value, str):
            _value = ord(value[0])
        else:
            _value = value[0]
        super()._set_value(_value)

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.fmt.format(self.value)


class StringField(ArrayField):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: InputT | None = None,
        value: str | None = None,
        format: str = DEFAULT_STRING_FORMAT,
    ) -> None:
        super().__init__(
            name=name,
            count=count,
            array_item_class=CharField,
            data=data,
            parent=None,
            children=None,
            format=format,
        )
        if len(self.value) == 0 and value is not None:
            self.value = value

    def _get_value(self) -> str | None:
        return "".join([v.value for v in self._children.values()])

    def _set_value(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
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

    @property
    def value(self) -> str | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: str) -> None:
        self._set_value(value=value)

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.fmt.format(self.value)


class ByteField(UInt8Field):
    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: bytes | None = None,
        format: str | None = DEFAULT_BYTE_FORMAT,
        init_to_zero: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            format=format,
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
    def value(self, value: str | bytes) -> None:
        if not isinstance(value, (bytes, str)):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        value = int(value[0])
        bits = bitarray(endian="little")
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[: self.bit_count]

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.fmt.format(hex(self.value))

    def _set_value(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        if isinstance(value, str):
            _value = ord(value[0])
        else:
            _value = value[0]
        super()._set_value(_value)

    @property
    def value(self) -> bytes | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        b = self._get_value()
        if b is None:
            return None
        return bytes([b])

    @value.setter
    def value(self, value: bytes) -> None:
        self._set_value(value=value)


class BytesField(ArrayField):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: InputT | None = None,
        value: bytes | None = None,
        format: str = DEFAULT_BYTES_FORMAT,
    ) -> None:
        super().__init__(
            name=name,
            count=count,
            array_item_class=ByteField,
            data=data,
            parent=None,
            children=None,
            format=format,
        )
        if len(self.value) == 0 and value is not None:
            self.value = value

    def _get_value(self) -> bytes | None:
        return b"".join([v.value for v in self._children.values()])

    def _set_value(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
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
                    f.value = bytes([item])
                    self.append(f)

    @property
    def value(self) -> bytes | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: bytes) -> None:
        self._set_value(value=value)

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.fmt.format(hex(self.value))
