"""The base parsing object for handling parsing in a convenient (to modify) package."""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Generic, Literal, NewType, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.utils import dataT

DEFAULT_ENDIANNESS: Literal["big", "little"] = "little"
UNDEFINED = "?UNDEFINED?"
endianT = Literal["little", "big"]
T = TypeVar("T", bound=Any)


class ParseBaseGeneric(Generic[T]):
    """The base parsing object for handling parsing in a convenient (to modify) package."""

    def __init__(
        self,
        name: str,
        value: T | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseBaseGeneric[Any] | None = None,
        children: OrderedDict[str, "ParseBaseGeneric[Any]"]
        | dict[str, "ParseBaseGeneric[Any]"]
        | list["ParseBaseGeneric[Any]"]
        | None = None,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: bytes to be parsed
            value: value to assign to object
            fmt: python format string (e.g. "{:f}")
            parent: object to nest this one inside of
            endian: the byte endian-ness of this object
        """
        self._name: str = ""
        self._endian: endianT = endian
        self._bits: bitarray = bitarray(endian="little")
        self._bit_count: int = bit_count
        self._name = name
        self._initialized = False
        self._parent: ParseBaseGeneric[Any] | None = parent
        self._children: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict()
        if string_format is None:
            self._string_format = "{}"
        else:
            self._string_format = string_format
        if children is not None:
            self.set_children(children)
        if data is not None:
            self.parse(data=data)
        elif value is not None:
            self.set_value(value)

    def parse(self, data: dataT) -> bitarray:
        """Parse the passed bits or bytes into meaningful data.

        Args:
            data: bits or bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        raise NotImplementedError()

    def get_value(self) -> T:
        raise NotImplementedError()

    def set_value(self, value: T) -> None:
        raise NotImplementedError()

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        if self.value is None:
            return UNDEFINED
        else:
            return self._string_format.format(self.value)

    def get_bytes_value(self) -> bytes:
        return self.__bytes__()

    def get_bits(self) -> bitarray:
        return self._bits

    def set_bits(self, bits: bitarray) -> None:
        raise NotImplementedError()

    def get_children(self) -> OrderedDict[str, ParseBaseGeneric[T]]:
        return self._children

    def set_children(
        self,
        children: OrderedDict[str, ParseBaseGeneric[T]]
        | dict[str, ParseBaseGeneric[T]]
        | list[ParseBaseGeneric[T]]
        | None,
    ) -> None:
        self._children.clear()
        if isinstance(children, (dict, OrderedDict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value.parent = self
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value.parent = self

    @property
    def name(self) -> str:
        """Get the name of the field.

        Returns:
            the name of the field
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: T) -> None:
        self.set_value(value)

    @property
    def bits(self) -> bitarray:
        """Get the bit value of the field.

        Returns:
            the bit value of the field
        """
        return self.get_bits()

    @bits.setter
    def bits(self, bits: bitarray) -> None:
        self.set_bits(bits)

    @property
    def parent(self) -> ParseBaseGeneric[T] | None:
        """Get the parent of the field.

        Returns:
            the parent of the field
        """
        return self._parent

    @parent.setter
    def parent(self, parent: ParseBaseGeneric[T] | None) -> None:
        self._parent = parent

    @property
    def children(self) -> OrderedDict[str, ParseBaseGeneric[T]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, "ParseBaseGeneric[T]"]
        | dict[str, "ParseBaseGeneric[T]"]
        | list["ParseBaseGeneric[T]"]
        | None,
    ) -> None:
        self.set_children(children=children)

    @property
    def string_format(self) -> str:
        """Get the format string of the field.

        Returns:
            the format string of the field
        """
        return self._string_format

    @string_format.setter
    def string_format(self, fmt: str) -> None:
        self._string_format = fmt

    @property
    def endian(self) -> Literal["little", "big"]:
        """Get the byte endianness value of this object.

        Returns:
            the byte endianness value of this object
        """
        return self._endian

    @property
    def bytes_value(self) -> bytes:
        """Get the byte value of this object.

        Returns:
            the byte value of this object
        """
        return self.__bytes__()

    @property
    def string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.get_string_value()

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self._bits.tobytes()

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


class ParseBase(ParseBaseGeneric[Any]):
    def __init__(
        self,
        name: str,
        value: Any | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        parent: ParseBaseGeneric[Any] | None = None,
        children: OrderedDict[str, "ParseBaseGeneric[Any]"]
        | dict[str, "ParseBaseGeneric[Any]"]
        | list["ParseBaseGeneric[Any]"]
        | None = None,
    ) -> None:
        super().__init__(
            name,
            value,
            data,
            bit_count,
            string_format,
            endian,
            parent,
            children,
        )


# T = TypeVar("T", bound=Union[Any, "ParseBaseGenericGeneric[Any]"])


# class ParseBaseGenericGeneric(ParseBaseGeneric, Generic[T]):
#     """The base parsing object for handling parsing in a convenient (to modify) package."""

#     def __init__(
#         self,
#         name: str,
#         value: T | None = None,
#         data: dataT = None,
#         bit_count: int = -1,
#         string_format: str | None = None,
#         endian: endianT = DEFAULT_ENDIANNESS,
#         parent: ParseBaseGenericGeneric[Any] | None = None,
#         children: OrderedDict[str, ParseBaseGenericGeneric[Any]]
#         | dict[str, ParseBaseGenericGeneric[Any]]
#         | list[ParseBaseGenericGeneric[Any]]
#         | None = None,
#     ) -> None:
#         """Create the base parsing object for handling parsing in a convenient package.

#         Args:
#             name: name of parsed object
#             data: bytes to be parsed
#             value: value to assign to object
#             fmt: python format string (e.g. "{:f}")
#             parent: object to nest this one inside of
#             endian: the byte endian-ness of this object
#         """
#         self._name: str = ""
#         self._endian: endianT = endian
#         self._bits: bitarray = bitarray(endian="little")
#         self._bit_count: int = bit_count
#         self._name = name
#         self._initialized = False
#         self._parent: ParseBaseGenericGeneric[Any] | None = parent
#         self._children: OrderedDict[str, ParseBaseGenericGeneric[Any]] = OrderedDict()
#         if string_format is None:
#             self._string_format = "{}"
#         else:
#             self._string_format = string_format
#         if children is not None:
#             self.set_children(children)
#         if data is not None:
#             self.parse(data=data)
#         elif value is not None:
#             self.set_value(value)

#     def parse(self, data: dataT) -> bitarray:
#         """Parse the passed bits or bytes into meaningful data.

#         Args:
#             data: bits or bytes to be parsed

#         Raises:
#             NotImplementedError: if not implemented for this field
#         """
#         raise NotImplementedError()

#     def update_field(self, data: dataT = None) -> Any:
#         """Calculate a new value for this field based on this field and/or an argument.

#         Args:
#             data: the optional data needed to update this field

#         Returns:
#             whatever is needed
#         """
#         raise NotImplementedError()

#     def get_value(self) -> T:
#         raise NotImplementedError()

#     def set_value(self, value: T | None) -> None:
#         raise NotImplementedError()

#     def get_string_value(self) -> str:
#         """Get a formatted value for the field (for any custom formatting).

#         Returns:
#             the value of the field with custom formatting
#         """
#         if self.value is None:
#             return UNDEFINED
#         else:
#             return self._string_format.format(self.value)

#     def get_bytes_value(self) -> bytes:
#         return self.__bytes__()

#     def get_bits(self) -> bitarray:
#         return self._bits

#     def set_bits(self, bits: bitarray) -> None:
#         raise NotImplementedError()

#     def get_children(self) -> OrderedDict[str, ParseBaseGenericGeneric[Any]]:
#         return OrderedDict(self._children)

#     def set_children(
#         self,
#         children: OrderedDict[str, ParseBaseGenericGeneric[Any]]
#         | dict[str, ParseBaseGenericGeneric[Any]]
#         | list[ParseBaseGenericGeneric[Any]]
#         | None,
#     ) -> None:
#         self._children.clear()
#         if isinstance(children, (dict, OrderedDict)):
#             keys = list(children.keys())
#             for key in keys:
#                 value = children[key]
#                 self._children[key] = value
#                 value.parent = self
#         elif isinstance(children, list):
#             for value in children:
#                 self._children[value._name] = value
#                 value.parent = self

#     @property
#     def name(self) -> str:
#         """Get the name of the field.

#         Returns:
#             the name of the field
#         """
#         return self._name

#     @name.setter
#     def name(self, name: str) -> None:
#         self._name = name

#     @property
#     def value(self) -> T:
#         """Get the parsed value of the field.

#         Returns:
#             the value of the field
#         """
#         return self.get_value()

#     @value.setter
#     def value(self, value: T | None) -> None:
#         self.set_value(value)

#     @property
#     def bits(self) -> bitarray:
#         """Get the bit value of the field.

#         Returns:
#             the bit value of the field
#         """
#         return self.get_bits()

#     @bits.setter
#     def bits(self, bits: bitarray) -> None:
#         self.set_bits(bits)

#     @property
#     def string_format(self) -> str:
#         """Get the format string of the field.

#         Returns:
#             the format string of the field
#         """
#         return self._string_format

#     @string_format.setter
#     def string_format(self, fmt: str) -> None:
#         self._string_format = fmt

#     @property
#     def endian(self) -> Literal["little", "big"]:
#         """Get the byte endianness value of this object.

#         Returns:
#             the byte endianness value of this object
#         """
#         return self._endian

#     @property
#     def bytes_value(self) -> bytes:
#         """Get the byte value of this object.

#         Returns:
#             the byte value of this object
#         """
#         return self.__bytes__()

#     @property
#     def string_value(self) -> str:
#         """Get a formatted value for the field (for any custom formatting).

#         Returns:
#             the value of the field with custom formatting
#         """
#         return self.get_string_value()

#     @property
#     def children(self) -> OrderedDict[str, ParseBaseGenericGeneric[Any]]:
#         """Get the parse objects that are contained by this one.

#         Returns:
#             the parse objects that are contained by this one
#         """
#         return self.get_children()

#     @children.setter
#     def children(
#         self,
#         children: OrderedDict[str, ParseBaseGenericGeneric[Any]]
#         | dict[str, ParseBaseGenericGeneric[Any]]
#         | list[ParseBaseGenericGeneric[Any]]
#         | None,
#     ) -> None:
#         self.set_children(children=children)

#     @property
#     def parent(self) -> ParseBaseGenericGeneric[Any] | None:
#         """Get the parent of the field.

#         Returns:
#             the parent of the field
#         """
#         return self._parent

#     @parent.setter
#     def parent(self, parent: ParseBaseGenericGeneric[Any] | None) -> None:
#         self._parent = parent

#     def __bytes__(self) -> bytes:
#         """Get the bytes that make up this field.

#         Returns:
#             the bytes of this field
#         """
#         return self._bits.tobytes()

#     def __str__(self) -> str:
#         """Get a nicely formatted string describing this field.

#         Returns:
#             a nicely formatted string describing this field
#         """
#         return f"{self._name}: {self.string_value}"

#     def __repr__(self) -> str:
#         """Get a nicely formatted string describing this field.

#         Returns:
#             a nicely formatted string describing this field
#         """
#         return f"<{self.__class__.__name__}> {self.__str__()}"


# T = TypeVar("T", bound=Union["ParseBaseGenericGeneric[Any]", Any])
# PT = TypeVar("PT", bound=Union["ParseBaseGenericGeneric[Any]", Any])
# CT = TypeVar("CT", bound=Union["ParseBaseGenericGeneric[Any]", Any])


# # class ParseBaseGenericGeneric(SupportsBytes, Generic[T, PT, CT]):
# #     """The base parsing object for handling parsing in a convenient (to modify) package."""

# #     def __init__(
# #         self,
# #         name: str,
# #         value: T | None = None,
# #         data: I = None,
# #         bit_count: int = -1,
# #         string_format: str | None = None,
# #         endian: endianT = DEFAULT_ENDIANNESS,
# #         parent: ParseBaseGenericGeneric[PT] | None = None,
# #         children: OrderedDict[str, ParseBaseGenericGeneric[CT]]
# #         | dict[str, ParseBaseGenericGeneric[CT]]
# #         | list[ParseBaseGenericGeneric[CT]]
# #         | None = None,
# #     ) -> None:
# #         """Create the base parsing object for handling parsing in a convenient package.

# #         Args:
# #             name: name of parsed object
# #             data: bytes to be parsed
# #             value: value to assign to object
# #             fmt: python format string (e.g. "{:f}")
# #             parent: object to nest this one inside of
# #             endian: the byte endian-ness of this object
# #         """
# #         super().__init__(
# #             name=name,
# #             bit_count=bit_count,
# #             children=cast(
# #                 Union[
# #                     OrderedDict[str, ParseBaseGeneric],
# #                     dict[str, ParseBaseGeneric],
# #                     list[ParseBaseGeneric],
# #                     None,
# #                 ],
# #                 children,
# #             ),
# #             data=data,
# #             endian=endian,
# #             parent=parent,
# #             string_format=string_format,
# #             value=value,
# #         )
# #         # # self._name: str = ""
# #         # # self._endian: endianT = endian
# #         # # self._bits: bitarray = bitarray(endian="little")
# #         # # self._parent: ParseBaseGenericGeneric[PT] | None = None
# #         # # self._children: OrderedDict[str, ParseBaseGenericGeneric[CT]] = OrderedDict()
# #         # # self._bit_count: int = bit_count
# #         # # self._name = name
# #         # # self._initialized = False
# #         # if string_format is None:
# #         #     self._string_format = "{}"
# #         # else:
# #         #     self._string_format = string_format
# #         # self._parent = parent
# #         # if self._string_format is None:
# #         #     self._string_format = "{}"
# #         # if children is not None:
# #         #     self.set_children(children)
# #         # if data is not None:
# #         #     self.parse(data=data)
# #         # elif value is not None:
# #         #     self.set_value(value)

# #     def parse(self, data: I) -> bitarray:
# #         """Parse the passed bits or bytes into meaningful data.

# #         Args:
# #             data: bits or bytes to be parsed

# #         Raises:
# #             NotImplementedError: if not implemented for this field
# #         """
# #         raise NotImplementedError()

# #     def update_field(self, data: I = None) -> Any:
# #         """Calculate a new value for this field based on this field and/or an argument.

# #         Args:
# #             data: the optional data needed to update this field

# #         Returns:
# #             whatever is needed
# #         """
# #         raise NotImplementedError()

# #     def get_value(self) -> T:
# #         raise NotImplementedError()

# #     def set_value(self, value: T | None) -> None:
# #         raise NotImplementedError()

# #     def get_string_value(self) -> str:
# #         """Get a formatted value for the field (for any custom formatting).

# #         Returns:
# #             the value of the field with custom formatting
# #         """
# #         if self.value is None:
# #             return UNDEFINED
# #         else:
# #             return self._string_format.format(self.value)

# #     def get_bytes_value(self) -> bytes:
# #         return self.__bytes__()

# #     def get_children(self) -> OrderedDict[str, ParseBaseGenericGeneric[CT]]:  # type:ignore[override]
# #         return cast(OrderedDict[str, ParseBaseGenericGeneric[CT]], OrderedDict(self._children))

# #     def set_children(  # type:ignore[override]
# #         self,
# #         children: OrderedDict[str, ParseBaseGenericGeneric[CT]]
# #         | dict[str, ParseBaseGenericGeneric[CT]]
# #         | list[ParseBaseGenericGeneric[CT]]
# #         | None,
# #     ) -> None:
# #         self._children.clear()
# #         if isinstance(children, (dict, OrderedDict)):
# #             keys = list(children.keys())
# #             for key in keys:
# #                 value = children[key]
# #                 self._children[key] = value
# #                 value.parent = self
# #         elif isinstance(children, list):
# #             for value in children:
# #                 self._children[value._name] = value
# #                 value.parent = self

# #     def get_bits(self) -> bitarray:
# #         return self._bits

# #     def set_bits(self, bits: bitarray) -> None:
# #         raise NotImplementedError()

# #     @property
# #     def name(self) -> str:
# #         """Get the name of the field.

# #         Returns:
# #             the name of the field
# #         """
# #         return self._name

# #     @name.setter
# #     def name(self, name: str) -> None:
# #         self._name = name

# #     @property
# #     def value(self) -> T:
# #         """Get the parsed value of the field.

# #         Returns:
# #             the value of the field
# #         """
# #         return self.get_value()

# #     @value.setter
# #     def value(self, value: T | None) -> None:
# #         self.set_value(value)

# #     @property
# #     def bits(self) -> bitarray:
# #         """Get the bit value of the field.

# #         Returns:
# #             the bit value of the field
# #         """
# #         return self.get_bits()

# #     @bits.setter
# #     def bits(self, bits: bitarray) -> None:
# #         self.set_bits(bits)

# #     @property  # type:ignore[override]
# #     def parent(self) -> ParseBaseGenericGeneric[PT] | None:
# #         """Get the parent of the field.

# #         Returns:
# #             the parent of the field
# #         """
# #         return cast(ParseBaseGenericGeneric[PT], self._parent)

# #     @parent.setter
# #     def parent(self, parent: ParseBaseGenericGeneric[PT] | None) -> None:
# #         self._parent = parent

# #     @property
# #     def string_format(self) -> str:
# #         """Get the format string of the field.

# #         Returns:
# #             the format string of the field
# #         """
# #         return self._string_format

# #     @string_format.setter
# #     def string_format(self, fmt: str) -> None:
# #         self._string_format = fmt

# #     @property  # type:ignore[override]
# #     def children(self) -> OrderedDict[str, ParseBaseGenericGeneric[CT]]:
# #         """Get the parse objects that are contained by this one.

# #         Returns:
# #             the parse objects that are contained by this one
# #         """
# #         return self.get_children()

# #     @children.setter
# #     def children(
# #         self,
# #         children: OrderedDict[str, ParseBaseGenericGeneric[CT]]
# #         | dict[str, ParseBaseGenericGeneric[CT]]
# #         | list[ParseBaseGenericGeneric[CT]]
# #         | None,
# #     ) -> None:
# #         self.set_children(children=children)

# #     @property
# #     def endian(self) -> Literal["little", "big"]:
# #         """Get the byte endianness value of this object.

# #         Returns:
# #             the byte endianness value of this object
# #         """
# #         return self._endian

# #     @property
# #     def bytes_value(self) -> bytes:
# #         """Get the byte value of this object.

# #         Returns:
# #             the byte value of this object
# #         """
# #         return self.__bytes__()

# #     @property
# #     def string_value(self) -> str:
# #         """Get a formatted value for the field (for any custom formatting).

# #         Returns:
# #             the value of the field with custom formatting
# #         """
# #         return self.get_string_value()

# #     def __bytes__(self) -> bytes:
# #         """Get the bytes that make up this field.

# #         Returns:
# #             the bytes of this field
# #         """
# #         return self._bits.tobytes()

# #     def __str__(self) -> str:
# #         """Get a nicely formatted string describing this field.

# #         Returns:
# #             a nicely formatted string describing this field
# #         """
# #         return f"{self._name}: {self.string_value}"

# #     def __repr__(self) -> str:
# #         """Get a nicely formatted string describing this field.

# #         Returns:
# #             a nicely formatted string describing this field
# #         """
# #         return f"<{self.__class__.__name__}> {self.__str__()}"
