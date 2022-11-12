"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from typing import Any, OrderedDict
from easyprotocol.parse_object import ParseObject

import collections


class ParseDict(OrderedDict[str, ParseObject[Any]]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: bytes | None = None,
        value: dict[str, Any] | OrderedDict[str, Any] | None = None,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: optional bytes to be parsed
            value: optional value to assign to object
        """
        self._name = name
        self._dict: OrderedDict[str, ParseObject[Any]] = collections.OrderedDict()

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
        for key, field in self._dict.items():
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
    def value(
        self,
    ) -> dict[str, ParseObject[Any]] | OrderedDict[str, ParseObject[Any]] | dict[str, Any] | OrderedDict[str, Any]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return dict(self._dict)

    @value.setter
    def value(
        self,
        value: dict[str, ParseObject[Any]]
        | OrderedDict[str, ParseObject[Any]]
        | dict[str, Any]
        | OrderedDict[str, Any],
    ) -> None:
        if not isinstance(value, dict):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        for key, item in value.items():
            if isinstance(item, ParseObject):
                self.__setitem__(key, item)
            else:
                self.__getitem__(key).value = item

    @property
    def data(self) -> bytes:
        """Get the bytes value of the field.

        Returns:
            the bytes value of the field
        """
        data = b""
        for key, value in self._dict.items():
            data += bytes(value)
        return data

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{",".join([str(value) for key,value in self._dict.items()])}]'

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

    def __setitem__(self, __key: str, __value: ParseObject[Any]) -> None:
        if not isinstance(__value, ParseObject):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {__value} of type {type(__value)}")
        return self._dict.__setitem__(__key, __value)

    def __getitem__(self, __key: str) -> ParseObject[Any]:
        return self._dict.__getitem__(__key)
