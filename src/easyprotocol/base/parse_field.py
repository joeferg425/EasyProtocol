# """The base parsing object for handling parsing in a convenient (to modify) package."""
# from __future__ import annotations

# from collections import OrderedDict
# from typing import Any, Generic, Literal, Sequence, TypeVar, Union, cast, overload

# from bitarray import bitarray
# from typing_extensions import override

# from easyprotocol.base.parse_dict_generic import ParseGenericDict
# from easyprotocol.base.parse_generic import (
#     DEFAULT_ENDIANNESS,
#     UNDEFINED,
#     ParseGeneric,
#     endianT,
# )
# from easyprotocol.base.parse_list_generic import ParseListGeneric
# from easyprotocol.base.parse_generic_value import ParseGenericValue
# from easyprotocol.base.utils import dataT

# T = TypeVar("T", bound=ParseGeneric[Any])
# # ParseGenericUnion = TypeVar(
# #     "ParseGenericUnion", ParseGenericValue[Any], ParseGenericDict[Any], ParseListGeneric[Any], covariant=True
# # )
# ParseGenericUnion = Union[ParseGenericValue[T], ParseGenericDict[T], ParseListGeneric[T]]


# class ParseFieldGeneric(
#     ParseGeneric[ParseGenericUnion[T]],
# ):
#     """The base parsing object for handling parsing in a convenient (to modify) package."""

#     def __init__(
#         self,
#         name: str,
#         bit_count: int = -1,
#         data: dataT = None,
#         string_format: str | None = None,
#         endian: endianT = DEFAULT_ENDIANNESS,
#         parent: ParseGeneric[Any] | None = None,
#         children: OrderedDict[str, ParseGeneric[Any]]
#         | dict[str, ParseGeneric[Any]]
#         | Sequence[ParseGeneric[Any]]
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
#         super().__init__(
#             name=name,
#             data=data,
#             bit_count=bit_count,
#             string_format=string_format,
#             endian=endian,
#             parent=parent,
#             children=children,
#         )

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

#     # def get_value(self) -> T:
#     #     raise NotImplementedError()

#     # def set_value(self, value: T) -> None:
#     #     raise NotImplementedError()

#     # def get_string_value(self) -> str:
#     #     """Get a formatted value for the field (for any custom formatting).

#     #     Returns:
#     #         the value of the field with custom formatting
#     #     """
#     #     if self.value is None:
#     #         return UNDEFINED
#     #     else:
#     #         return self._string_format.format(self.value)

#     def get_bytes_value(self) -> bytes:
#         return self.__bytes__()

#     def get_bits(self) -> bitarray:
#         return self._bits

#     def set_bits(self, bits: bitarray) -> None:
#         raise NotImplementedError()

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

#     def get_parent(self) -> ParseGenericUnion[Any] | None:
#         return cast(ParseGenericUnion[Any], self._parent)

#     def set_parent(self, parent: ParseGenericUnion[T] | None) -> None:
#         self._parent = parent

#     # @property
#     # def value(self) -> T:
#     #     """Get the parsed value of the field.

#     #     Returns:
#     #         the value of the field
#     #     """
#     #     return self.get_value()

#     # @value.setter
#     # def value(self, value: T) -> None:
#     #     self.set_value(value)

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
#     def parent(self) -> ParseGenericUnion[T] | None:
#         """Get the parent of the field.

#         Returns:
#             the parent of the field
#         """
#         return self.get_parent()

#     @parent.setter
#     def parent(self, parent: ParseGenericUnion[T] | None) -> None:
#         self.set_parent(parent)

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
#     def bytes(self) -> bytes:
#         """Get the byte value of this object.

#         Returns:
#             the byte value of this object
#         """
#         return self.__bytes__()

#     @property
#     def string(self) -> str:
#         """Get a formatted value for the field (for any custom formatting).

#         Returns:
#             the value of the field with custom formatting
#         """
#         return self.get_string_value()

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
#         return f"{self._name}: {self.string}"

#     def __repr__(self) -> str:
#         """Get a nicely formatted string describing this field.

#         Returns:
#             a nicely formatted string describing this field
#         """
#         return f"<{self.__class__.__name__}> {self.__str__()}"


# # class ParseField(ParseFieldGeneric[Any]):
# #     def __init__(
# #         self,
# #         name: str,
# #         value: Any | None = None,
# #         data: dataT = None,
# #         bit_count: int = -1,
# #         string_format: str | None = None,
# #         endian: endianT = DEFAULT_ENDIANNESS,
# #         parent: ParseFieldGeneric[Any] | None = None,
# #         children: OrderedDict[str, ParseGeneric[T]] | dict[str, ParseGeneric[T]] | Sequence[ParseGeneric[T]] | None = None,
# #     ) -> None:
# #         super().__init__(
# #             name=name,
# #             value=value,
# #             data=data,
# #             bit_count=bit_count,
# #             string_format=string_format,
# #             endian=endian,
# #             parent=parent,
# #             children=children,
# #         )
