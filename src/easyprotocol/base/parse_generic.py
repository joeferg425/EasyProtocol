"""The base parsing object for handling parsing in a convenient (to modify) package."""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Generic, Literal, Sequence, SupportsBytes, TypeVar

from bitarray import bitarray

from easyprotocol.base.utils import DEFAULT_ENDIANNESS, dataT, endianT, hex

UNDEFINED = "?UNDEFINED?"
T = TypeVar("T", bound=Any, covariant=True)


class ParseGeneric(SupportsBytes, Generic[T]):
    """The base parsing object for handling parsing in a convenient (to modify) package."""

    def __init__(
        self,
        name: str,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: bytes to be parsed
            value: value to assign to object
            fmt: python format string (e.g. "{:f}")
            parent: object to nest this one inside of
            endian: the byte endian-ness of this object
        """
        self._name: str = ""
        self._endian: endianT = endian
        self._bits: bitarray = bitarray(endian="little")
        self._bit_count: int = bit_count
        self._name = name
        self._initialized = False
        self._parent: ParseGeneric[Any] | None = None
        self._children: OrderedDict[str, ParseGeneric[Any]] = OrderedDict()
        if string_format is None:
            self._string_format = "{}"
        else:
            self._string_format = string_format
        if data is not None:
            self.parse(data=data)

    def parse(self, data: dataT) -> bitarray:
        """Parse the passed bits or bytes into meaningful data.

        Args:
            data: bits or bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        raise NotImplementedError()

    def get_name(self) -> str:
        return self._name

    def set_name(self, value: str) -> None:
        self._name = value

    def get_bits_lsb(self) -> bitarray:
        return self._bits

    def get_bits(self) -> bitarray:
        b = self.get_bits_lsb().tobytes()
        bits = bitarray(endian="big")
        bits.frombytes(b)
        if self._bit_count != -1:
            return bits[-self._bit_count :]
        else:
            return bits

    def set_bits_lsb(self, bits: bitarray) -> None:
        raise NotImplementedError()

    def _get_parent_generic(self) -> ParseGeneric[Any] | None:
        return self._parent

    def _set_parent_generic(self, parent: ParseGeneric[Any] | None) -> None:
        self._parent = parent

    def _get_children_generic(self) -> OrderedDict[str, ParseGeneric[Any]]:
        return self._children

    def _set_children_generic(
        self,
        children: OrderedDict[str, ParseGeneric[Any]] | Sequence[ParseGeneric[Any]],
    ) -> None:
        self._children.clear()
        if isinstance(children, (dict, OrderedDict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return UNDEFINED

    def get_bytes_value(self) -> bytes:
        return self.__bytes__()

    def get_hex_value(self) -> str:
        return hex(self.get_bytes_value())

    @property
    def name(self) -> str:
        """Get the name of the field.

        Returns:
            the name of the field
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def bits_lsb(self) -> bitarray:
        """Get the bit value of the field.

        Returns:
            the bit value of the field
        """
        return self.get_bits_lsb()

    @bits_lsb.setter
    def bits_lsb(self, bits: bitarray) -> None:
        self.set_bits_lsb(bits)

    @property
    def bits(self) -> bitarray:
        return self.get_bits()

    @property
    def bits_str(self) -> str:
        return f"{self.bits.to01()}:<b"

    @property
    def bits_str_lsb(self) -> str:
        return f"b>:{self.bits_lsb.to01()}"

    @property
    def string_format(self) -> str:
        """Get the format string of the field.

        Returns:
            the format string of the field
        """
        return self._string_format

    @string_format.setter
    def string_format(self, fmt: str) -> None:
        self._string_format = fmt

    @property
    def endian(self) -> Literal["little", "big"]:
        """Get the byte endianness value of this object.

        Returns:
            the byte endianness value of this object
        """
        return self._endian

    @property
    def bytes(self) -> bytes:
        """Get the byte value of this object.

        Returns:
            the byte value of this object
        """
        return self.__bytes__()

    @property
    def string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.get_string_value()

    @property
    def hex(self) -> str:
        return self.get_hex_value()

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self._bits.tobytes()

    def __str__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"{self._name}: {self.string}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"