"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from easyprotocol.parse_object import ParseObject
import math
from bitarray import bitarray


class Uint(ParseObject[int]):
    """The base parsing object for unsigned integers."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        self.bit_count = bit_count
        super().__init__(
            name=name,
            data=data,
            value=value,
        )
        if self.value is None:
            self.value = 0

    def parse(self, data: bytes | bitarray) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed
        """
        if isinstance(data, bytes):
            bits = bitarray()
            bits.frombytes(data)
        else:
            bits = bitarray(data)
        if len(bits) < self.bit_count:
            bits = bitarray("0" * (self.bit_count - len(bits))) + bits
        self._bits = bits[: self.bit_count]
        my_bytes = self._bits.tobytes()
        self._value = int.from_bytes(my_bytes, byteorder="big", signed=False)

        return bits[self.bit_count :]  # noqa

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Can't assign value {value} to {self.__class__.__name__}")
        bits = bitarray()
        byte_count = math.ceil(self.bit_count / 8)
        bits.frombytes(int.to_bytes(value, length=byte_count, byteorder="big", signed=False))
        self._bits = bits
        self._value = value


class UInt8(Uint):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=8,
        )


class UInt16(Uint):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=16,
        )


class UInt24(Uint):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=24,
        )


class UInt32(Uint):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=32,
        )


class UInt64(Uint):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            value=value,
            bit_count=64,
        )
