"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from collections import OrderedDict
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    MutableSequence,
    Sequence,
    SupportsIndex,
    TypeVar,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseGeneric, endianT

# from easyprotocol.base.parse_generic_value import _T
from easyprotocol.base.utils import dataT, input_to_bytes

_T = TypeVar("_T")


class ParseGenericList(
    ParseGeneric[_T],
    MutableSequence[ParseGeneric[_T]],
    Generic[_T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: Sequence[ParseGeneric[_T]] | OrderedDict[str, ParseGeneric[_T]] = list(),
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

        if isinstance(default, dict):
            self._set_children_generic(default)
        else:
            self._set_children_generic(OrderedDict({val._name: val for val in default}))
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

    def insert(self, index: int | slice, value: ParseGeneric[_T] | Sequence[ParseGeneric[_T]]) -> None:
        c: OrderedDict[str, ParseGeneric[_T]] = OrderedDict()
        for i, v in enumerate(self._children.values()):
            if index == i:
                if isinstance(value, ParseGeneric):
                    c[value._name] = value
                    value._set_parent_generic(self)
                else:
                    raise NotImplementedError()
            c[v._name] = self._children[v._name]
        self._children = c

    def append(self, value: ParseGeneric[_T]) -> None:
        self._children[value.name] = value

    def get_value(self) -> Sequence[ParseGeneric[_T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [item for item in self._children.values()]

    def set_value(
        self,
        value: Sequence[ParseGeneric[_T]] | OrderedDict[str, ParseGeneric[_T]],
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

    def get_bits_lsb(self) -> bitarray:
        data = bitarray(endian="little")
        values = list(self._children.values())
        for value in values:
            data += value.bits_lsb
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

    @property
    def value(self) -> Sequence[ParseGeneric[_T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: Sequence[ParseGeneric[_T]]) -> None:
        self.set_value(value=value)

    @overload
    def __getitem__(self, index: int) -> ParseGeneric[_T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[ParseGeneric[_T]]:
        ...

    def __getitem__(self, index: int | slice) -> ParseGeneric[_T] | Sequence[ParseGeneric[_T]]:
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
    def __setitem__(self, index: SupportsIndex, value: ParseGeneric[_T]) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[ParseGeneric[_T]]) -> None:
        ...

    def __setitem__(self, index: SupportsIndex | slice, value: ParseGeneric[_T] | Iterable[ParseGeneric[_T]]) -> None:
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

    def _get_children_generic(self) -> OrderedDict[str, ParseGeneric[_T]]:
        return self._children

    def _set_children_generic(
        self,
        children: OrderedDict[str, ParseGeneric[_T]] | Sequence[ParseGeneric[_T]] | None,
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

    def __iter__(self) -> Iterator[ParseGeneric[Any]]:
        return self._children.values().__iter__()
