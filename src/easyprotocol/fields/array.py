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

    # def get_list(self) -> list[ParseBase[T]]:
    #     return list([v for v in self._children.values()])

    # def set_value(self, value: list[ParseBase[T]] | list[T] | None) -> None:
    #     if value is None:
    #         return
    #     for index, item in enumerate(value):
    #         if isinstance(item, ParseBase):
    #             if index < len(self._children):
    #                 self[index] = item
    #                 item.parent = self
    #             else:
    #                 self.append(item)
    #                 item.parent = self
    #         else:
    #             parse_base = self[index]
    #             parse_base.value = item  # type:ignore

    # @property  # type:ignore
    # def value(self) -> list[ParseBase[T]]:
    #     """Get the parsed value of the field.

    #     Returns:
    #         the value of the field
    #     """
    #     return self.get_value()

    # @value.setter
    # def value(self, value: list[ParseBase[T]] | list[T] | None) -> None:
    #     self.set_value(value=value)


# class ArrayField(ArrayFieldGeneric[T]):
#     def __init__(
#         self,
#         name: str,
#         count: UIntFieldGeneric[int] | int,
#         array_item_class: type[ParseBaseGeneric[T]],
#         data: dataT | None = None,
#         value_list: list[ParseBaseGeneric[T]] | None = None,
#         parent: ParseBaseGeneric[Any] | None = None,
#         children: list[ParseBaseGeneric[T]] | dict[str, ParseBaseGeneric[T]]| OrderedDict[str, ParseBaseGeneric[T]] | None = None,
#     ) -> None:
#         super().__init__(
#             name=name,
#             count=count,
#             array_item_class=array_item_class,
#             data=data,
#             value=value,
#             parent=parent,
#             children=children,
#         )

#     def get_value(self) -> list[valueT | None]:  # type:ignore
#         return list([v.value for v in self._children.values()])

#     def set_value(self, value: list[ParseBase[T]] | list[T] | None) -> None:
#         if value is None:
#             return
#         for index, item in enumerate(value):
#             if isinstance(item, ParseBase):
#                 if index < len(self._children):
#                     self[index] = item
#                     item.parent = self
#                 else:
#                     self.append(item)
#                     item.parent = self
#             else:
#                 if index < len(self):
#                     parse_base = self[index]
#                     parse_base.value = item  # type:ignore
#                 else:
#                     new_name = f"#{index}"
#                     new_item = self.array_item_class(name=new_name, value=item)  # type:ignore
#                     new_item.parent = self
#                     self._children[new_name] = new_item

#     @property  # type:ignore
#     def value(self) -> list[valueT | None]:
#         """Get the parsed value of the field.

#         Returns:
#             the value of the field
#         """
#         return self.get_value()

#     @value.setter
#     def value(self, value: list[ParseBase[T]] | list[T] | None) -> None:
#         self.set_value(value=value)
