"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from enum import Enum
from typing import (
    Any,
    Generic,
    Iterator,
    Mapping,
    OrderedDict,
    Sequence,
    TypeVar,
    Union,
    cast,
)

from bitarray import bitarray

# from easyprotocol.base.parse_field_list import ParseGenericUnion
from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseGeneric, T, endianT
from easyprotocol.base.parse_generic_dict import K, ParseGenericDict
from easyprotocol.base.parse_generic_list import ParseGenericList
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.utils import dataT, input_to_bytes

ParseGenericUnion = Union[ParseGenericValue[T], ParseGenericDict[K, T], ParseGenericList[T]]


class ParseFieldDictGeneric(
    ParseGeneric[T],
    Mapping[
        K,
        Any,
    ],
    Generic[K, T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: Sequence[ParseGeneric[T]] = list(),
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
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
        if default is not None:
            if isinstance(default, list):
                self.set_children(children=default)
            # if isinstance(default, OrderedDict):
            #     self.set_children(children=OrderedDict({str(k): v for k, v in default.items()}))
        if data is not None:
            self.parse(data)

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data, endian=self.endian)
        for field in self._children.values():
            bit_data = field.parse(data=bit_data)
        return bit_data

    def popitem(self, last: bool = False) -> tuple[K, ParseGenericUnion[K, T]]:
        """Remove item from list.

        Args:
            last: delete the last added item instead of the first

        Returns:
            the popped item
        """
        return cast(
            tuple[K, ParseGenericUnion[K, T]],
            self._children.popitem(last=last),
        )

    def pop(self, name: str, default: ParseGeneric[T] | None = None) -> ParseGenericUnion[K, T] | None:
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
            p = self._children.pop(str(name), default)
        if p is not None:
            p._set_parent_generic(None)
        return cast(ParseGenericUnion[K, T], p)

    def get_value(
        self,
    ) -> OrderedDict[str, ParseGenericUnion[K, T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return cast(
            OrderedDict[str, ParseGenericUnion[K, T]],
            OrderedDict(self._children),
        )

    def set_value(
        self,
        value: OrderedDict[K, ParseGeneric[T]] | Sequence[ParseGeneric[T]],
    ) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                self.__setitem__(key, item)
                item._set_parent_generic(self)
        else:
            for item in value:
                key = item.name
                self.__setitem__(cast(K, key), item)
                item._set_parent_generic(self)

    def get_bits_lsb(self) -> bitarray:
        data = bitarray(endian="little")
        values = list(self._children.values())
        for value in values:
            data += value.bits_lsb
        return data

    def get_children(self) -> OrderedDict[str, ParseGenericUnion[str, Any]]:
        return self._children  # pyright:ignore[reportGeneralTypeIssues]

    def set_children(
        self,
        children: OrderedDict[str, ParseGeneric[Any]] | Sequence[ParseGeneric[Any]],
    ) -> None:
        self._children.clear()
        if isinstance(children, (dict, OrderedDict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[str(key)] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

    def get_parent(self) -> ParseGenericUnion[str, Any] | None:
        return cast(ParseGenericUnion[str, Any], self._parent)

    def set_parent(self, parent: ParseGenericUnion[str, Any] | None) -> None:
        self._parent = parent

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'{{{", ".join([str(value) for value in self._children.values()])}}}'

    @property
    def value(self) -> OrderedDict[str, ParseGenericUnion[K, T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: Sequence[ParseGeneric[T]],
    ) -> None:
        self.set_value(value)

    @property
    def parent(self) -> ParseGenericUnion[str, Any] | None:
        return self.get_parent()

    @parent.setter
    def parent(self, value: ParseGenericUnion[str, Any] | None) -> None:
        self.set_parent(value)

    @property
    def children(self) -> OrderedDict[str, ParseGenericUnion[str, Any]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseGeneric[Any]],
    ) -> None:
        self.set_children(children=children)

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self.bits_lsb.tobytes()

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

    def __setitem__(self, name: K, value: ParseGeneric[T]) -> None:
        value._set_parent_generic(self)
        return self._children.__setitem__(str(name), value)

    def __getitem__(self, name: K) -> ParseGenericUnion[K, T]:
        return cast(ParseGenericUnion[K, T], self._children.__getitem__(str(name)))

    def __delitem__(self, name: K) -> None:
        return self._children.__delitem__(str(name))

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self) -> Iterator[K]:
        return self._children.__iter__()  # pyright:ignore[reportGeneralTypeIssues]


class ParseFieldDict(ParseFieldDictGeneric[str, Any]):
    ...
