from __future__ import annotations

from collections import OrderedDict
from typing import Any, Generic, TypeVar

from bitarray import bitarray

from easyprotocol.base.parse_base import ParseBaseGeneric
from easyprotocol.base.parse_list import ParseListGeneric
from easyprotocol.base.utils import dataT, input_to_bytes
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

T = TypeVar("T", bound=Any)


class ArrayField(ParseListGeneric[T]):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseBaseGeneric[T]],
        data: dataT | None = None,
        value_list: list[T] | None = None,
        parent: ParseBaseGeneric[Any] | None = None,
        children: list[ParseBaseGeneric[T]]
        | dict[str, ParseBaseGeneric[T]]
        | OrderedDict[str, ParseBaseGeneric[T]]
        | None = None,
    ) -> None:
        self._count = count
        self.array_item_class = array_item_class
        super().__init__(
            name=name,
            data=data,
            parent=parent,
            children=children,
            value_list=value_list,
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
