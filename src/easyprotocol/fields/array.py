from __future__ import annotations

from collections import OrderedDict
from typing import Any, Generic, TypeVar

from bitarray import bitarray

from easyprotocol.base.parse_list import ParseListGeneric
from easyprotocol.base.parse_object import ParseObjectGeneric, T
from easyprotocol.base.utils import I, input_to_bytes
from easyprotocol.fields.unsigned_int import UIntFieldGeneric


class ArrayFieldGeneric(ParseListGeneric[T], Generic[T]):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseObjectGeneric[T]],
        data: I | None = None,
        value: list[ParseObjectGeneric[T]] | list[T] | None = None,
        parent: ParseObjectGeneric[Any] | None = None,
        children: list[ParseObjectGeneric[T]] | OrderedDict[str, ParseObjectGeneric[T]] | None = None,
    ) -> None:
        self._count = count
        self.array_item_class = array_item_class
        super().__init__(
            name=name,
            data=data,
            parent=parent,
            children=children,
            value=value,  # type:ignore
        )

    def parse(self, data: I) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, UIntFieldGeneric):
            count = self._count.value
        else:
            count = self._count
        if count is not None:
            for i in range(count):
                f = self.array_item_class(f"#{i}")
                bit_data = f.parse(data=bit_data)
                self.append(f)
        return bit_data

    def _get_value(self) -> list[ParseObjectGeneric[T]]:  # type:ignore
        return list([v for v in self._children.values()])

    def _set_value(self, value: list[ParseObjectGeneric[T]] | list[T] | None) -> None:
        if value is None:
            return
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
                parse_object.value = item  # type:ignore

    @property  # type:ignore
    def value(self) -> list[ParseObjectGeneric[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: list[ParseObjectGeneric[T]] | list[T] | None) -> None:
        self._set_value(value=value)


class ArrayField(ArrayFieldGeneric[T]):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseObjectGeneric[T]],
        data: I | None = None,
        value: list[ParseObjectGeneric[T]] | list[T] | None = None,
        parent: ParseObjectGeneric[Any] | None = None,
        children: list[ParseObjectGeneric[T]] | OrderedDict[str, ParseObjectGeneric[T]] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            count=count,
            array_item_class=array_item_class,
            data=data,
            value=value,
            parent=parent,
            children=children,
        )

    def _get_value(self) -> list[T | None]:  # type:ignore
        return list([v.value for v in self._children.values()])

    def _set_value(self, value: list[ParseObjectGeneric[T]] | list[T] | None) -> None:
        if value is None:
            return
        for index, item in enumerate(value):
            if isinstance(item, ParseObjectGeneric):
                if index < len(self._children):
                    self[index] = item
                    item.parent = self
                else:
                    self.append(item)
                    item.parent = self
            else:
                if index < len(self):
                    parse_object = self[index]
                    parse_object.value = item  # type:ignore
                else:
                    new_name = f"#{index}"
                    new_item = self.array_item_class(name=new_name, value=item)  # type:ignore
                    new_item.parent = self
                    self._children[new_name] = new_item

    @property  # type:ignore
    def value(self) -> list[T | None]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_value()

    @value.setter
    def value(self, value: list[ParseObjectGeneric[T]] | list[T] | None) -> None:
        self._set_value(value=value)
