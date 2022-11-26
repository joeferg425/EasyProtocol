"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from collections import OrderedDict
from enum import Enum
from typing import Any, Generic, Literal, MutableSequence, overload

from bitarray import bitarray

from easyprotocol.base.parse_object import ParseObjectGeneric, T
from easyprotocol.base.utils import I, input_to_bytes


class ParseListGeneric(
    ParseObjectGeneric[list[ParseObjectGeneric[T]]], MutableSequence[ParseObjectGeneric[T]], Generic[T]
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str | Enum,
        bit_count: int = -1,
        data: I | None = None,
        value: list[ParseObjectGeneric[T]] | None = None,
        parent: ParseObjectGeneric[T] | None = None,
        children: list[ParseObjectGeneric[T]] | OrderedDict[str, ParseObjectGeneric[T]] | None = None,
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
            bit_count=bit_count,
            data=None,
            value=None,
            parent=parent,
            fmt=format,
        )

        if children is not None:
            if isinstance(children, dict):
                self._set_children(children)
            else:
                self._set_children(OrderedDict({val._name: val for val in children}))
        if data is not None:
            self.parse(data)
        elif value is not None:
            self._set_value(value)

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

    def insert(self, index: int | slice, val: ParseObjectGeneric[T]) -> None:
        c: OrderedDict[str, ParseObjectGeneric[Any]] = OrderedDict()
        for i, value in enumerate(self._children.values()):
            if index == i:
                c[val._name] = val
                val.parent = self
            c[value._name] = self._children[value._name]
        self._children = c

    def append(self, val: ParseObjectGeneric[T]) -> None:
        self._children[val._name] = val
        val.parent = self

    def _get_value(self) -> list[T | None]:  # type:ignore
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return list([v.value for f, v in self._children.items()])

    def _set_value(self, value: list[Any] | list[ParseObjectGeneric[T]]) -> None:
        if not isinstance(value, list):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        for index, item in enumerate(value):
            if isinstance(item, ParseObjectGeneric):
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
        return f"{self._name}: {self.formatted_value}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    @property  # type:ignore
    def value(self) -> list[Any | None]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: list[ParseObjectGeneric[T]] | list[Any]) -> None:
        self._set_value(value)

    @overload
    def __getitem__(self, index: int) -> ParseObjectGeneric[T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[ParseObjectGeneric[T]]:
        ...

    def __getitem__(self, index: int | slice) -> ParseObjectGeneric[T] | list[ParseObjectGeneric[T]]:
        return list(self._children.values())[index]

    def __delitem__(self, index: int | slice) -> None:
        item = list(self._children.values())[index]
        if isinstance(item, list):
            for x in item:
                x.parent = None
                self._children.pop(x._name)
        else:
            item.parent = None
            self._children.pop(item._name)

    @overload  # type:ignore
    def __setitem__(self, index: int, value: ParseObjectGeneric[T]) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: list[ParseObjectGeneric[T]]) -> None:
        ...

    def __setitem__(self, index: int | slice, value: ParseObjectGeneric[T] | list[ParseObjectGeneric[T]]) -> None:
        index_key = list(self._children.keys())[index]
        c = OrderedDict()
        for key in self._children:
            if isinstance(index_key, str) and isinstance(value, ParseObjectGeneric):
                if key != index_key:
                    c[key] = self._children[key]
                else:
                    c[value._name] = value
                    value.parent = self
            elif isinstance(index_key, list) and isinstance(value, list):
                for i, sub_key in enumerate(index_key):
                    if key != sub_key:
                        c[key] = self._children[key]
                    else:
                        c[value[i]._name] = value[i]
                        value[i].parent = self
        self._children = c

    def __len__(self) -> int:
        return len(self._children)

    def _get_children(self) -> OrderedDict[str, ParseObjectGeneric[T]]:
        return self._children

    def _set_children(
        self, children: OrderedDict[str, ParseObjectGeneric[T]] | list[ParseObjectGeneric[T]] | None | None
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

    @property
    def children(self) -> OrderedDict[str, ParseObjectGeneric[T]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self._get_children()

    @children.setter
    def children(
        self, children: OrderedDict[str, ParseObjectGeneric[T]] | list[ParseObjectGeneric[T]] | None | None
    ) -> None:
        self._set_children(children=children)


class ParseList(ParseListGeneric[Any]):
    def __init__(
        self,
        name: str | Enum,
        bit_count: int = -1,
        data: I | None = None,
        value: list[ParseObjectGeneric[Any]] | None = None,
        parent: ParseObjectGeneric[Any] | None = None,
        children: list[ParseObjectGeneric[Any]] | OrderedDict[str, ParseObjectGeneric[Any]] | None = None,
        format: str = "{}",
    ) -> None:
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            value=value,
            parent=parent,
            children=children,
            format=format,
        )
