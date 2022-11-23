from __future__ import annotations
from easyprotocol.fields.unsigned_int import UInt8Field, UIntField
from easyprotocol.fields.array import ArrayField
from easyprotocol.base.utils import InputT
from bitarray import bitarray
import math


class CharField(UInt8Field):
    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: str | bytes | None = None,
        format: str | None = "{}",
        string_encoding: str = "latin1",
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            format=format,
            endian="little",
        )
        self._string_encoding = string_encoding

    @property
    def value(self) -> str | None:
        if len(self.bits) == 0:
            return None
        return bytes(self).decode(self._string_encoding)

    @value.setter
    def value(self, value: str | bytes) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        value = int(value[0])
        bits = bitarray(endian="little")
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[: self.bit_count]


class StringField(ArrayField):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: InputT | None = None,
    ) -> None:
        super().__init__(
            name=name,
            count=count,
            array_item_class=CharField,
            data=data,
            parent=None,
            children=None,
        )

    def _get_value(self) -> str | None:
        return "".join([v.value for v in self._children.values()])

    @property
    def value(self) -> str | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        self._get_value()

    @value.setter
    def value(self, value: str) -> None:
        self._set_value(value=value)


class ByteField(UInt8Field):
    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: bytes | None = None,
        format: str | None = "{}",
        string_encoding: str = "latin1",
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            format=format,
            endian="little",
        )
        self._string_encoding = string_encoding

    @property
    def value(self) -> bytes | None:
        if len(self.bits) == 0:
            return None
        return bytes(self)

    @value.setter
    def value(self, value: str | bytes) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        value = int(value[0])
        bits = bitarray(endian="little")
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder=self._endian, signed=False))
        self._bits = bits[: self.bit_count]


class BytesField(ArrayField):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        data: InputT | None = None,
    ) -> None:
        super().__init__(
            name=name,
            count=count,
            array_item_class=ByteField,
            data=data,
            parent=None,
            children=None,
        )

    def _get_value(self) -> bytes | None:
        return "".join([v.value for v in self._children.values()])

    @property
    def value(self) -> bytes | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        self._get_value()

    @value.setter
    def value(self, value: bytes) -> None:
        self._set_value(value=value)
