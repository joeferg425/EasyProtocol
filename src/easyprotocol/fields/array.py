from __future__ import annotations

from collections import OrderedDict
from typing import Any, TypeVar, Union

from bitarray import bitarray

from easyprotocol.base.parse_field_dict import ParseDictGeneric
from easyprotocol.base.parse_field_list import ParseValueList
from easyprotocol.base.parse_list_generic import ParseListGeneric
from easyprotocol.base.parse_value_generic import ParseValueGeneric
from easyprotocol.base.utils import dataT, input_to_bytes
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

T = TypeVar("T", bound=Any)
ParseGenericUnion = Union[ParseValueGeneric[T], ParseDictGeneric[T], ParseListGeneric[T]]


class ParseArrayField(ParseValueList[T]):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseValueGeneric[T]],
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        self._count = count
        self.array_item_class = array_item_class
        super().__init__(
            name=name,
            data=data,
            string_format=string_format,
        )

    def parse(self, data: dataT) -> bitarray:
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
                self._children[f.name] = f
        return bit_data


class ParseValueArrayField(ParseValueList[T]):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseValueGeneric[T]],
        default: list[T] | dict[str, ParseGenericUnion[T]] | OrderedDict[str, ParseGenericUnion[T]] | None = None,
        data: dataT | None = None,
    ) -> None:
        self._count = count
        self.array_item_class = array_item_class
        super().__init__(
            name=name,
            data=data,
        )

    def parse(self, data: dataT) -> bitarray:
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
                self._children[f.name] = f
        return bit_data

    # def get_value(self) -> list[T]:
    #     return [v for v in self.children.values()]

    # def set_value(self, value: str) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
    #     if value is None:
    #         return
    #     for index, item in enumerate(value):
    #         if index < len(self._children):
    #             kid = cast(CharField, self[index])
    #             kid.value = item
    #         else:
    #             f = self.array_item_class(f"#{index}")
    #             f.value = item
    #             self._children[f.name] = f

    # @property
    # def value(self) -> str:  # pyright:ignore[reportIncompatibleMethodOverride]
    #     return self.get_value()

    # @value.setter
    # def value(self, value: str) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
    #     self.set_value(value=value)
