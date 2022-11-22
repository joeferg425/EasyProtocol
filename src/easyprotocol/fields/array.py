from __future__ import annotations
from typing import Any, TypeVar
from easyprotocol.base.parse_list import ParseList
from easyprotocol.base.parse_object import ParseObject
from easyprotocol.base.utils import InputT, input_to_bytes
from bitarray import bitarray
from collections import OrderedDict
from easyprotocol.fields.unsigned_int import UIntField

T = TypeVar("T")


class ArrayField(ParseList):
    def __init__(
        self,
        name: str,
        count: UIntField | int,
        array_item_class: type[ParseObject[Any]],
        data: InputT | None = None,
        parent: ParseObject[Any] | None = None,
        children: list[ParseObject[T]] | OrderedDict[str, ParseObject[T]] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            parent=parent,
            children=children,
        )
        self._count = count
        self.array_item_class = array_item_class

    def parse(self, data: InputT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, UIntField):
            count = self._count.value
        else:
            count = self._count
        for i in range(count):
            f = self.array_item_class(f"#{i}")
            bit_data = f.parse(data=bit_data)
            self.append(f)
        return bit_data

    @property
    def value(self) -> list[T]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return list([v.value for f, v in self._children.items()])

    @value.setter
    def value(self, value: list[ParseObject[Any]] | list[T]) -> None:
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
