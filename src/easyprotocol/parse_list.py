"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from typing import Any, MutableSequence
from easyprotocol.parse_object import ParseObject


class ParseList(MutableSequence[ParseObject[Any]]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | None = None,
        value: list[Any] | None = None,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: optional bytes to be parsed
            value: optional value to assign to object
        """
        self._name = name
        self._list: list[ParseObject[Any]] = list()

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
        for field in self._list:
            data = field.parse(data=data)
        return data

    @property
    def name(self) -> str:
        """Get the name of the field.

        Returns:
            the name of the field
        """
        return self._name

    @property
    def value(self) -> list[ParseObject[Any]] | list[Any]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return list(self._list)

    @value.setter
    def value(self, value: list[ParseObject[Any]] | list[Any]) -> None:
        if not isinstance(value, list):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        for index, item in enumerate(value):
            if isinstance(item, ParseObject):
                if index < len(self._list):
                    self[index] = item
                else:
                    self.append(item)
            else:
                self[index].value = item

    @property
    def data(self) -> bytes:
        """Get the bytes value of the field.

        Returns:
            the bytes value of the field
        """
        data = b""
        for value in self._list:
            data += bytes(value)
        return data

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{",".join([str(value) for value in self._list])}]'

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self.data

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

    def __getitem__(self, index: int | slice) -> ParseObject[Any]:
        return self._list[index]

    def __delitem__(self, index: int | slice) -> None:
        del self._list[index]

    def __setitem__(self, index: int | slice, val: ParseObject[Any]):
        self._list[index] = val

    def insert(self, index: int | slice, val: ParseObject[Any]):
        self._list.insert(index, val)

    def append(self, val: ParseObject[Any]):
        self.insert(len(self._list), val)

    def __len__(self) -> int:
        return len(self._list)
