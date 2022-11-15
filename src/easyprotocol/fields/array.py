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
        count_field: UIntField,
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
        self.count_field = count_field
        self.array_item_class = array_item_class

    def parse(self, data: InputT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        count = self.count_field.value
        for i in range(count):
            f = self.array_item_class(f"f{i}")
            bit_data = f.parse(data=bit_data)
            self.append(f)
        return bit_data
