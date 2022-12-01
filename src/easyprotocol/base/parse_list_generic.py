"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from collections import OrderedDict
from typing import (
    Any,
    Generic,
    Iterable,
    Literal,
    MutableSequence,
    SupportsIndex,
    TypeVar,
    Union,
    cast,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseGeneric, endianT
from easyprotocol.base.utils import dataT, input_to_bytes

T = TypeVar("T", bound=Any)


class ParseListGeneric(
    ParseGeneric[T],
    MutableSequence[ParseGeneric[T]],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        value: list[ParseGeneric[T]] | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseGeneric[Any] | None = None,
        children: OrderedDict[str, ParseGeneric[Any]]
        | dict[str, ParseGeneric[Any]]
        | list[ParseGeneric[Any]]
        | None = None,
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
            if isinstance(children, dict):
                self._set_children_generic(children)
            else:
                self._set_children_generic(OrderedDict({val._name: val for val in children}))
        if data is not None:
            self.parse(data)
        elif value is not None:
            self.set_value(value)

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

    def insert(self, index: int | slice, value: ParseGeneric[T] | list[ParseGeneric[T]]) -> None:
        c: OrderedDict[str, ParseGeneric[T]] = OrderedDict()
        for i, v in enumerate(self._children.values()):
            if index == i:
                if isinstance(value, ParseGeneric):
                    c[value._name] = value
                    value._set_parent_generic(self)
                else:
                    raise NotImplementedError()
            c[v._name] = self._children[v._name]
        self._children = c

    def append(self, value: ParseGeneric[T]) -> None:
        self._children[value.name] = value

    def get_value(self) -> list[ParseGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [item for item in self._children.values()]

    def set_value(
        self,
        value: list[ParseGeneric[T]] | dict[str, ParseGeneric[T]] | OrderedDict[str, ParseGeneric[T]],
    ) -> None:
        if isinstance(value, (dict, OrderedDict)):
            values = list(value.values())
            for index in range(len(value)):
                item = values[index]
                if index < len(self._children):
                    self[index] = item
                    item._set_parent_generic(self)
                else:
                    self._children[item.name] = item
                    item._set_parent_generic(self)
        else:
            for index in range(len(value)):
                item = value[index]
                if index < len(self._children):
                    self[index] = item
                    item._set_parent_generic(self)
                else:
                    self._children[item.name] = item
                    item._set_parent_generic(self)

    def get_bits(self) -> bitarray:
        data = bitarray(endian="little")
        values = list(self._children.values())
        for value in values:
            data += value.bits
        return data

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for value in self._children .values()])}]'

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

    @property
    def value(self) -> list[ParseGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: list[ParseGeneric[T]]) -> None:
        self.set_value(value=value)

    @overload
    def __getitem__(self, index: int) -> ParseGeneric[T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[ParseGeneric[T]]:
        ...

    def __getitem__(self, index: int | slice) -> ParseGeneric[T] | list[ParseGeneric[T]]:
        vs = list(self._children.values())[index]
        if isinstance(vs, list):
            return [v for v in vs]
        else:
            return vs

    def __delitem__(self, index: int | slice) -> None:
        item = list(self._children.values())[index]
        if isinstance(item, list):
            for x in item:
                x._set_parent_generic(None)
                self._children.pop(x._name)
        else:
            item._set_parent_generic(None)
            self._children = OrderedDict({k: v for k, v in self._children.items() if k != item.name})

    @overload
    def __setitem__(self, index: SupportsIndex, value: ParseGeneric[T]) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[ParseGeneric[T]]) -> None:
        ...

    def __setitem__(self, index: SupportsIndex | slice, value: ParseGeneric[T] | Iterable[ParseGeneric[T]]) -> None:
        indexed_keys = list(self._children.keys())[index]
        c: OrderedDict[str, ParseGeneric[Any]] = OrderedDict()
        for existing_key in self._children:
            if isinstance(indexed_keys, str) and isinstance(value, ParseGeneric):
                if existing_key != indexed_keys:
                    c[existing_key] = self._children[existing_key]
                else:
                    c[indexed_keys] = value
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        sub_value = value[i]
                        if existing_key != sub_key:
                            c[existing_key] = self._children[existing_key]
                        else:
                            c[sub_value._name] = sub_value
                            sub_value._set_parent_generic(self)
        self._children = c

    def __len__(self) -> int:
        return len(self._children)

    def _get_children_generic(self) -> OrderedDict[str, ParseGeneric[T]]:
        return self._children

    def _set_children_generic(
        self,
        children: OrderedDict[str, ParseGeneric[T]] | dict[str, ParseGeneric[T]] | list[ParseGeneric[T]] | None,
    ) -> None:
        self._children.clear()
        if isinstance(children, (dict, OrderedDict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

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
