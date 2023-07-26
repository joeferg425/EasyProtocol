"""Classes for parsing fields made up of an array of uniform sub-fields."""
from __future__ import annotations

from typing import (
    Any,
    Generic,
    Iterable,
    Mapping,
    Sequence,
    SupportsIndex,
    TypeVar,
    cast,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.array_field import BaseArrayField, BaseArrayValueField
from easyprotocol.base.base_dict_field import BaseDictField
from easyprotocol.base.base_field import BaseParseField
from easyprotocol.base.base_list_field import BaseListField
from easyprotocol.base.base_types import fieldGenericT
from easyprotocol.base.base_value_field import BaseValueField
from easyprotocol.base.utils import dataT, input_to_bytes
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

T = TypeVar("T")


class ArrayField(
    BaseArrayField[T],
    BaseParseField,
    Generic[T],
):
    """Generic base class for parsing an array of uniform sub-fields."""

    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[fieldGenericT[T]],
        array_item_default: T,
        default: Sequence[T] | Sequence[fieldGenericT[T]] | None = None,
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

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
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

    def create_default(self, default: Sequence[T] | Sequence[fieldGenericT[T]]) -> None:
        """Create an array of default valued sub-fields for this array field.

        Args:
            default: default values for the sub-fields
        """
        for i, item in enumerate(default):
            if isinstance(item, (BaseValueField, BaseDictField, BaseListField)):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast("BaseValueField[T]", item).value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast("T", item),
                )
            self._children[f.name] = f

    def set_value(
        self,
        value: Sequence[fieldGenericT[T] | Any]
        | dict[
            str,
            fieldGenericT[T] | Any,
        ],
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if isinstance(value, (Sequence)):
            for index in range(len(value)):
                item = value[index]
                if isinstance(item, BaseParseField):
                    if index < len(self.children):
                        self[index] = item
                        item._set_parent_generic(self)
                    else:
                        item = self._array_item_class(
                            name=f"#{index}",
                            default=item,
                        )
                        item._set_parent_generic(self)
                        self._children[item.name] = item
                else:
                    self[index].value = item
        else:
            keys = list(value.keys())
            for index in range(len(keys)):
                key = keys[index]
                item = value[key]
                if isinstance(item, BaseParseField):
                    if index < len(self.children):
                        self[index] = item
                        item._set_parent_generic(self)
                    else:
                        item = self._array_item_class(
                            name=f"#{index}",
                            default=item,
                        )
                        item._set_parent_generic(self)
                        self._children[item.name] = item
                else:
                    self[index].value = item

    @overload
    def get(
        self,
        index: SupportsIndex,
    ) -> Any | Iterable[Any] | Mapping[str, Any]:
        """Get the parsed value of the field.

        Args:
            index: index or of the sub-field to retrieve
        """
        ...

    @overload
    def get(self, index: slice) -> Iterable[Any | Iterable[Any] | Mapping[str, Any]]:
        """Get the parsed values of the fields.

        Args:
            index: indices or of the sub-field to retrieve
        """
        ...

    def get(
        self, index: SupportsIndex | slice
    ) -> Any | Iterable[Any] | Mapping[str, Any] | Iterable[Any | Iterable[Any] | Mapping[str, Any]]:
        """Get the parsed value(s) of the field(s).

        Args:
            index: index(s) or of the sub-field(s) to retrieve

        Returns:
            the value(s) of the field(s)
        """
        vs = list(self.children.values())[index]
        if isinstance(vs, list):
            return [v.value for v in vs]
        else:
            return vs.value

    @overload
    def set(self, index: SupportsIndex, value: Any | Iterable[Any] | Mapping[str, Any]) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def set(self, index: slice, value: Iterable[Any | Iterable[Any] | Mapping[str, Any]]) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def set(
        self,
        index: SupportsIndex | slice,
        value: Any | Iterable[Any] | Mapping[str, Any] | Iterable[Any | Iterable[Any] | Mapping[str, Any]],
    ) -> None:
        """Set one or more items in this list to new values.

        Args:
            index: one ore more indices
            value: one or more values
        """
        indexed_keys = list(self._children.keys())[index]
        c: dict[str, fieldGenericT[T]] = dict()
        for existing_key in self.children:
            if isinstance(indexed_keys, str):
                c[existing_key] = self.children[existing_key]
                c[existing_key].value = value
            else:
                if isinstance(value, list):
                    for _, key in enumerate(indexed_keys):
                        # s = cast("valueGenericT[T]", value[i])
                        c[key] = self.children[existing_key]
                        c[key].value = value
        self.children = c


class ArrayValueField(
    BaseArrayValueField[T],
    BaseParseField,
    Generic[T],
):
    """Generic base class for parsing an array of uniform sub-fields."""

    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[BaseValueField[T]],
        array_item_default: T,
        default: Sequence[T] | Sequence[BaseValueField[T]] | None = None,
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

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
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

    def create_default(self, default: Sequence[T] | Sequence[BaseValueField[T]]) -> None:
        """Create an array of default valued sub-fields for this array field.

        Args:
            default: default values for the sub-fields
        """
        for i, item in enumerate(default):
            if isinstance(item, (BaseValueField, BaseDictField, BaseListField)):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast("BaseValueField[T]", item).value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast("T", item),
                )
            self._children[f.name] = f

    def set_value(
        self,
        value: Sequence[BaseValueField[T] | Any]
        | dict[
            str,
            BaseValueField[T] | Any,
        ],
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if isinstance(value, (Sequence)):
            for index in range(len(value)):
                item = value[index]
                if isinstance(item, BaseParseField):
                    if index < len(self.children):
                        self[index] = item
                        item._set_parent_generic(self)
                    else:
                        item = self._array_item_class(
                            name=f"#{index}",
                            default=item,
                        )
                        item._set_parent_generic(self)
                        self._children[item.name] = item
                else:
                    self[index].value = item
        else:
            keys = list(value.keys())
            for index in range(len(keys)):
                key = keys[index]
                item = value[key]
                if isinstance(item, BaseParseField):
                    if index < len(self.children):
                        self[index] = item
                        item._set_parent_generic(self)
                    else:
                        item = self._array_item_class(
                            name=f"#{index}",
                            default=item,
                        )
                        item._set_parent_generic(self)
                        self._children[item.name] = item
                else:
                    self[index].value = item

    @overload
    def get(
        self,
        index: SupportsIndex,
    ) -> Any | Iterable[Any] | Mapping[str, Any]:
        """Get the parsed value of the field.

        Args:
            index: index or of the sub-field to retrieve
        """
        ...

    @overload
    def get(self, index: slice) -> Iterable[Any | Iterable[Any] | Mapping[str, Any]]:
        """Get the parsed values of the fields.

        Args:
            index: indices or of the sub-field to retrieve
        """
        ...

    def get(
        self, index: SupportsIndex | slice
    ) -> Any | Iterable[Any] | Mapping[str, Any] | Iterable[Any | Iterable[Any] | Mapping[str, Any]]:
        """Get the parsed value(s) of the field(s).

        Args:
            index: index(s) or of the sub-field(s) to retrieve

        Returns:
            the value(s) of the field(s)
        """
        vs = list(self.children.values())[index]
        if isinstance(vs, list):
            return [v.value for v in vs]
        else:
            return vs.value

    @overload
    def set(self, index: SupportsIndex, value: Any | Iterable[Any] | Mapping[str, Any]) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def set(self, index: slice, value: Iterable[Any | Iterable[Any] | Mapping[str, Any]]) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def set(
        self,
        index: SupportsIndex | slice,
        value: Any | Iterable[Any] | Mapping[str, Any] | Iterable[Any | Iterable[Any] | Mapping[str, Any]],
    ) -> None:
        """Set one or more items in this list to new values.

        Args:
            index: one ore more indices
            value: one or more values
        """
        indexed_keys = list(self._children.keys())[index]
        c: dict[str, BaseValueField[T]] = dict()
        for existing_key in self.children:
            if isinstance(indexed_keys, str):
                c[existing_key] = self.children[existing_key]
                c[existing_key].value = value
            else:
                if isinstance(value, list):
                    for _, key in enumerate(indexed_keys):
                        # s = cast("valueGenericT[T]", value[i])
                        c[key] = self.children[existing_key]
                        c[key].value = value
        self.children = c
