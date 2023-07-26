"""The base field dictionary."""
from __future__ import annotations

from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    MutableSequence,
    Sequence,
    SupportsIndex,
    cast,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.base_dict_field import BaseDictField
from easyprotocol.base.base_field import BaseParseField, T
from easyprotocol.base.base_list_field import BaseListField
from easyprotocol.base.base_types import collectionGenericT, fieldGenericT

# from easyprotocol.base.parse_generic_field_value_list import ParseGenericFieldValueList
from easyprotocol.base.base_value_field import BaseValueField
from easyprotocol.base.utils import DEFAULT_ENDIANNESS, dataT, endianT, input_to_bytes


class ListFieldGeneric(
    BaseListField[T],
    BaseParseField,
    MutableSequence[fieldGenericT[T]],
    Generic[T],
):
    """The base generic field dictionary."""

    def __init__(
        self,
        name: str,
        default: collectionGenericT[T] | Any | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create a generic field dictionary.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            data=None,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
        )

        if default is not None:
            self.set_value(default)
        if data is not None:
            self.parse(data)

    def parse(
        self,
        data: dataT,
    ) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
        for field in self._children.values():
            bit_data = field.parse(data=bit_data)
        return bit_data

    def insert(
        self,
        index: SupportsIndex,
        value: fieldGenericT[T],
    ) -> None:
        """Insert a new field into this list.

        Args:
            index: the index at which the new field will be inserted
            value: the new field to be inserted
        """
        c: dict[str, BaseParseField] = dict()
        existing_values = list(self._children.values())
        existing_values.insert(index, value)
        for v in existing_values:
            c[v.name] = v
        self.children = cast("dict[str, fieldGenericT[ T]]", c)

    def append(
        self,
        value: fieldGenericT[T] | Any,
    ) -> None:
        """Append a new field to this list.

        Args:
            value: the new field to be appended
        """
        self.children[value.name] = value

    def get_value(self) -> MutableSequence[fieldGenericT[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [item for item in self.children.values()]

    def set_value(
        self,
        value: collectionGenericT[T],
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if isinstance(value, dict):
            values = list(value.values())
            for index, (key, item) in enumerate(value.items()):
                item = values[index]
                if index < len(self._children):
                    if isinstance(
                        item,
                        (BaseListField, BaseDictField, BaseValueField, BaseParseField),
                    ):
                        self[index] = cast("fieldGenericT[T]", item)
                    else:
                        self[index].value = item
                    self[index]._set_parent_generic(self)
                else:
                    if isinstance(
                        item,
                        (BaseListField, BaseDictField, BaseValueField, BaseParseField),
                    ):
                        self.children[item.name] = cast("fieldGenericT[T]", item)
                    else:
                        self.children[key].value = item
                    self._children[item.name]._set_parent_generic(self)
        elif isinstance(value, (Sequence)):
            for index in range(len(value)):
                item = value[index]
                if index < len(self._children):
                    self[index] = item
                    self[index]._set_parent_generic(self)
                else:
                    self._children[item.name] = item
                    item._set_parent_generic(self)
        else:
            self._children.clear()

            index = 0
            item = value
            if index < len(self._children):
                self[index] = item
                self[index]._set_parent_generic(self)
            else:
                self._children[item.name] = item
                item._set_parent_generic(self)

    def get_bits_lsb(self) -> bitarray:
        """Get the bits of this field in least-significant-bit first format.

        Returns:
            lsb bits
        """
        data = bitarray(endian="little")
        values = list(self._children.values())
        for value in values:
            data += value.bits_lsb
        return data

    def get_children(self) -> dict[str, fieldGenericT[T]]:
        """Get the children of this field as an ordered dictionary.

        Returns:
            the children of this field
        """
        return cast("dict[str, fieldGenericT[T]]", self._children)

    def set_children(
        self,
        children: dict[str, fieldGenericT[T]]
        | Sequence[fieldGenericT[T]]
        | MutableSequence[fieldGenericT[T]]
        | dict[str, BaseParseField]
        | MutableSequence[BaseParseField]
        | Sequence[BaseParseField],
    ) -> None:
        """Set the children of this field using an ordered dictionary.

        Args:
            children: the new children for this field
        """
        self._children.clear()
        if isinstance(children, dict):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

    def get_parent(self) -> fieldGenericT[T] | None:
        """Get the field (if any) that is this field's parent.

        Returns:
            this field's parent (or None)
        """
        return cast("fieldGenericT[ T]", self._parent)

    def set_parent(
        self,
        parent: fieldGenericT[T] | None,
    ) -> None:
        """Set this field's parent.

        Args:
            parent: this field's new parent (or None)
        """
        self._parent = parent

    @property
    def parent(self) -> fieldGenericT[T] | None:
        """Get the field (if any) that is this field's parent.

        Returns:
            this field's parent (or None)
        """
        return self.get_parent()

    @parent.setter
    def parent(
        self,
        value: fieldGenericT[T] | None,
    ) -> None:
        self.set_parent(value)

    @property
    def children(self) -> dict[str, fieldGenericT[T]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: dict[str, fieldGenericT[T]],
    ) -> None:
        self.set_children(children=children)

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for value in self._children .values()])}]'

    @property
    def value(self) -> MutableSequence[fieldGenericT[T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: MutableSequence[fieldGenericT[T]] | MutableSequence[Any] | Any,
    ) -> None:
        self.set_value(value=value)

    @overload
    def __getitem__(
        self,
        index: SupportsIndex,
    ) -> fieldGenericT[T]:
        """Get a field from this class by index.

        Args:
            index: index of the sub-field to retrieve
        """
        ...

    @overload
    def __getitem__(
        self,
        index: slice,
    ) -> MutableSequence[fieldGenericT[T]]:
        """Get fields from this class by index.

        Args:
            index: indices of the sub-fields to retrieve
        """
        ...

    def __getitem__(
        self,
        index: SupportsIndex | slice,
    ) -> fieldGenericT[T] | MutableSequence[fieldGenericT[T]]:
        """Get a field or fields from this class by index.

        Args:
            index: index or indices of the sub-field(s) to retrieve

        Returns:
            the field or fields
        """
        vs = list(self.children.values())[index]
        if isinstance(vs, list):
            return [v for v in vs]
        else:
            return vs

    def __delitem__(
        self,
        index: SupportsIndex | slice,
    ) -> None:
        """Delete one or more items from this list by index.

        Args:
            index: index or slice to delete
        """
        item = list(self._children.values())[index]
        if isinstance(item, list):
            for x in item:
                x._set_parent_generic(None)
                self._children.pop(x._name)
        else:
            item._set_parent_generic(None)
            self._children = dict({k: v for k, v in self._children.items() if k != item.name})

    @overload
    def __setitem__(
        self,
        index: SupportsIndex,
        value: fieldGenericT[T] | Any,
    ) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def __setitem__(
        self,
        index: slice,
        value: Iterable[fieldGenericT[T]] | Iterable[Any],
    ) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def __setitem__(
        self,
        index: SupportsIndex | slice,
        value: fieldGenericT[T] | Iterable[fieldGenericT[T]] | Any | Iterable[Any],
    ) -> None:
        """Set one or more items in this list to new values.

        Args:
            index: one ore more indices
            value: one or more values
        """
        indexed_keys = list(self._children.keys())[index]
        c: dict[str, BaseParseField] = dict()
        for existing_key in self.children:
            if isinstance(indexed_keys, str):
                if isinstance(value, (BaseListField, BaseDictField, BaseValueField)):
                    if existing_key != indexed_keys:
                        c[existing_key] = self.children[existing_key]
                    else:
                        c[indexed_keys] = cast("fieldGenericT[T]", value)
                else:
                    if existing_key != indexed_keys:
                        c[existing_key] = self.children[existing_key]
                    else:
                        c[indexed_keys] = self.children[existing_key]
                        c[indexed_keys].value = value
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        if isinstance(value[i], BaseParseField):
                            sub_value = value[i]
                            if existing_key != sub_key:
                                c[existing_key] = self.children[existing_key]
                            else:
                                c[sub_value._name] = sub_value
                                sub_value._set_parent_generic(self)
                        else:
                            sub_value = value[i]
                            if existing_key != sub_key:
                                c[existing_key] = self.children[existing_key]
                            else:
                                c[sub_value._name].value = sub_value
                                sub_value._set_parent_generic(self)
        self.children = cast("dict[str,fieldGenericT[T]]", c)

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field list
        """
        return len(self._children)

    def __iter__(self) -> Iterator[fieldGenericT[T]]:
        """Iterate over the fields in this list.

        Returns:
            field iterator
        """
        return self.children.values().__iter__()


class ListField(
    ListFieldGeneric[Any],
    BaseParseField,
):
    """The base field list."""

    ...
