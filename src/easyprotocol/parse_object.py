"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from typing import SupportsBytes, Generic, TypeVar, Any

T = TypeVar("T", Any, Any)


class ParseObject(SupportsBytes, Generic[T]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | None = None,
        value: T | None = None,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: optional bytes to be parsed
            value: optional value to assign to object
        """
        self._name = name
        self._data: bytes | None = None
        self._value: T | None = None

        if data is not None:
            self.parse(data)
        elif value is not None:
            self.value = value

    def parse(self, data: bytes) -> bytes:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

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
    def data(self) -> bytes:
        """Get the bytes value of the field.

        Returns:
            the bytes value of the field
        """
        return self._data

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return str(self.value)

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        if self._data is not None:
            return self._data
        else:
            return b""

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
