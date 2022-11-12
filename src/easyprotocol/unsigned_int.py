"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
import struct
from easyprotocol.parse_object import ParseObject


class UInt8(ParseObject[int]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | None = None,
        value: int | None = None,
    ) -> None:
        if data is None and value is None:
            value = 0
        super().__init__(
            name=name,
            data=data,
            value=value,
        )

    def parse(self, data: bytes) -> bytes:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        self._data = bytes([data[0]])
        self._value = struct.unpack("B", self._data)[0]
        return data[1:]

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        if value < 0 or value > 0xFF:
            raise ValueError(f"{self.__class__.__name__} cannot be assigned value {value}")
        self._value = value
        self._data = struct.pack("B", value)


class UInt16(ParseObject[int]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | None = None,
        value: int | None = None,
    ) -> None:
        if data is None and value is None:
            value = 0
        super().__init__(
            name=name,
            data=data,
            value=value,
        )

    def parse(self, data: bytes) -> bytes:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        self._data = data[:2]
        self._value = struct.unpack("!H", self._data)[0]
        return data[2:]

    @property
    def value(self) -> int:
        return super().value

    @value.setter
    def value(self, value: int) -> None:
        if value < 0 or value > 0xFFFF:
            raise ValueError(f"{self.__class__.__name__} cannot be assigned value {value}")
        self._value = value
        self._data = struct.pack("!H", value)


class UInt32(ParseObject[int]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | None = None,
        value: int | None = None,
    ) -> None:
        if data is None and value is None:
            value = 0
        super().__init__(
            name=name,
            data=data,
            value=value,
        )

    def parse(self, data: bytes) -> bytes:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        self._data = data[:4]
        self._value = struct.unpack("!I", self._data)[0]
        return data[4:]

    @property
    def value(self) -> int:
        return super().value

    @value.setter
    def value(self, value: int) -> None:
        if value < 0 or value > 0xFFFFFFFF:
            raise ValueError(f"{self.__class__.__name__} cannot be assigned value {value}")
        self._value = value
        self._data = struct.pack("!I", value)


class UInt64(ParseObject[int]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | None = None,
        value: int | None = None,
    ) -> None:
        if data is None and value is None:
            value = 0
        super().__init__(
            name=name,
            data=data,
            value=value,
        )

    def parse(self, data: bytes) -> bytes:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        self._data = data[:8]
        self._value = struct.unpack("!Q", self._data)[0]
        return data[8:]

    @property
    def value(self) -> int:
        return super().value

    @value.setter
    def value(self, value: int) -> None:
        if value < 0 or value > 0xFFFFFFFFFFFFFFFF:
            raise ValueError(f"{self.__class__.__name__} cannot be assigned value {value}")
        self._value = value
        self._data = struct.pack("!Q", value)
