"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations
from collections import OrderedDict
from typing import Any, MutableSequence
from easyprotocol.base.parse_object import ParseObject
from easyprotocol.base.utils import InputT, input_to_bytes
from bitarray import bitarray


class ParseList(ParseObject[ParseObject[Any]], MutableSequence[ParseObject[Any]]):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        data: InputT | None = None,
        parent: ParseObject[Any] | None = None,
        children: list[ParseObject[Any]] | OrderedDict[str, ParseObject[Any]] | None = None,
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
        )

        if children is not None:
            if isinstance(children, dict):
                self.children = children
            else:
                self.children = OrderedDict({val.name: val for val in children})
        if data is not None:
            self.parse(data)

    def parse(self, data: InputT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        for name, field in self._children.items():
            bit_data = field.parse(data=bit_data)
        return bit_data

    @property
    def name(self) -> str:
        """Get the name of the field.

        Returns:
            the name of the field
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def value(self) -> list[Any]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return list([v.value for f, v in self._children.items()])

    @value.setter
    def value(self, value: list[ParseObject[Any]] | list[Any]) -> None:
        if not isinstance(value, list):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        for index, item in enumerate(value):
            if isinstance(item, ParseObject):
                if index < len(self._children):
                    self[index] = item
                else:
                    self.append(item)
            else:
                parse_object = self[index]
                parse_object.value = item

    @property
    def bits(self) -> bitarray:
        """Get the bytes value of the field.

        Returns:
            the bytes value of the field
        """
        data = bitarray()
        values = list(self._children.values())
        for value in values:
            data += value.bits
        return data

    @property
    def formatted_value(self) -> str:
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

    def __getitem__(self, index: int | slice) -> ParseObject[Any]:
        return list(self._children.values())[index]

    def __delitem__(self, index: int | slice) -> None:
        p_o = list(self._children.values())[index]
        p_o.parent = None
        self._children.popitem(p_o)

    def __setitem__(self, index: int | slice, val: ParseObject[Any]):
        index_key = list(self._children.keys())[index]
        c = OrderedDict()
        for key in self._children:
            if key != index_key:
                c[key] = self._children[key]
            else:
                c[val.name] = val
                val.parent = self
        self._children = c

    def insert(self, index: int | slice, val: ParseObject[Any]):
        c = OrderedDict()
        for i, value in enumerate(self._children.values()):
            if index == i:
                c[val.name] = val
                val.parent = self
            c[value.name] = self._children[value.name]
        self._children = c

    def append(self, val: ParseObject[Any]):
        self._children[val.name] = val
        val.parent = self

    def __len__(self) -> int:
        return len(self._children)
