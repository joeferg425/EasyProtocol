"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from collections import OrderedDict
from typing import (
    Any,
    Iterable,
    MutableSequence,
    SupportsIndex,
    TypeVar,
    Union,
    cast,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.parse_dict_generic import ParseDictGeneric
from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseGeneric, endianT
from easyprotocol.base.parse_list_generic import ParseListGeneric
from easyprotocol.base.parse_value_generic import ParseValueGeneric
from easyprotocol.base.utils import dataT, input_to_bytes

T = TypeVar("T", bound=Any)
ParseGenericUnion = Union[ParseValueGeneric[T], ParseDictGeneric[T], ParseListGeneric[T]]
valueT = Union[T, list[ParseGenericUnion[T]], OrderedDict[str, ParseGenericUnion[T]]]


class ParseFieldListGeneric(
    ParseGeneric[T],
    MutableSequence[ParseGenericUnion[T]],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: list[ParseGenericUnion[T]]
        | dict[str, ParseGenericUnion[T]]
        | OrderedDict[str, ParseGenericUnion[T]]
        | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseGenericUnion[Any] | None = None,
        children: OrderedDict[str, ParseGenericUnion[Any]]
        | dict[str, ParseGenericUnion[Any]]
        | list[ParseGenericUnion[Any]]
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
            self.set_children(children)
        if data is not None:
            self.parse(data)
        elif default is not None:
            self.set_value(default)

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

    def insert(self, index: int | slice, value: ParseGenericUnion[T] | list[ParseGenericUnion[T]]) -> None:
        c: OrderedDict[str, ParseGenericUnion[T]] = OrderedDict()
        for i, v in enumerate(self.children.values()):
            if index == i:
                if isinstance(value, ParseGeneric):
                    c[value._name] = value
                    value._set_parent_generic(self)
                else:
                    raise NotImplementedError()
            c[v._name] = self.children[v._name]
        self.children = c

    def append(self, value: ParseGenericUnion[T]) -> None:
        self.children[value.name] = value

    def get_value(self) -> list[ParseGenericUnion[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [item for item in self.children.values()]

    def set_value(
        self,
        value: list[ParseGenericUnion[T]]
        | dict[str, ParseGenericUnion[T]]
        | OrderedDict[
            str,
            ParseGenericUnion[T],
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

    def get_children(self) -> OrderedDict[str, ParseGenericUnion[T]]:
        return cast(OrderedDict[str, ParseGenericUnion[T]], self._children)

    def set_children(
        self,
        children: OrderedDict[str, ParseGenericUnion[T]]
        | dict[str, ParseGenericUnion[T]]
        | list[ParseGenericUnion[T]]
        | None,
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

    def get_parent(self) -> ParseGenericUnion[Any] | None:
        return cast(ParseGenericUnion[Any], self._parent)

    def set_parent(self, parent: ParseGenericUnion[T] | None) -> None:
        self._parent = parent

    @property
    def parent(self) -> ParseGenericUnion[T] | None:
        return self.get_parent()

    @parent.setter
    def parent(self, value: ParseGenericUnion[T] | None) -> None:
        self.set_parent(value)

    @property
    def children(self) -> OrderedDict[str, ParseGenericUnion[T]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseGenericUnion[T]],
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
    def value(self) -> list[ParseGenericUnion[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: list[ParseGenericUnion[T]]) -> None:
        self.set_value(value=value)

    @overload
    def __getitem__(self, index: int) -> ParseGenericUnion[T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[ParseGenericUnion[T]]:
        ...

    def __getitem__(self, index: int | slice) -> ParseGenericUnion[T] | list[ParseGenericUnion[T]]:
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
    def __setitem__(self, index: SupportsIndex, value: ParseGenericUnion[T]) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[ParseGenericUnion[T]]) -> None:
        ...

    def __setitem__(
        self, index: SupportsIndex | slice, value: ParseGenericUnion[T] | Iterable[ParseGenericUnion[T]]
    ) -> None:
        indexed_keys = list(self._children.keys())[index]
        c: OrderedDict[str, ParseGenericUnion[Any]] = OrderedDict()
        for existing_key in self.children:
            if isinstance(indexed_keys, str) and isinstance(value, ParseGeneric):
                if existing_key != indexed_keys:
                    c[existing_key] = self.children[existing_key]
                else:
                    c[indexed_keys] = value
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        sub_value = value[i]
                        if existing_key != sub_key:
                            c[existing_key] = self.children[existing_key]
                        else:
                            c[sub_value._name] = sub_value
                            sub_value._set_parent_generic(self)
        self.children = c

    def __len__(self) -> int:
        return len(self._children)


class ParseFieldList(ParseFieldListGeneric[Any]):
    ...


class ParseValueList(
    ParseGeneric[T],
    MutableSequence[T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseGenericUnion[Any] | None = None,
        children: OrderedDict[str, ParseValueGeneric[Any]]
        | dict[str, ParseValueGeneric[Any]]
        | list[ParseValueGeneric[Any]]
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
                self.set_children(children)
            else:
                self.set_children(OrderedDict({val._name: val for val in children}))
        if data is not None:
            self.parse(data)

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

    def insert(self, index: int | slice, value: ParseValueGeneric[T] | list[ParseValueGeneric[T]]) -> None:
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

    def append(self, value: T) -> None:
        raise NotImplementedError()

    def get_value(self) -> list[T]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [v.value for v in self.children.values()]

    def set_value(self, value: list[T] | list[ParseValueGeneric[T]]) -> None:
        if value is not None:
            for index in range(len(value)):
                item = value[index]
                if isinstance(item, ParseValueGeneric):
                    if index < len(self.children):
                        self[index] = item  # pyright:ignore[reportGeneralTypeIssues]
                        item._set_parent_generic(self)
                    else:
                        self.children[item.name] = item
                        item._set_parent_generic(self)
                else:
                    # parse_base = self[index]
                    self[index] = item.value

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
    def value(self) -> list[T]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: list[T]) -> None:
        self.set_value(value=value)

    @overload
    def __getitem__(self, index: SupportsIndex) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Iterable[T]:
        ...

    def __getitem__(self, index: SupportsIndex | slice) -> valueT[T] | Iterable[valueT[T]]:
        vs = list(self.children.values())[index]
        if isinstance(vs, list):
            return cast(
                list[valueT[T]],
                [v.value for v in vs],
            )
        else:
            return cast(valueT[T], vs.value)

    def __delitem__(self, index: int | slice) -> None:
        item = list(self.children.values())[index]
        if isinstance(item, list):
            for x in item:
                x._set_parent_generic(None)
                self._children.pop(x._name)
        else:
            item._set_parent_generic(None)
            self._children = OrderedDict({k: v for k, v in self._children.items() if k != item.name})

    @overload
    def __setitem__(self, index: SupportsIndex, value: T) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[T]) -> None:
        ...

    def __setitem__(self, index: SupportsIndex | slice, value: T | Iterable[T]) -> None:
        indexed_keys = list(self._children.keys())[index]
        c: OrderedDict[str, ParseValueGeneric[Any]] = OrderedDict()
        for existing_key in self.children:
            if isinstance(indexed_keys, str):
                if isinstance(value, ParseValueGeneric):
                    if existing_key != indexed_keys:
                        c[existing_key] = self.children[existing_key]
                    else:
                        old = self.children[value._name]
                        old._set_parent_generic(None)
                        c[value.name] = value
                        value._set_parent_generic(self)
                else:
                    c[existing_key] = self.children[existing_key]
                    c[existing_key].value = value
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        sub_value = value[i]
                        if isinstance(sub_value, ParseValueGeneric):
                            if existing_key != sub_key:
                                c[existing_key] = self.children[existing_key]
                            else:
                                c[sub_value._name] = sub_value
                                sub_value._set_parent_generic(self)
        self.children = c

    def __len__(self) -> int:
        return len(self._children)

    def get_children(self) -> OrderedDict[str, ParseValueGeneric[T]]:
        return cast(
            OrderedDict[
                str,
                ParseValueGeneric[T],
            ],
            self._children,
        )

    def set_children(
        self,
        children: OrderedDict[str, ParseValueGeneric[T]]
        | dict[str, ParseValueGeneric[T]]
        | list[ParseValueGeneric[T]]
        | None,
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

    def get_parent(self) -> ParseValueGeneric[Any] | None:
        return cast(ParseValueGeneric[Any], self._parent)

    def set_parent(self, parent: ParseValueGeneric[T] | None) -> None:
        self._parent = parent

    @property
    def parent(self) -> ParseValueGeneric[T] | None:
        return self.get_parent()

    @parent.setter
    def parent(self, value: ParseValueGeneric[T] | None) -> None:
        self.set_parent(value)

    @property
    def children(self) -> OrderedDict[str, ParseValueGeneric[Any]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseValueGeneric[Any]]
        | dict[str, ParseValueGeneric[Any]]
        | list[ParseValueGeneric[Any]]
        | None,
    ) -> None:
        self.set_children(children=children)
