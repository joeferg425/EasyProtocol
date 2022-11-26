"""The base parsing object for handling parsing in a convenient (to modify) package."""
from __future__ import annotations

from collections import OrderedDict
from enum import Enum
from typing import Any, Generic, Literal, SupportsBytes, TypeVar, Union

from bitarray import bitarray

from easyprotocol.base.utils import I

DEFAULT_ENDIANNESS: Literal["big", "little"] = "little"
T = TypeVar("T", bound=Union[Any, list[Any], OrderedDict[str, Any]])

UNDEFINED = "?UNDEFINED?"


class ParseObjectGeneric(SupportsBytes, Generic[T]):
    """The base parsing object for handling parsing in a convenient (to modify) package."""

    def __init__(
        self,
        name: str | Enum,
        bit_count: int = -1,
        data: I | None = None,
        value: T | None = None,
        fmt: str | None = None,
        parent: ParseObjectGeneric[Any] | None = None,
        children: OrderedDict[str, ParseObjectGeneric[Any]] | list[ParseObjectGeneric[Any]] | None = None,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
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
        self._endian: Literal["little", "big"] = endian
        self._bits: bitarray = bitarray(endian="little")
        self._parent: ParseObjectGeneric[Any] | None = None
        self._children: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict()
        self._bit_count: int = bit_count
        if isinstance(name, Enum):
            self._name = name.name
        else:
            self._name = str(name)
        if fmt is None:
            self._fmt = "{}"
        else:
            self._fmt = fmt
        self._parent = parent
        if self._fmt is None:
            self._fmt = "{}"
        if children is not None:
            self._set_children(children)
        if data is not None:
            self.parse(data=data)
        elif value is not None:
            self._set_value(value)

    def parse(self, data: I) -> bitarray:
        """Parse the passed bits or bytes into meaningful data.

        Args:
            data: bits or bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        raise NotImplementedError()

    def update_field(self, data: I | None = None) -> Any:
        """Calculate a new value for this field based on this field and/or an argument.

        Args:
            data: the optional data needed to update this field

        Returns:
            whatever is needed
        """
        raise NotImplementedError()

    def _get_value(self) -> T | None:
        return None

    def _set_value(self, value: T) -> None:
        raise NotImplementedError()

    def _get_children(self) -> OrderedDict[str, ParseObjectGeneric[Any]]:
        return self._children

    def _set_children(
        self, children: OrderedDict[str, ParseObjectGeneric[Any]] | list[ParseObjectGeneric[Any]] | None | None
    ) -> None:
        self._children.clear()
        if isinstance(children, (dict, OrderedDict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value.parent = self
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value.parent = self

    def _get_bits(self) -> bitarray:
        return self._bits

    def _set_bits(self, bits: bitarray) -> None:
        raise NotImplementedError()

    def _get_formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        if self.value is None:
            return UNDEFINED
        else:
            return self._fmt.format(self.value)

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
    def value(self) -> T | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: T) -> None:
        self._set_value(value)

    @property
    def bits(self) -> bitarray:
        """Get the bit value of the field.

        Returns:
            the bit value of the field
        """
        return self._get_bits()

    @bits.setter
    def bits(self, bits: bitarray) -> None:
        self._set_bits(bits)

    @property
    def parent(self) -> ParseObjectGeneric[Any] | None:
        """Get the parent of the field.

        Returns:
            the parent of the field
        """
        return self._parent

    @parent.setter
    def parent(self, parent: ParseObjectGeneric[Any] | None) -> None:
        self._parent = parent

    @property
    def fmt(self) -> str:
        """Get the format string of the field.

        Returns:
            the format string of the field
        """
        return self._fmt

    @fmt.setter
    def fmt(self, fmt: str) -> None:
        self._fmt = fmt

    @property
    def children(self) -> OrderedDict[str, ParseObjectGeneric[Any]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self._get_children()

    @children.setter
    def children(
        self, children: OrderedDict[str, ParseObjectGeneric[Any]] | list[ParseObjectGeneric[Any]] | None | None
    ) -> None:
        self._set_children(children=children)

    @property
    def endian(self) -> Literal["little", "big"]:
        """Get the byte endianness value of this object.

        Returns:
            the byte endianness value of this object
        """
        return self._endian

    @property
    def byte_value(self) -> bytes:
        """Get the byte value of this object.

        Returns:
            the byte value of this object
        """
        return self.__bytes__()

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self._get_formatted_value()

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
        return f"{self._name}: {self.formatted_value}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"


class ParseObject(ParseObjectGeneric[Any]):
    def __init__(
        self,
        name: str | Enum,
        bit_count: int = -1,
        data: I | None = None,
        value: T | None = None,
        fmt: str | None = None,
        parent: ParseObjectGeneric[Any] | None = None,
        children: OrderedDict[str, ParseObjectGeneric[Any]] | list[ParseObjectGeneric[Any]] | None = None,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            value=value,
            fmt=fmt,
            parent=parent,
            children=children,
            endian=endian,
        )
