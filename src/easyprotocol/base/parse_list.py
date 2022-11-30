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

from easyprotocol.base.parse_base import DEFAULT_ENDIANNESS, ParseBaseGeneric, endianT
from easyprotocol.base.utils import dataT, input_to_bytes

T = TypeVar("T", bound=Any)


class ParseListGeneric(
    ParseBaseGeneric[T],
    MutableSequence[T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        value_list: list[T] | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseBaseGeneric[Any] | None = None,
        children: OrderedDict[str, ParseBaseGeneric[Any]]
        | dict[str, ParseBaseGeneric[Any]]
        | list[ParseBaseGeneric[Any]]
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
            value=None,
            data=None,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
            parent=parent,
        )

        if children is not None:
            if isinstance(children, dict):
                self.set_children(children)
            else:
                self.set_children(OrderedDict({val._name: val for val in children}))
        if data is not None:
            self.parse(data)
        elif value_list is not None:
            self.set_list(value_list)

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

    def insert(self, index: int | slice, value: T | ParseBaseGeneric[T]) -> None:
        c: OrderedDict[str, ParseBaseGeneric[T]] = OrderedDict()
        for i, v in enumerate(self._children.values()):
            if index == i:
                if isinstance(value, ParseBaseGeneric):
                    c[value._name] = value
                    value.parent = self
                else:
                    raise NotImplementedError()
            c[v._name] = self._children[v._name]
        self._children = c

    def append(self, value: T) -> None:
        raise NotImplementedError()

    def get_list(self) -> list[ParseBaseGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return list([v for v in self._children.values()])

    def get_value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        raise NotImplementedError()

    def set_list(self, value: list[T] | list[ParseBaseGeneric[T]]) -> None:
        if value is not None:
            for index in range(len(value)):
                item = value[index]
                if isinstance(item, ParseBaseGeneric):
                    if index < len(self._children):
                        self[index] = item.value
                        item.parent = self
                    else:
                        self.children[item.name] = item
                        item.parent = self
                else:
                    # parse_base = self[index]
                    self[index] = item

    def set_value(self, value: T) -> None:
        raise NotImplementedError()

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
    def value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: T) -> None:
        self.set_value(value=value)

    @property
    def value_list(self) -> list[ParseBaseGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_list()

    @value_list.setter
    def value_list(self, value: list[T] | list[ParseBaseGeneric[T]]) -> None:
        self.set_list(value)

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[T]:
        ...

    def __getitem__(self, index: int | slice) -> T | list[T]:
        vs = list(self._children.values())[index]
        if isinstance(vs, list):
            return [v.value for v in vs]
        else:
            return vs.value

    def __delitem__(self, index: int | slice) -> None:
        item = list(self._children.values())[index]
        if isinstance(item, list):
            for x in item:
                x.parent = None
                self._children.pop(x._name)
        else:
            item.parent = None
            self._children = OrderedDict({k: v for k, v in self._children.items() if k != item.name})

    @overload
    def __setitem__(self, index: SupportsIndex, value: T) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[T]) -> None:
        ...

    def __setitem__(self, index: SupportsIndex | slice, value: T | Iterable[T]) -> None:
        indexed_keys = list(self._children.keys())[index]
        c: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict()
        for existing_key in self._children:
            if isinstance(indexed_keys, str):
                if isinstance(value, ParseBaseGeneric):
                    if existing_key != indexed_keys:
                        c[existing_key] = self._children[existing_key]
                    else:
                        old = self._children[value._name]
                        old.parent = None
                        c[value._name] = value
                        value.parent = self
                else:
                    c[existing_key] = self._children[existing_key]
                    c[existing_key].value = value
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        sub_value = value[i]
                        if isinstance(sub_value, ParseBaseGeneric):
                            if existing_key != sub_key:
                                c[existing_key] = self._children[existing_key]
                            else:
                                c[sub_value._name] = sub_value
                                sub_value.parent = self
        self._children = c

    def __len__(self) -> int:
        return len(self._children)

    def get_children(self) -> OrderedDict[str, ParseBaseGeneric[T]]:
        return self._children

    def set_children(
        self,
        children: OrderedDict[str, ParseBaseGeneric[T]]
        | dict[str, ParseBaseGeneric[T]]
        | list[ParseBaseGeneric[T]]
        | None,
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
    def children(self) -> OrderedDict[str, ParseBaseGeneric[Any]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseBaseGeneric[Any]]
        | dict[str, ParseBaseGeneric[Any]]
        | list[ParseBaseGeneric[Any]]
        | None,
    ) -> None:
        self.set_children(children=children)


class ParseList(ParseListGeneric[Any]):
    def __init__(
        self,
        name: str,
        value: list[T] | None = None,
        data: dataT | None = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseBaseGeneric[Any] | None = None,
        children: OrderedDict[str, ParseBaseGeneric[Any]]
        | dict[str, ParseBaseGeneric[Any]]
        | list[ParseBaseGeneric[Any]]
        | None = None,
    ) -> None:
        super().__init__(
            name=name,
            value_list=value,
            data=data,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
            parent=parent,
            children=children,
        )
