"""This class is the basic parsing class for list types."""
from __future__ import annotations

from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    MutableSequence,
    Sequence,
    SupportsIndex,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.base import BaseField, T, defaultT
from easyprotocol.base.utils import DEFAULT_ENDIANNESS, dataT, endianT, input_to_bytes


class ListFieldGeneric(
    BaseField,
    MutableSequence[BaseField],
    Generic[T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: defaultT | None = (),
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

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
            data=data,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
            default=default,
        )

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
        value: Any | BaseField,
    ) -> None:
        """Insert a new field into this list.

        Args:
            index: the index at which the new field will be inserted
            value: the new field to be inserted
        """
        c: dict[str, BaseField] = dict()
        existing_values = list(self._children.values())
        existing_values.insert(index, value)
        value.set_parent(self)
        for v in existing_values:
            c[v._name] = v
        self._children = c

    def append(
        self,
        value: Any | BaseField,
    ) -> None:
        """Append a new field to this list.

        Args:
            value: the new field to be appended
        """
        self._children[value.name] = value

    def get_value(self) -> Sequence[BaseField]:
        """Get the parsed fields that are part of this field.

        Returns:
            the value(s) of this field
        """
        return [item for item in self._children.values()]

    def set_value(
        self,
        value: defaultT,
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields to assign to this field
        """
        if isinstance(value, dict):
            values = list(value.values())
            for index in range(len(value)):
                item = values[index]
                if index < len(self._children):
                    self[index] = item
                    item.set_parent(self)
                else:
                    self._children[item.name] = item
                    item.set_parent(self)
        if isinstance(value, Sequence):
            for index in range(len(value)):
                item = value[index]
                if index < len(self._children):
                    self[index] = item
                    item.set_parent(self)
                else:
                    self._children[item.name] = item
                    item.set_parent(self)

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

    def get_value_as_string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        s = f'[{", ".join([str(value) for value in self._children .values()])}]'
        return self.string_format.format(s)

    @property
    def value(self) -> Sequence[BaseField]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: defaultT,
    ) -> None:
        self.set_value(value=value)

    @overload
    def __getitem__(
        self,
        index: SupportsIndex,
    ) -> BaseField:
        """Get a field from this class by index.

        Args:
            index: index of the sub-field to retrieve
        """
        ...

    @overload
    def __getitem__(
        self,
        index: slice,
    ) -> MutableSequence[BaseField]:
        """Get fields from this class by index.

        Args:
            index: indices of the sub-fields to retrieve
        """
        ...

    def __getitem__(
        self,
        index: SupportsIndex | slice,
    ) -> BaseField | MutableSequence[BaseField]:
        """Get a field or fields from this class by index.

        Args:
            index: index or indices of the sub-field(s) to retrieve

        Returns:
            the field or fields
        """
        vs = list(self._children.values())[index]
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
                x.set_parent(None)
                self._children.pop(x._name)
        else:
            item.set_parent(None)
            self._children = dict({k: v for k, v in self._children.items() if k != item.name})

    @overload
    def __setitem__(
        self,
        index: SupportsIndex,
        value: BaseField,
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
        value: Iterable[BaseField],
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
        value: BaseField | Iterable[BaseField],
    ) -> None:
        """Set one or more items in this list to new values.

        Args:
            index: one ore more indices
            value: one or more values
        """
        indexed_keys = list(self._children.keys())[index]
        c: dict[str, BaseField] = dict()
        for existing_key in self._children:
            if isinstance(indexed_keys, str) and isinstance(value, BaseField):
                if existing_key != indexed_keys:
                    c[existing_key] = self._children[existing_key]
                else:
                    c[indexed_keys] = value
                    value.set_parent(self)
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        sub_value = value[i]
                        if existing_key != sub_key:
                            c[existing_key] = self._children[existing_key]
                        else:
                            c[sub_value._name] = sub_value
                            sub_value.set_parent(self)
        self._children = c

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field list
        """
        return len(self._children)

    def __iter__(self) -> Iterator[BaseField]:
        """Iterate over the fields in this list.

        Returns:
            field iterator
        """
        return self._children.values().__iter__()

    def get_value_concatenated(self) -> T:
        """Get list values as a single concatenated value (if supported).

        Raises:
            NotImplementedError: until implemented in supporting field
        """
        raise NotImplementedError()

    @property
    def value_concatenated(self) -> T:
        """Get list values as a single concatenated value (if supported).

        Returns:
            list values as a single concatenated value (if supported)
        """
        return self.get_value_concatenated()

    @property
    def value_list(self) -> list[T]:
        """Get values as a list of value types.

        Returns:
            values as a list of value types
        """
        return [v.value for v in self]

    @property
    def value_dict(self) -> dict[str, T]:
        """Get values as a list of value types.

        Returns:
            values as a list of value types
        """
        return {v.name: v.value for v in self}


class ListField(
    ListFieldGeneric[Any],
    BaseField,
):
    def __init__(
        self,
        name: str,
        default: defaultT | None = (),
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            default=default,
            data=data,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
        )
