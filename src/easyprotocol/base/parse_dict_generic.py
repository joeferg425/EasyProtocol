"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from enum import Enum
from typing import Any, Literal, OrderedDict, TypeVar, Union, cast

from bitarray import bitarray

# from easyprotocol.base.parse_field import ParseFieldGeneric
from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseGeneric, endianT
from easyprotocol.base.utils import dataT, input_to_bytes

T = TypeVar("T", bound=Any)


class ParseDictGeneric(
    ParseGeneric[T],
    OrderedDict[str, ParseGeneric[T]],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        value: OrderedDict[str, ParseGeneric[T]] | dict[str, ParseGeneric[T]] | list[ParseGeneric[T]] | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseGeneric[Any] | None = None,
        children: OrderedDict[str, ParseGeneric[T]] | dict[str, ParseGeneric[T]] | list[ParseGeneric[T]] | None = None,
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
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
            parent=parent,
        )
        if children is not None:
            self._set_children_generic(children=children)
        if data is not None:
            self.parse(data)
        elif value is not None:
            self.set_value(value=value)

    def parse(self, data: dataT) -> bitarray:
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

    def popitem(self, last: bool = False) -> tuple[str, ParseGeneric[T]]:
        """Remove item from list.

        Args:
            last: delete the last added item instead of the first

        Returns:
            the popped item
        """
        return cast(tuple[str, ParseGeneric[T]], self._children.popitem(last=last))

    def pop(self, name: str, default: ParseGeneric[T] | None = None) -> ParseGeneric[T] | None:
        """Pop item from dictionary by name.

        Args:
            name: name of item to pop
            default: object to return if the name is not in the dictionary

        Returns:
            the item (or default item)
        """
        if isinstance(name, Enum):
            p = self._children.pop(name.name, default)
        else:
            p = self._children.pop(name, default)
        if p is not None:
            p._set_parent_generic(None)
        return p

    def get_value(
        self,
    ) -> OrderedDict[str, ParseGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return OrderedDict(self._children)

    def set_value(
        self,
        value: OrderedDict[str, ParseGeneric[T]] | dict[str, ParseGeneric[T]] | list[ParseGeneric[T]],
    ) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                self.__setitem__(key, item)
                item._set_parent_generic(self)
        else:
            for item in value:
                key = item.name
                self.__setitem__(key, item)
                item._set_parent_generic(self)

    def get_bits(self) -> bitarray:
        data = bitarray(endian="little")
        values = list(self._children.values())
        for value in values:
            data += value.bits
        return data

    def _get_children_generic(self) -> OrderedDict[str, ParseGeneric[T]]:
        return self._children

    def _set_children_generic(
        self,
        children: OrderedDict[str, ParseGeneric[T]] | dict[str, ParseGeneric[T]] | list[ParseGeneric[T]] | None,
    ) -> None:
        self._children.clear()
        if isinstance(children, (dict)):
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
        return f'{{{", ".join([str(value) for value in self._children.values()])}}}'

    @property
    def value(self) -> OrderedDict[str, ParseGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: OrderedDict[str, ParseGeneric[T]] | dict[str, ParseGeneric[T]] | list[ParseGeneric[T]],
    ) -> None:
        self.set_value(value)

    @property
    def children(self) -> OrderedDict[str, ParseGeneric[T]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self._get_children_generic()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseGeneric[T]] | dict[str, ParseGeneric[T]] | list[ParseGeneric[T]] | None,
    ) -> None:
        self._set_children_generic(children=children)

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
        return f"{self._name}: {self.string}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    def __setitem__(self, name: str, value: ParseGeneric[T]) -> None:
        value._set_parent_generic(self)
        return self._children.__setitem__(name, value)

    def __getitem__(self, name: str) -> ParseGeneric[T]:
        return self._children.__getitem__(name)

    def __delitem__(self, name: str) -> None:
        return self._children.__delitem__(name)

    def __len__(self) -> int:
        return len(self._children)

    @property
    def parent(self) -> ParseGeneric[Any] | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_parent_generic()

    @value.setter
    def value(self, value: ParseGeneric[Any] | None) -> None:
        self._set_parent_generic(value)
