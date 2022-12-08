# import struct
# from collections import OrderedDict
# from enum import IntFlag
# from typing import Any

# import pytest
# from bitarray import bitarray
# from parse_data import ParseData
# from test_parse_uint import check_int_properties, check_int_value

# from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS
# from easyprotocol.fields.flags import FlagsField


# def check_flags_strings(
#     obj: FlagsField[IntFlag],
#     tst: ParseData,
# ) -> None:

#     assert len(obj.string) > 0, f"{obj}: obj.string is not the expected value " + f"(? != expected value: {obj.string})"
#     assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
#     assert obj.string in str(
#         obj
#     ), f"{obj}: obj.string is not in the object's string vale ({obj.string} not in {str(obj)})"
#     assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
#     assert obj.string in repr(
#         obj
#     ), f"{obj}: obj.string is not in the object's repr vale ({obj.string} not in {repr(obj)})"
#     assert obj.__class__.__name__ in repr(
#         obj
#     ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


# def check_flags(
#     obj: FlagsField[Any],
#     tst: ParseData,
# ) -> None:
#     check_int_value(
#         obj=obj,
#         tst=tst,
#     )
#     check_int_properties(
#         obj=obj,
#         tst=tst,
#     )
#     check_flags_strings(
#         obj=obj,
#         tst=tst,
#     )


# class ExampleFlags(IntFlag):
#     NONE = 0
#     ONE = 1
#     TWO = 2
#     FOUR = 4
#     EIGHT = 8


# class TestFlags:
#     def test_flags_create_empty(self) -> None:
#         bit_count = 2
#         value = ExampleFlags.NONE
#         byte_data = struct.pack("B", value.value)
#         bits_data = bitarray()
#         bits_data.frombytes(byte_data)
#         bits_data = bits_data[-bit_count:]
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = FlagsField(
#             name=tst.name,
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             default=ExampleFlags.NONE,
#         )
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#     def test_flags_create_parse_one(self) -> None:
#         value = ExampleFlags.ONE
#         bit_count = 2
#         byte_data = struct.pack("B", value.value)
#         bits_data = bitarray()
#         bits_data.frombytes(byte_data)
#         bits_data = bits_data[-bit_count:]
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = FlagsField(
#             name=tst.name,
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             data=tst.byte_data,
#             default=ExampleFlags.NONE,
#         )
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#     def test_flags_create_parse_multiple(self) -> None:
#         value = ExampleFlags.ONE | ExampleFlags.TWO | ExampleFlags.FOUR | ExampleFlags.EIGHT
#         bit_count = 4
#         byte_data = struct.pack("B", value.value)
#         bits_data = bitarray()
#         bits_data.frombytes(byte_data)
#         bits_data = bits_data[-bit_count:]
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = FlagsField(
#             name=tst.name,
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             data=tst.byte_data,
#             default=ExampleFlags.NONE,
#         )
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#     def test_flags_create_truncate(self) -> None:
#         value1 = ExampleFlags.ONE | ExampleFlags.TWO | ExampleFlags.FOUR | ExampleFlags.EIGHT
#         value2 = ExampleFlags.ONE | ExampleFlags.TWO
#         bit_count = 2
#         byte_data1 = struct.pack("B", value1.value)
#         bits_data1 = bitarray()
#         bits_data1.frombytes(byte_data1)
#         bits_data1 = bits_data1[-bit_count:]
#         byte_data2 = struct.pack("B", value2.value)
#         bits_data2 = bitarray()
#         bits_data2.frombytes(byte_data2)
#         bits_data2 = bits_data2[-bit_count:]
#         tst = ParseData(
#             name="test",
#             value=value2,
#             string_format="{}",
#             byte_data=byte_data2,
#             bits_data=bits_data2,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = FlagsField(
#             name=tst.name,
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             data=byte_data2,
#             default=ExampleFlags.NONE,
#         )
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#     def test_flags_create_invalid(self) -> None:
#         with pytest.raises(TypeError):
#             FlagsField(
#                 name="invalid",
#                 bit_count=4,
#                 flags_type=ExampleFlags,
#                 data="pickles",  # pyright:ignore[reportGeneralTypeIssues]
#             )

#     def test_flags_set_name(self) -> None:
#         value = ExampleFlags.ONE | ExampleFlags.TWO | ExampleFlags.FOUR | ExampleFlags.EIGHT
#         bit_count = 4
#         byte_data = struct.pack("B", value.value)
#         bits_data = bitarray()
#         bits_data.frombytes(byte_data)
#         bits_data = bits_data[-bit_count:]
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = FlagsField(
#             name=tst.name,
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             data=tst.byte_data,
#             default=ExampleFlags.NONE,
#         )
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#         tst.name = "new_name"
#         obj.name = tst.name
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#     def test_flags_set_value(self) -> None:
#         value1 = ExampleFlags.ONE
#         value2 = ExampleFlags.ONE | ExampleFlags.TWO | ExampleFlags.FOUR | ExampleFlags.EIGHT
#         bit_count = 4
#         byte_data1 = struct.pack("B", value1.value)
#         bits_data1 = bitarray()
#         bits_data1.frombytes(byte_data1)
#         bits_data1 = bits_data1[-bit_count:]
#         byte_data2 = struct.pack("B", value2.value)
#         bits_data2 = bitarray()
#         bits_data2.frombytes(byte_data2)
#         bits_data2 = bits_data2[-bit_count:]
#         tst = ParseData(
#             name="test",
#             value=value1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = FlagsField(
#             name=tst.name,
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             data=tst.byte_data,
#             default=ExampleFlags.NONE,
#         )
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#         obj.value = value2
#         tst.value = value2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#     def test_flags_set_bits(self) -> None:
#         value1 = ExampleFlags.ONE
#         value2 = ExampleFlags.ONE | ExampleFlags.TWO | ExampleFlags.FOUR | ExampleFlags.EIGHT
#         bit_count = 4
#         byte_data1 = struct.pack("B", value1.value)
#         bits_data1 = bitarray()
#         bits_data1.frombytes(byte_data1)
#         bits_data1 = bits_data1[-bit_count:]
#         byte_data2 = struct.pack("B", value2.value)
#         bits_data2 = bitarray()
#         bits_data2.frombytes(byte_data2)
#         bits_data2 = bits_data2[-bit_count:]
#         tst = ParseData(
#             name="test",
#             value=value1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = FlagsField(
#             name=tst.name,
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             data=tst.byte_data,
#             default=ExampleFlags.NONE,
#         )
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#         obj.bits_lsb = bits_data2
#         tst.value = value2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#     def test_flags_set_parent(self) -> None:
#         value = ExampleFlags.ONE | ExampleFlags.TWO | ExampleFlags.FOUR | ExampleFlags.EIGHT
#         bit_count = 4
#         byte_data = struct.pack("B", value.value)
#         bits_data = bitarray()
#         bits_data.frombytes(byte_data)
#         bits_data = bits_data[-bit_count:]
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = FlagsField(
#             name=tst.name,
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             data=tst.byte_data,
#             default=ExampleFlags.NONE,
#         )
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )

#         tst.parent = FlagsField(
#             name="parent",
#             bit_count=bit_count,
#             flags_type=ExampleFlags,
#             data=tst.byte_data,
#             default=ExampleFlags.NONE,
#         )

#         obj.parent = tst.parent
#         check_flags(
#             obj=obj,
#             tst=tst,
#         )
