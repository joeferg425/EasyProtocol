"""This class is the basic parsing class for dictionary types."""
from __future__ import annotations

from typing import Any, Generic, Iterator, Mapping, Sequence, TypeVar

from bitarray import bitarray

from easyprotocol.base.base import BaseField, defaultT
from easyprotocol.base.utils import (
    DEFAULT_ENDIANNESS,
    dataT,
    endianT,
    input_to_bitarray,
)

T = TypeVar("T")


class DictFieldGeneric(
    BaseField,
    Mapping[str, BaseField],
    Generic[T],
):
    """This class is the basic parsing class for dictionary types."""

    def __init__(
        self,
        name: str,
        default: defaultT | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create the basic parsing class for dictionary types.

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
        bit_data = input_to_bitarray(data=data)
        for field in self._children.values():
            bit_data = field.parse(data=bit_data)
        return bit_data

    def popitem(self) -> tuple[str, BaseField]:
        """Remove item from list.

        Returns:
            the popped item
        """
        (name, item) = self._children.popitem()
        item.parent = None
        return (name, item)

    def pop(
        self,
        name: str,
        default: Any | BaseField | None = None,
    ) -> Any | BaseField | None:
        """Pop item from dictionary by name.

        Args:
            name: name of item to pop
            default: object to return if the name is not in the dictionary

        Returns:
            the item (or default item)
        """
        p = self._children.pop(name, default)
        if p is not None:
            p.set_parent(None)
        return p

    def get_value(
        self,
    ) -> dict[str, Any] | dict[str, BaseField]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return dict(self._children)

    def set_value(
        self,
        value: defaultT,
    ) -> None:
        """Set the value of the field.

        Args:
            value: the value of the field

        Raises:
            TypeError: if assigned value is of the wrong type
        """
        if isinstance(value, dict):
            for key, item in value.items():
                if not isinstance(item, BaseField):
                    raise TypeError(f"Cannot assign item of type {type(item)} to value of {self.__class__.__name__}")
                else:
                    self.__setitem__(key, item)
                    item.set_parent(self)
        else:
            for item in value:
                if not isinstance(item, BaseField):
                    raise TypeError(f"Cannot assign item of type {type(item)} to value of {self.__class__.__name__}")
                else:
                    key = item.name
                    self.__setitem__(key, item)
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

    def get_children(self) -> dict[str, BaseField]:
        """Get the children of this field as an ordered dictionary.

        Returns:
            the children of this field
        """
        return self._children

    def set_children(
        self,
        children: Sequence[Any] | dict[str, Any] | Sequence[BaseField] | dict[str, BaseField] | None,
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
                value.set_parent(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value.set_parent(self)

    def get_value_as_string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        s = f'{", ".join([str(value) for value in self._children.values()])}'
        return self.string_format.format(s)

    @property
    def value(self) -> dict[str, BaseField]:
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
        self.set_value(value)

    @property
    def children(self) -> dict[str, BaseField]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: dict[str, Any] | Sequence[Any] | dict[str, BaseField] | Sequence[BaseField] | None,
    ) -> None:
        self.set_children(children=children)

    def __setitem__(
        self,
        name: Any,
        value: BaseField,
    ) -> None:
        """Set an item in this dictionary to a new value.

        Args:
            name: a field name
            value: a new field value
        """
        value.set_parent(self)
        self._children.__setitem__(str(name), value)

    def __getitem__(
        self,
        name: Any,
    ) -> BaseField:
        """Get an item in this dictionary by name.

        Args:
            name: a field name

        Returns:
            the named field
        """
        return self._children.__getitem__(str(name))

    def __delitem__(
        self,
        name: str,
    ) -> None:
        """Delete an item in this dictionary by name.

        Args:
            name: a field name
        """
        self.children[name].parent = None
        self._children.__delitem__(name)

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field dictionary
        """
        return len(self._children)

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
        return f"{self._name}: {self.value_as_string}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    def __iter__(self) -> Iterator[str]:
        """Iterate over the fields in this list.

        Returns:
            field iterator
        """
        return self.children.__iter__()

    @property
    def value_list(self) -> list[T]:
        """Get values as a list of value types.

        Returns:
            values as a list of value types
        """
        return [v.value for v in self.values()]

    @property
    def value_dict(self) -> dict[str, T]:
        """Get values as a list of value types.

        Returns:
            values as a list of value types
        """
        return {v.name: v.value for v in self.values()}


class DictField(
    DictFieldGeneric[Any],
    BaseField,
):
    """Less Generic dictionary field."""

    def __init__(
        self,
        name: str,
        default: defaultT | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Less Generic dictionary field.

        Args:
            name: name of field
            default: default fields
            data: data to parse
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            default=default,
            data=data,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
        )
