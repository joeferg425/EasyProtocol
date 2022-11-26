"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from enum import Enum
from typing import Any, OrderedDict

from bitarray import bitarray

from easyprotocol.base.parse_object import ParseObjectGeneric, T
from easyprotocol.base.utils import I, input_to_bytes


class ParseDictGeneric(
    ParseObjectGeneric[OrderedDict[str, ParseObjectGeneric[T]]], OrderedDict[str, ParseObjectGeneric[T]]
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        bit_count: int = -1,
        data: I | None = None,
        value: OrderedDict[str, ParseObjectGeneric[T]] | None = None,
        children: OrderedDict[str, ParseObjectGeneric[T]] | None = None,
        parent: ParseObjectGeneric[T] | None = None,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: optional bytes to be parsed
            value: optional value to assign to object
        """
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=None,
            value=None,
            parent=parent,
        )

        if children is not None:
            self._set_children(children=children)
        if data is not None:
            self.parse(data)
        elif value is not None:
            self._set_value(value=value)

    def parse(self, data: I) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        for field in self._children.values():
            bit_data = field.parse(data=bit_data)
        return bit_data

    def popitem(self, last: bool = False) -> tuple[str, ParseObjectGeneric[T]]:
        """Remove item from list.

        Args:
            last: delete the last added item instead of the first

        Returns:
            the popped item
        """
        return self.children.popitem(last=last)

    def pop(  # type:ignore
        self, name: str, default: ParseObjectGeneric[T] | None = None
    ) -> ParseObjectGeneric[T] | None:
        """Pop item from dictionary by name.

        Args:
            name: name of item to pop
            default: object to return if the name is not in the dictionary

        Returns:
            the item (or default item)
        """
        if isinstance(name, Enum):
            p = self.children.pop(name.name, default)
        else:
            p = self.children.pop(name, default)
        if p is not None:
            p.parent = None
        return p

    def _get_value(
        self,
    ) -> OrderedDict[str, ParseObjectGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return OrderedDict({k: v for k, v in self.children.items()})

    def _set_value(
        self,
        value: OrderedDict[str, ParseObjectGeneric[T]] | OrderedDict[str, T] | None,
    ) -> None:
        if not isinstance(value, dict):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        for key, item in value.items():
            if isinstance(item, ParseObjectGeneric):
                self.__setitem__(key, item)
                item.parent = self
            else:
                obj = self.__getitem__(key)
                obj.value = item

    def _get_bits(self) -> bitarray:
        data = bitarray(endian="little")
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
        return f'[{", ".join([str(value) for value in self._children.values()])}]'

    @property  # type:ignore
    def value(self) -> OrderedDict[str, ParseObjectGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: OrderedDict[str, T] | OrderedDict[str, ParseObjectGeneric[T]] | None) -> None:
        self._set_value(value)

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
        return f"{self._name}: {self.formatted_value}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    def __setitem__(self, name: str | Enum, value: ParseObjectGeneric[T]) -> None:
        if not isinstance(value, ParseObjectGeneric):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        value.parent = self
        if isinstance(name, Enum):
            return self._children.__setitem__(name.name, value)
        else:
            return self._children.__setitem__(name, value)

    def __getitem__(self, name: str | Enum) -> ParseObjectGeneric[T]:
        if isinstance(name, Enum):
            return self._children.__getitem__(name.name)
        else:
            return self._children.__getitem__(name)

    def __delitem__(self, name: str | Enum) -> None:
        if isinstance(name, Enum):
            return self._children.__delitem__(name.name)
        else:
            return self._children.__delitem__(name)

    def __len__(self) -> int:
        return len(self._children)


class ParseDict(ParseDictGeneric[Any]):
    def __init__(
        self,
        name: str,
        bit_count: int = -1,
        data: I | None = None,
        value: OrderedDict[str, ParseObjectGeneric[Any]] | None = None,
        children: OrderedDict[str, ParseObjectGeneric[Any]] | None = None,
        parent: ParseObjectGeneric[Any] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            value=value,
            children=children,
            parent=parent,
        )
