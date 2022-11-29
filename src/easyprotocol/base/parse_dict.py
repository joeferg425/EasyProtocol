"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from enum import Enum
from typing import Any, Literal, OrderedDict, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_base import DEFAULT_ENDIANNESS, ParseBase, ParseBaseGeneric, endianT
from easyprotocol.base.parse_field import ParseFieldGeneric
from easyprotocol.base.utils import dataT, input_to_bytes

T = TypeVar("T", bound=Any)
# valueVT = OrderedDict[str, T]
# assignVT = Union[
#     list[T],
#     dict[str, T],
#     dict[str, ParseValueGeneric[T]],
#     OrderedDict[str, T],
#     OrderedDict[str, ParseValueGeneric[T]],
#     None,
# ]
# childVT = OrderedDict[str, ParseFieldGeneric[T]]
# assignChildVT = Union[
#     OrderedDict[str, ParseValueGeneric[T]],
#     dict[str, ParseValueGeneric[T]],
#     list[ParseValueGeneric[T]],
#     None,
# ]
# valueFT = OrderedDict[str, ParseFieldGeneric[T]]
# assignFT = Union[
#     list[ParseFieldGeneric[T]],
#     dict[str, T],
#     dict[str, ParseFieldGeneric[T]],
#     OrderedDict[str, T],
#     OrderedDict[str, ParseFieldGeneric[T]],
#     None,
# ]
# childFT = OrderedDict[str, ParseValueGeneric[T]]
# assignChildFT = Union[
#     OrderedDict[str, ParseFieldGeneric[T]],
#     dict[str, ParseFieldGeneric[T]],
#     list[ParseFieldGeneric[T]],
#     None,
# ]


class ParseDictGeneric(
    ParseBaseGeneric[T],
    dict[str, T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        value_dict: dict[str, T] | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseBaseGeneric[Any] | None = None,
        children: OrderedDict[str, ParseBaseGeneric[T]]
        | dict[str, ParseBaseGeneric[T]]
        | list[ParseBaseGeneric[T]]
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
            self.set_children(children=children)
        if data is not None:
            self.parse(data)
        elif value_dict is not None:
            self.set_dict(value=value_dict)

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

    def popitem(self, last: bool = False) -> tuple[str, T]:
        """Remove item from list.

        Args:
            last: delete the last added item instead of the first

        Returns:
            the popped item
        """
        return cast(tuple[str, T], self._children.popitem(last=last))

    def pop(self, name: str, default: T | None = None) -> T | None:
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
            p.parent = None
        if p is None:
            return p
        else:
            return p.value

    def get_value(
        self,
    ) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        raise NotImplementedError()

    def get_dict(self) -> dict[str, T]:
        return cast(dict[str, T], {k: v for k, v in self._children.items()})

    def set_value(
        self,
        value: T,
    ) -> None:
        raise NotImplementedError()

    def set_dict(
        self,
        value: dict[str, T] | list[T],
    ) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(item, ParseBase):
                    self.__setitem__(key, item.value)
                    item.parent = self
                else:
                    obj = self.__getitem__(key)
                    obj.value = item
        else:
            for item in value:
                key = item.name
                self.__setitem__(key, item)
                item.parent = self

    def get_bits(self) -> bitarray:
        data = bitarray(endian="little")
        values = list(self._children.values())
        for value in values:
            data += value.bits
        return data

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
    def string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for value in self._children.values()])}]'

    @property
    def value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: T,
    ) -> None:
        self.set_value(value)

    @property
    def value_dict(self) -> dict[str, T]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_dict()

    @value_dict.setter
    def value_dict(
        self,
        value: dict[str, T] | list[T],
    ) -> None:
        self.set_dict(value)

    @property
    def children(self) -> OrderedDict[str, ParseBaseGeneric[T]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseBaseGeneric[T]]
        | dict[str, ParseBaseGeneric[T]]
        | list[ParseBaseGeneric[T]]
        | None,
    ) -> None:
        self.set_children(children=children)

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
        return f"{self._name}: {self.string_value}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    def __setitem__(self, name: str, value: T) -> None:
        if not isinstance(value, ParseBase):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        value.parent = self
        return self._children.__setitem__(name, value)

    def __getitem__(self, name: str) -> T:
        return self._children.__getitem__(name).value

    def __delitem__(self, name: str) -> None:
        return self._children.__delitem__(name)

    def __len__(self) -> int:
        return len(self._children)


class ParseValueDict(ParseDictGeneric[Any]):
    def __init__(
        self,
        name: str,
        value_dict: dict[str, Any] | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseBaseGeneric[Any] | None = None,
        children: OrderedDict[str, ParseBaseGeneric[Any]]
        | dict[str, ParseBaseGeneric[Any]]
        | list[ParseBaseGeneric[Any]]
        | None = None,
    ) -> None:
        super().__init__(
            name=name,
            value_dict=value_dict,
            data=data,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
            parent=parent,
            children=children,
        )


fieldDictT = TypeVar(
    "fieldDictT",
    bound=Union[
        OrderedDict[str, Any],
        OrderedDict[str, ParseBase],
    ],
)
fieldDictvalueT = OrderedDict[str, ParseBase]

fieldDictAssignT = Union[
    list[ParseBase],
    dict[str, Any],
    dict[str, ParseBase],
    OrderedDict[str, Any],
    OrderedDict[str, ParseBase],
    None,
]


class ParseDict(ParseDictGeneric[Any]):
    def __init__(
        self,
        name: str,
        value_dict: dict[str, Any] | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: Literal["little", "big"] = DEFAULT_ENDIANNESS,
        parent: ParseBaseGeneric[Any] | None = None,
        children: OrderedDict[str, ParseBaseGeneric[T]]
        | dict[str, ParseBaseGeneric[T]]
        | list[ParseBaseGeneric[T]]
        | None = None,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            value_dict=value_dict,
            string_format=string_format,
            parent=parent,
            children=children,
            endian=endian,
        )
