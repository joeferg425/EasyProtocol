"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from collections import OrderedDict
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    Sequence,
    SupportsIndex,
    Union,
    cast,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseGeneric, T, endianT
from easyprotocol.base.parse_generic_dict import K, ParseGenericDict
from easyprotocol.base.parse_generic_list import ParseGenericList
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.utils import dataT, input_to_bytes

ParseGenericUnion = Union[ParseGenericValue[T], ParseGenericDict[K, T], ParseGenericList[T]]


class ParseFieldListGeneric(ParseGeneric[T], Sequence[ParseGenericUnion[K, T]], Generic[K, T]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: Sequence[ParseGeneric[T]] | OrderedDict[str, ParseGeneric[T]] = list(),
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
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
        )

        self.set_children(default)  # pyright:ignore[reportGeneralTypeIssues]
        if data is not None:
            self.parse(data)
        elif default is not None:
            self.set_value(default)  # pyright:ignore[reportGeneralTypeIssues]

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

    def insert(self, index: int | slice, value: ParseGeneric[T] | Sequence[ParseGeneric[T]]) -> None:
        c: OrderedDict[str, ParseGenericUnion[K, T]] = OrderedDict()
        for i, v in enumerate(self.children.values()):
            if index == i:
                if isinstance(value, ParseGeneric):
                    c[value._name] = value  # pyright:ignore[reportGeneralTypeIssues]
                    value._set_parent_generic(self)
                else:
                    raise NotImplementedError()
            c[v._name] = self.children[v._name]
        self.children = c

    def append(self, value: ParseGenericUnion[K, T]) -> None:
        self.children[value.name] = value

    def get_value(self) -> Sequence[ParseGenericUnion[K, T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [item for item in self.children.values()]

    def set_value(
        self,
        value: Sequence[ParseGenericUnion[K, T]]
        | OrderedDict[
            str,
            ParseGenericUnion[K, T],
        ],
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

    def get_children(self) -> OrderedDict[str, ParseGenericUnion[K, T]]:
        return cast(OrderedDict[str, ParseGenericUnion[K, T]], self._children)

    def set_children(
        self,
        children: OrderedDict[str, ParseGenericUnion[K, T]] | Sequence[ParseGenericUnion[K, T]],
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

    def get_parent(self) -> ParseGenericUnion[K, T] | None:
        return cast(ParseGenericUnion[K, T], self._parent)

    def set_parent(self, parent: ParseGenericUnion[K, T] | None) -> None:
        self._parent = parent

    @property
    def parent(self) -> ParseGenericUnion[K, T] | None:
        return self.get_parent()

    @parent.setter
    def parent(self, value: ParseGenericUnion[K, T] | None) -> None:
        self.set_parent(value)

    @property
    def children(self) -> OrderedDict[str, ParseGenericUnion[K, T]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseGenericUnion[K, T]],
    ) -> None:
        self.set_children(children=children)

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
    def value(self) -> Sequence[ParseGenericUnion[K, T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: Sequence[ParseGeneric[T]]) -> None:
        self.set_value(value=value)  # pyright:ignore[reportGeneralTypeIssues]

    @overload
    def __getitem__(self, index: int) -> ParseGenericUnion[K, T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[ParseGenericUnion[K, T]]:
        ...

    def __getitem__(self, index: int | slice) -> ParseGenericUnion[K, T] | Sequence[ParseGenericUnion[K, T]]:
        vs = list(self.children.values())[index]
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
    def __setitem__(self, index: SupportsIndex, value: ParseGenericUnion[K, T]) -> None:
        ...

    @overload
    def __setitem__(self, index: int | slice, value: Iterable[ParseGenericUnion[K, T]]) -> None:
        ...

    def __setitem__(
        self, index: SupportsIndex | int | slice, value: ParseGeneric[T] | Iterable[ParseGeneric[T]]
    ) -> None:
        indexed_keys = list(self._children.keys())[index]
        c: OrderedDict[str, ParseGenericUnion[K, T]] = OrderedDict()
        for existing_key in self.children:
            if isinstance(indexed_keys, str) and isinstance(value, ParseGeneric):
                if existing_key != indexed_keys:
                    c[existing_key] = self.children[existing_key]
                else:
                    c[indexed_keys] = value  # pyright:ignore[reportGeneralTypeIssues]
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        sub_value = value[i]
                        if existing_key != sub_key:
                            c[existing_key] = self.children[existing_key]
                        else:
                            c[sub_value._name] = sub_value  # pyright:ignore[reportGeneralTypeIssues]
                            sub_value._set_parent_generic(self)
        self.children = c

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self) -> Iterator[T]:
        return self.children.values().__iter__()  # pyright:ignore[reportGeneralTypeIssues]


class ParseFieldList(ParseFieldListGeneric[str, Any]):
    ...
