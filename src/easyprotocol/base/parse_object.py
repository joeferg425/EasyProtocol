"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from collections import OrderedDict
from typing import Literal, SupportsBytes, Generic, Any
from bitarray import bitarray
from easyprotocol.base.utils import T, InputT


class ParseObject(SupportsBytes, Generic[T]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: T | None = None,
        format: str | None = None,
        parent: ParseObject[Any] = None,
        endian: Literal["little", "big"] = "big",
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: optional bytes to be parsed
            value: optional value to assign to object
            parent: an optional containing object for nesting layers of parsed objects
        """
        self._name = name
        self._endian = endian
        self._bits: bitarray = bitarray(endian=self._endian)
        self._value: T | None = None
        self._format = format
        self._parent: ParseObject[Any] | None = parent
        self._children: OrderedDict[str, ParseObject[Any]] = OrderedDict()

        if self._format is None:
            self._format = "{}"
        if data is not None:
            self.parse(data=data)
        elif value is not None:
            self.value = value

    def parse(self, data: InputT) -> bitarray:
        """Parse bits or bytes that make of this protocol field into meaningful data.

        Args:
            data: bits or bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        raise NotImplementedError()

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
    def endian(self) -> Literal["little", "big"]:
        return self._endian

    @property
    def format(self) -> str:
        """Get the format string of the field.

        Returns:
            the format string of the field
        """
        return self._format

    @format.setter
    def format(self, format: str) -> None:
        self._format = format

    @property
    def value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        raise NotImplementedError()

    @property
    def parent(self) -> ParseObject[Any]:
        """Get the parent of the field.

        Returns:
            the parent of the field
        """
        return self._parent

    @parent.setter
    def parent(self, parent: ParseObject[Any]) -> None:
        self._parent = parent

    @property
    def children(self) -> OrderedDict[str, ParseObject[Any]]:
        return self._children

    @children.setter
    def children(self, children: OrderedDict[str, ParseObject[Any]]) -> None:
        for key, value in children.items():
            self._children[key] = value
            value.parent = self

    @property
    def bits(self) -> bitarray:
        """Get the bit value of the field.

        Returns:
            the bit value of the field
        """
        return self._bits

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self._format.format(self.value)

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
        return f"{self.name}: {self.formatted_value}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"
