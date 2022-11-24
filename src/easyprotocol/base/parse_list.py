"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Generic, MutableSequence, SupportsIndex, TypeVar, overload

from bitarray import bitarray

from easyprotocol.base.parse_object import ParseObject
from easyprotocol.base.utils import InputT, T, input_to_bytes


class ParseList(ParseObject[list[ParseObject[Any]]], MutableSequence[ParseObject[Any]]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        value: list[ParseObject[Any]] | None = None,
        parent: ParseObject[Any] | None = None,
        children: list[ParseObject[Any]] | None = None,
        format: str = "{}",
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
            fmt=format,
        )

        if children is not None:
            if isinstance(children, dict):
                self.children = children
            else:
                self.children = OrderedDict({val.name: val for val in children})
        if data is not None:
            self.parse(data)
        elif value is not None:
            self.value = value

    def parse(self, data: InputT) -> bitarray:
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

    def insert(self, index: int | slice, val: ParseObject[Any]) -> None:
        c = OrderedDict()
        for i, value in enumerate(self._children.values()):
            if index == i:
                c[val.name] = val
                val.parent = self
            c[value.name] = self._children[value.name]
        self._children = c

    def append(self, val: ParseObject[Any]) -> None:
        self._children[val.name] = val
        val.parent = self

    def _get_value(self) -> list[Any] | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return list([v.value for f, v in self._children.items()])

    def _set_value(self, value: list[Any] | list[ParseObject[Any]]) -> None:
        if not isinstance(value, list):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        for index, item in enumerate(value):
            if isinstance(item, ParseObject):
                if index < len(self._children):
                    self[index] = item
                    item.parent = self
                else:
                    self.append(item)
                    item.parent = self
            else:
                parse_object = self[index]
                parse_object.value = item

    def _get_bits(self) -> bitarray:
        data = bitarray(endian="little")
        values = list(self._children.values())
        for value in values:
            data += value.bits
        return data

    def _get_formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for key,value in self._children .items()])}]'

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

    @property
    def value(self) -> list[Any] | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: list[ParseObject[Any]] | list[Any]) -> None:
        self._set_value(value)

    @overload
    def __getitem__(self, index: int) -> ParseObject[Any]:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[ParseObject[Any]]:
        ...

    def __getitem__(self, index: int | slice) -> ParseObject[Any] | list[ParseObject[Any]]:
        return list(self._children.values())[index]

    def __delitem__(self, index: int | slice) -> None:
        item = list(self._children.values())[index]
        if isinstance(item, list):
            for x in item:
                x.parent = None
                self._children.pop(x.name)
        else:
            item.parent = None
            self._children.pop(item.name)

    @overload  # type:ignore
    def __setitem__(self, index: int, value: ParseObject[Any]) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: list[ParseObject[Any]]) -> None:
        ...

    def __setitem__(self, index: int | slice, value: ParseObject[Any] | list[ParseObject[Any]]) -> None:
        index_key = list(self._children.keys())[index]
        c = OrderedDict()
        for key in self._children:
            if isinstance(index_key, str) and isinstance(value, ParseObject):
                if key != index_key:
                    c[key] = self._children[key]
                else:
                    c[value.name] = value
                    value.parent = self
            elif isinstance(index_key, list) and isinstance(value, list):
                for i, sub_key in enumerate(index_key):
                    if key != sub_key:
                        c[key] = self._children[key]
                    else:
                        c[value[i].name] = value[i]
                        value[i].parent = self
        self._children = c

    def __len__(self) -> int:
        return len(self._children)
