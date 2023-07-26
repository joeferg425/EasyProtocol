"""The base parsing object for handling parsing in a convenient package."""
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

from easyprotocol.base.base_dict_field import BaseDictField, T
from easyprotocol.base.base_field import BaseParseField
from easyprotocol.base.base_list_field import BaseListField
from easyprotocol.base.base_types import (
    collectionGenericT,
    fieldGenericT,
    valueGenericT,
)
from easyprotocol.base.base_value_field import BaseValueField
from easyprotocol.base.utils import DEFAULT_ENDIANNESS, dataT, endianT, input_to_bytes

# T = TypeVar("T")
# valueGenericT = Sequence[T]


class BaseArrayField(
    BaseParseField,
    MutableSequence[fieldGenericT[T]],
    Generic[T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: Sequence[BaseParseField] | dict[str, BaseParseField] | Sequence[Any] | dict[str, Any] | None = None,
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
            data=None,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
        )
        if data is not None:
            self.parse(data)
        if default is not None:
            self.value = default

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
        self.children = cast("dict[str, fieldGenericT[T]]", c)

    def append(
        self,
        value: fieldGenericT[T],
    ) -> None:
        """Append a new field to this list.

        Args:
            value: the new field to be appended
        """
        self.children[value.name] = value

    def get_value(self) -> valueGenericT[T]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [v.value for v in self.children.values()]

    def set_value(
        self,
        value: collectionGenericT[T],
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if isinstance(value, Sequence):
            for index in range(len(value)):
                item = value[index]
                if index < len(self.children):
                    self[index] = item
                    item._set_parent_generic(self)
                else:
                    self.children[item.name] = item
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

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for value in self._children .values()])}]'

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self.bits_lsb.tobytes()

    def __str__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"{self._name}: {self.string_value}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    @property
    def value(self) -> valueGenericT[T]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: Sequence[valueGenericT[T]]
        | Sequence[fieldGenericT[T]]
        | dict[str, valueGenericT[T]]
        | dict[str, fieldGenericT[T]],
    ) -> None:
        self.set_value(value=value)

    def get_field_at(
        self,
        index: int,
    ) -> fieldGenericT[T]:
        """Get a field by index.

        Args:
            index: index or of the sub-field to retrieve

        Returns:
            the field
        """
        children = cast("list[fieldGenericT[T]]", list(self._children.values()))
        return children[index]

    @overload
    def __getitem__(
        self,
        index: SupportsIndex,
    ) -> fieldGenericT[T]:
        """Get the parsed value of the field.

        Args:
            index: index or of the sub-field to retrieve
        """
        ...

    @overload
    def __getitem__(self, index: slice) -> MutableSequence[fieldGenericT[T]]:
        """Get the parsed values of the fields.

        Args:
            index: indices or of the sub-field to retrieve
        """
        ...

    def __getitem__(self, index: SupportsIndex | slice) -> fieldGenericT[T] | MutableSequence[fieldGenericT[T]]:
        """Get the parsed value(s) of the field(s).

        Args:
            index: index(s) or of the sub-field(s) to retrieve

        Returns:
            the value(s) of the field(s)
        """
        vs = list(self.children.values())[index]
        return vs

    @overload
    def get(
        self,
        index: SupportsIndex,
    ) -> Any:
        """Get the parsed value of the field.

        Args:
            index: index or of the sub-field to retrieve
        """
        ...

    @overload
    def get(self, index: slice) -> Iterable[Any]:
        """Get the parsed values of the fields.

        Args:
            index: indices or of the sub-field to retrieve
        """
        ...

    def get(self, index: SupportsIndex | slice) -> Any | Iterable[Any]:
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

    def __delitem__(self, index: int | slice) -> None:
        """Delete one or more items from this list by index.

        Args:
            index: index or slice to delete
        """
        item = list(self.children.values())[index]
        if isinstance(item, list):
            for x in item:
                x._set_parent_generic(None)
                self._children.pop(x._name)
        else:
            item._set_parent_generic(None)
            self._children = dict({k: v for k, v in self._children.items() if k != item.name})

    @overload
    def __setitem__(self, index: SupportsIndex, value: fieldGenericT[T]) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def __setitem__(self, index: slice, value: fieldGenericT[T] | Iterable[fieldGenericT[T]]) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def __setitem__(
        self,
        index: SupportsIndex | slice,
        value: fieldGenericT[T] | Iterable[fieldGenericT[T]],
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
                if isinstance(value, (BaseListField, BaseDictField, BaseValueField, BaseParseField)):
                    if existing_key != indexed_keys:
                        c[existing_key] = self.children[existing_key]
                    else:
                        old = self.children[value._name]
                        old._set_parent_generic(None)
                        c[value.name] = cast("fieldGenericT[T]", value)
                        value._set_parent_generic(self)
                else:
                    c[existing_key] = self.children[existing_key]
                    c[existing_key].value = value
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        if isinstance(value[i], (BaseListField, BaseDictField, BaseValueField, BaseParseField)):
                            s = value[i]
                            if existing_key != sub_key:
                                c[existing_key] = self.children[existing_key]
                            else:
                                c[s.name] = s
                                s._set_parent_generic(self)
                        else:
                            s = cast("valueGenericT[T]", value[i])
                            c[existing_key] = self.children[existing_key]
                            c[existing_key].value = value
        self.children = c

    @overload
    def set(self, index: SupportsIndex, value: Any) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def set(self, index: slice, value: Iterable[Any]) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def set(
        self,
        index: SupportsIndex | slice,
        value: Any | Iterable[Any],
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

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field list
        """
        return len(self._children)

    def get_children(self) -> dict[str, fieldGenericT[T]]:
        """Get the children of this field as an ordered dictionary.

        Returns:
            the children of this field
        """
        return cast(
            "dict[str,fieldGenericT[T],]",
            self._children,
        )

    def set_children(
        self,
        children: dict[str, fieldGenericT[T]] | Sequence[fieldGenericT[T]] | None,
    ) -> None:
        """Set the children of this field using an ordered dictionary.

        Args:
            children: the new children for this field
        """
        self._children.clear()
        if isinstance(children, (dict, dict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

    def get_parent(self) -> fieldGenericT[Any] | None:
        """Get the field (if any) that is this field's parent.

        Returns:
            this field's parent (or None)
        """
        return cast("fieldGenericT[Any]", self._parent)

    def set_parent(self, parent: fieldGenericT[T] | None) -> None:
        """Set this field's parent.

        Args:
            parent: this field's new parent (or None)
        """
        self._parent = parent

    @property
    def children(self) -> dict[str, fieldGenericT[Any]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: dict[str, fieldGenericT[Any]] | Sequence[fieldGenericT[Any]],
    ) -> None:
        self.set_children(children=children)

    def __iter__(self) -> Iterator[fieldGenericT[T]]:
        """Iterate over the fields in this list.

        Returns:
            field iterator
        """
        return cast("Iterator[fieldGenericT[T]]", self._children.values().__iter__())


class BaseArrayValueField(
    BaseParseField,
    MutableSequence[BaseValueField[T]],
    Generic[T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: Sequence[BaseParseField] | dict[str, BaseParseField] | Sequence[Any] | dict[str, Any] | None = None,
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
            data=None,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
        )
        if data is not None:
            self.parse(data)
        if default is not None:
            self.value = default

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
        self.children = cast("dict[str, fieldGenericT[T]]", c)

    def append(
        self,
        value: fieldGenericT[T],
    ) -> None:
        """Append a new field to this list.

        Args:
            value: the new field to be appended
        """
        self.children[value.name] = value

    def get_value(self) -> valueGenericT[T]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [v.value for v in self.children.values()]

    def set_value(
        self,
        value: collectionGenericT[T],
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if isinstance(value, Sequence):
            for index in range(len(value)):
                item = value[index]
                if index < len(self.children):
                    self[index] = item
                    item._set_parent_generic(self)
                else:
                    self.children[item.name] = item
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

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for value in self._children .values()])}]'

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self.bits_lsb.tobytes()

    def __str__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"{self._name}: {self.string_value}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    @property
    def value(self) -> valueGenericT[T]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: Sequence[valueGenericT[T]]
        | Sequence[fieldGenericT[T]]
        | dict[str, valueGenericT[T]]
        | dict[str, fieldGenericT[T]],
    ) -> None:
        self.set_value(value=value)

    def get_field_at(
        self,
        index: int,
    ) -> fieldGenericT[T]:
        """Get a field by index.

        Args:
            index: index or of the sub-field to retrieve

        Returns:
            the field
        """
        children = cast("list[fieldGenericT[T]]", list(self._children.values()))
        return children[index]

    @overload
    def __getitem__(
        self,
        index: SupportsIndex,
    ) -> BaseValueField[T]:
        """Get the parsed value of the field.

        Args:
            index: index or of the sub-field to retrieve
        """
        ...

    @overload
    def __getitem__(self, index: slice) -> MutableSequence[BaseValueField[T]]:
        """Get the parsed values of the fields.

        Args:
            index: indices or of the sub-field to retrieve
        """
        ...

    def __getitem__(self, index: SupportsIndex | slice) -> BaseValueField[T] | MutableSequence[BaseValueField[T]]:
        """Get the parsed value(s) of the field(s).

        Args:
            index: index(s) or of the sub-field(s) to retrieve

        Returns:
            the value(s) of the field(s)
        """
        vs = list(self.children.values())[index]
        return cast("list[BaseValueField[T]]", vs)

    @overload
    def get(
        self,
        index: SupportsIndex,
    ) -> Any:
        """Get the parsed value of the field.

        Args:
            index: index or of the sub-field to retrieve
        """
        ...

    @overload
    def get(self, index: slice) -> Iterable[Any]:
        """Get the parsed values of the fields.

        Args:
            index: indices or of the sub-field to retrieve
        """
        ...

    def get(self, index: SupportsIndex | slice) -> Any | Iterable[Any]:
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

    def __delitem__(self, index: int | slice) -> None:
        """Delete one or more items from this list by index.

        Args:
            index: index or slice to delete
        """
        item = list(self.children.values())[index]
        if isinstance(item, list):
            for x in item:
                x._set_parent_generic(None)
                self._children.pop(x._name)
        else:
            item._set_parent_generic(None)
            self._children = dict({k: v for k, v in self._children.items() if k != item.name})

    @overload
    def __setitem__(self, index: SupportsIndex, value: fieldGenericT[T]) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def __setitem__(self, index: slice, value: fieldGenericT[T] | Iterable[fieldGenericT[T]]) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def __setitem__(
        self,
        index: SupportsIndex | slice,
        value: fieldGenericT[T] | Iterable[fieldGenericT[T]],
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
                if isinstance(value, (BaseListField, BaseDictField, BaseValueField, BaseParseField)):
                    if existing_key != indexed_keys:
                        c[existing_key] = self.children[existing_key]
                    else:
                        old = self.children[value._name]
                        old._set_parent_generic(None)
                        c[value.name] = cast("fieldGenericT[T]", value)
                        value._set_parent_generic(self)
                else:
                    c[existing_key] = self.children[existing_key]
                    c[existing_key].value = value
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        if isinstance(value[i], (BaseListField, BaseDictField, BaseValueField, BaseParseField)):
                            s = value[i]
                            if existing_key != sub_key:
                                c[existing_key] = self.children[existing_key]
                            else:
                                c[s.name] = s
                                s._set_parent_generic(self)
                        else:
                            s = cast("valueGenericT[T]", value[i])
                            c[existing_key] = self.children[existing_key]
                            c[existing_key].value = value
        self.children = c

    @overload
    def set(self, index: SupportsIndex, value: Any) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def set(self, index: slice, value: Iterable[Any]) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def set(
        self,
        index: SupportsIndex | slice,
        value: Any | Iterable[Any],
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

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field list
        """
        return len(self._children)

    def get_children(self) -> dict[str, fieldGenericT[T]]:
        """Get the children of this field as an ordered dictionary.

        Returns:
            the children of this field
        """
        return cast(
            "dict[str,fieldGenericT[T],]",
            self._children,
        )

    def set_children(
        self,
        children: dict[str, fieldGenericT[T]] | Sequence[fieldGenericT[T]] | None,
    ) -> None:
        """Set the children of this field using an ordered dictionary.

        Args:
            children: the new children for this field
        """
        self._children.clear()
        if isinstance(children, (dict, dict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

    def get_parent(self) -> fieldGenericT[Any] | None:
        """Get the field (if any) that is this field's parent.

        Returns:
            this field's parent (or None)
        """
        return cast("fieldGenericT[Any]", self._parent)

    def set_parent(self, parent: fieldGenericT[T] | None) -> None:
        """Set this field's parent.

        Args:
            parent: this field's new parent (or None)
        """
        self._parent = parent

    @property
    def children(self) -> dict[str, fieldGenericT[Any]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: dict[str, fieldGenericT[Any]] | Sequence[fieldGenericT[Any]],
    ) -> None:
        self.set_children(children=children)

    def __iter__(self) -> Iterator[BaseValueField[T]]:
        """Iterate over the fields in this list.

        Returns:
            field iterator
        """
        return cast("Iterator[BaseValueField[T]]", self._children.values().__iter__())


# class ParseValueList(BaseArrayField[T], Generic[T]):
#     """The base field value list."""

#     ...
