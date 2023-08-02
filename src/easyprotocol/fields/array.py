"""Classes for parsing fields made up of an array of uniform sub-fields."""
from __future__ import annotations

from typing import Generic, Sequence, TypeVar, cast

from bitarray import bitarray

from easyprotocol.base.base import BaseField
from easyprotocol.base.list import ListFieldGeneric
from easyprotocol.base.utils import dataT, input_to_bitarray
from easyprotocol.base.value import ValueFieldGeneric
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

T = TypeVar("T")


class ArrayFieldGeneric(
    ListFieldGeneric[T],
    ValueFieldGeneric[T],
    BaseField,
    Generic[T],
):
    """Generic base class for parsing an array of uniform sub-fields."""

    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[BaseField],
        array_item_default: T,
        default: Sequence[T] | Sequence[BaseField] | None = None,
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        """Create generic base class for parsing an array of uniform sub-fields.

        Args:
            name: name of parsed object
            count: number of sub-fields
            array_item_class: class to use for sub-fields
            array_item_default: default value of sub-fields
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        self._count = count
        self._array_item_class = array_item_class
        self._array_item_default = array_item_default
        super().__init__(
            name=name,
            data=None,
            string_format=string_format,
        )
        if data is not None:
            self.parse(data=data)
        elif default is not None:
            self.create_default(default=default)
        else:
            if isinstance(count, int):
                if count > 0:
                    self.create_default(default=[array_item_default] * count)
            else:
                if count.value > 0:
                    self.create_default(default=[array_item_default] * count.value)

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bitarray(data=data)
        if isinstance(self._count, UIntFieldGeneric):
            count = self._count.value
        else:
            count = self._count
        for i in range(count):
            f = self._array_item_class(
                name=f"#{i}",
                default=self._array_item_default,
            )
            f.parent = self
            bit_data = f.parse(data=bit_data)
            self._children[f.name] = f
        return bit_data

    def create_default(self, default: Sequence[T] | Sequence[BaseField]) -> None:
        """Create an array of default valued sub-fields for this array field.

        Args:
            default: default values for the sub-fields
        """
        for i, item in enumerate(default):
            if isinstance(item, BaseField):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=item.value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast("T", item),
                )
            self._children[f.name] = f

    def set_value(
        self,
        value: T | Sequence[BaseField] | Sequence[T] | dict[str, BaseField] | dict[str, T],
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if isinstance(value, Sequence):
            for index in range(len(value)):  # pyright:ignore[reportUnknownArgumentType]
                item = value[index]  # pyright:ignore[reportUnknownVariableType]
                if isinstance(item, BaseField):
                    if index < len(self.children):
                        self[index] = item
                        item.set_parent(self)
                    else:
                        item = self._array_item_class(
                            name=f"#{index}",
                            default=item,
                        )
                        item.set_parent(self)
                        self._children[item.name] = item
                else:
                    self[index].value = item
        else:
            keys = list(
                value.keys(),  # noqa # pyright:ignore[reportGeneralTypeIssues,reportUnknownMemberType,reportUnknownArgumentType]
            )
            for index in range(len(keys)):
                key = keys[index]
                item = value[key]  # pyright:ignore[reportGeneralTypeIssues,reportUnknownVariableType]
                if isinstance(item, BaseField):
                    if index < len(self.children):
                        self[index] = item
                        item.set_parent(self)
                    else:
                        item = self._array_item_class(
                            name=f"#{index}",
                            default=item,
                        )
                        item.set_parent(self)
                        self._children[item.name] = item
                else:
                    self[index].value = item

    @property
    def value_list(self) -> list[T]:
        """Get a list of values from child fields.

        Returns:
            a list of values from child fields
        """
        return [v.value for v in self]
