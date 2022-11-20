"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from typing import Any, OrderedDict
from easyprotocol.base.parse_object import ParseObject
from easyprotocol.base.utils import InputT, input_to_bytes
from bitarray import bitarray
from enum import Enum


class ParseDict(ParseObject[ParseObject[Any]], OrderedDict[str, ParseObject[Any]]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        children: list[ParseObject[Any]] | OrderedDict[str, ParseObject[Any]] | None = None,
        parent: ParseObject[Any] | None = None,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: optional bytes to be parsed
            value: optional value to assign to object
        """
        super().__init__(
            name=name,
            data=None,
            value=None,
            parent=parent,
        )

        if children is not None:
            self.children = children
        if data is not None:
            self.parse(data)

    def parse(self, data: InputT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        for key, field in self._children.items():
            bit_data = field.parse(data=bit_data)
        return bit_data

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
    def value(
        self,
    ) -> dict[str, Any] | OrderedDict[str, Any]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return {k: v.value for k, v in self._children.items()}

    @value.setter
    def value(
        self,
        value: OrderedDict[str, ParseObject[Any]] | OrderedDict[str, Any],
    ) -> None:
        if not isinstance(value, dict):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        for key, item in value.items():
            if isinstance(item, ParseObject):
                self.__setitem__(key, item)
                item.parent = self
            else:
                obj = self.__getitem__(key)
                obj.value = item

    @property
    def bits(self) -> bitarray:
        """Get the bytes value of the field.

        Returns:
            the bytes value of the field
        """
        data = bitarray()
        values = list(self._children.values())
        for value in values:
            data += value.bits
        return data

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for key,value in self._children.items()])}]'

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self.bits.tobytes()

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

    def __setitem__(self, name: str | Enum, value: ParseObject[Any]) -> None:
        if not isinstance(value, ParseObject):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        value.parent = self
        if isinstance(name, Enum):
            return self._children.__setitem__(name.name, value)
        else:
            return self._children.__setitem__(name, value)

    def __getitem__(self, name: str | Enum) -> ParseObject[Any]:
        if isinstance(name, Enum):
            return self._children.__getitem__(name.name)
        else:
            return self._children.__getitem__(name)

    def __delitem__(self, name: str | Enum) -> None:
        if isinstance(name, Enum):
            return self._children.__delitem__(name.name)
        else:
            return self._children.__delitem__(name)

    def popitem(self, last: bool) -> tuple[str, ParseObject[Any]]:
        self.children.popitem(last=last)

    def pop(self, name: str | Enum) -> ParseObject[Any]:
        if isinstance(name, Enum):
            p = self.children.pop(name.name)
        else:
            p = self.children.pop(name)
        p.parent = None
        return p

    def __len__(self) -> int:
        return len(self._children)
