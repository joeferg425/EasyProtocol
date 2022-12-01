# from __future__ import annotations

# import struct
# from collections import OrderedDict
# from typing import Any

# import pytest
# from bitarray import bitarray
# from test_parse_object import (
#     TestData,
#     check_parseobject_properties,
#     check_parseobject_value,
# )

# from easyprotocol.base.parse_base import DEFAULT_ENDIANNESS, ParseBase
# from easyprotocol.base.parse_list import ParseList
# from easyprotocol.fields.array import ArrayField
# from easyprotocol.fields.unsigned_int import BoolField, UInt8Field


# def check_array_strings(
#     obj: ArrayField[Any],
#     tst: TestData,
# ) -> None:
#     # assert tst.format.format(tst.value) == obj.string_value, (
#     #     f"{obj}: obj.string_value is not the expected value "
#     #     + f"({tst.format.format(tst.value)} != expected value: {obj.string_value})"
#     # )
#     assert len(obj.string_value) > 0, (
#         f"{obj}: obj.string_value is not the expected value " + f"(? != expected value: {obj.string_value})"
#     )
#     assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
#     assert obj.string_value in str(
#         obj
#     ), f"{obj}: obj.string_value is not in the object's string vale ({obj.string_value} not in {str(obj)})"
#     assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
#     assert obj.string_value in repr(
#         obj
#     ), f"{obj}: obj.string_value is not in the object's repr vale ({obj.string_value} not in {repr(obj)})"
#     assert obj.__class__.__name__ in repr(
#         obj
#     ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


# def check_array(
#     obj: ArrayField[Any],
#     tst: TestData,
# ) -> None:
#     check_parseobject_value(
#         obj=obj,
#         tst=tst,
#     )
#     check_parseobject_properties(
#         obj=obj,
#         tst=tst,
#     )
#     check_array_strings(
#         obj=obj,
#         tst=tst,
#     )


# class TestArray:
#     def test_array_create_empty_int_count(self) -> None:
#         value: list[Any] = []
#         byte_data = b""
#         bits_data = bitarray(endian="little")
#         count = 0
#         tst = TestData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = ArrayField(
#             name=tst.name,
#             count=count,
#             array_item_class=ParseBase,
#         )

#         check_array(
#             obj=obj,
#             tst=tst,
#         )

#     def test_array_create_empty_field_count(self) -> None:
#         value: list[Any] = []
#         byte_data = b""
#         bits_data = bitarray(endian="little")
#         count = UInt8Field(name="count")
#         tst = TestData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = ArrayField(
#             name=tst.name,
#             count=count,
#             array_item_class=ParseBase,
#         )

#         check_array(
#             obj=obj,
#             tst=tst,
#         )

#     def test_array_create_one(self) -> None:
#         name = "parent"
#         f1_name = "count"
#         f1 = UInt8Field(name=f1_name)
#         f2_name = "array"
#         f2 = ArrayField(
#             name=f2_name,
#             count=f1,
#             array_item_class=UInt8Field,
#         )
#         data = b"\x01\x00"
#         obj = ParseList(
#             name=name,
#             children=[f1, f2],
#         )
#         obj.parse(data=data)

#         assert f1.value == 1
#         assert f2.value == [0]

#     def test_array_create_three(self) -> None:
#         name = "parent"
#         f1_name = "count"
#         f1 = UInt8Field(name=f1_name)
#         f2_name = "array"
#         f2 = ArrayField(name=f2_name, count=f1, array_item_class=UInt8Field)
#         data = b"\x03\x00\x01\x02"
#         obj = ParseList(name=name, children=[f1, f2])
#         obj.parse(data=data)

#         assert f1.value == 3
#         assert f2.value == [0, 1, 2]

#     def test_array_create_invalid(self) -> None:
#         name = "parent"
#         f1_name = "count"
#         f1 = ParseList(name=f1_name)
#         f2_name = "array"
#         f2 = ArrayField(
#             name=f2_name,
#             count=f1,
#             array_item_class=UInt8Field,
#         )
#         data = b"\x02\x01\x00\x03"
#         with pytest.raises(TypeError):
#             obj = ParseList(name=name, children=[f1, f2])
#             obj.parse(data=data)

#     def test_array_of_booleans(self) -> None:
#         name = "parent"
#         count = 8
#         f2_name = "array"
#         f2 = ArrayField(
#             name=f2_name,
#             count=count,
#             array_item_class=BoolField,
#         )
#         value = 0b10100010
#         byte_data = struct.pack("B", value)
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         obj = ParseList(name=name, children=[f2])
#         obj.parse(data=byte_data)

#         assert obj.bytes_value == byte_data
#         assert obj.bits == bits_data

#     def test_array_set_name(self) -> None:
#         value: list[Any] = []
#         byte_data = b""
#         bits_data = bitarray(endian="little")
#         count = 0
#         tst = TestData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = ArrayField(
#             name=tst.name,
#             count=count,
#             array_item_class=BoolField,
#         )
#         check_array(
#             obj=obj,
#             tst=tst,
#         )

#         tst.name = "new_name"
#         obj.name = tst.name
#         check_array(
#             obj=obj,
#             tst=tst,
#         )

#     def test_array_set_value(self) -> None:
#         value1: list[Any] = [0, 1]
#         value2: list[Any] = [2, 3]
#         byte_data1 = bytes(value1)
#         bits_data1 = bitarray(endian="little")
#         bits_data1.frombytes(byte_data1)
#         byte_data2 = bytes(value2)
#         bits_data2 = bitarray(endian="little")
#         bits_data2.frombytes(byte_data2)
#         count = 2
#         tst = TestData(
#             name="test",
#             value=value1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = ArrayField(
#             name=tst.name,
#             count=count,
#             array_item_class=UInt8Field,
#             value_list=value1,
#         )
#         check_array(
#             obj=obj,
#             tst=tst,
#         )

#         obj.value_list = value2
#         tst.value = value2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2
#         check_array(
#             obj=obj,
#             tst=tst,
#         )

#     def test_array_set_bits(self) -> None:
#         value1: list[Any] = [0, 1]
#         value2: list[Any] = [2, 3]
#         byte_data1 = bytes(value1)
#         bits_data1 = bitarray(endian="little")
#         bits_data1.frombytes(byte_data1)
#         byte_data2 = bytes(value2)
#         bits_data2 = bitarray(endian="little")
#         bits_data2.frombytes(byte_data2)
#         count = 2
#         tst = TestData(
#             name="test",
#             value=value1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = ArrayField(
#             name=tst.name,
#             count=count,
#             array_item_class=UInt8Field,
#             value_list=value1,
#         )
#         check_array(
#             obj=obj,
#             tst=tst,
#         )
#         with pytest.raises(NotImplementedError):
#             obj.bits = bits_data2

#     def test_array_set_parent(self) -> None:
#         value1: list[Any] = [0, 1]
#         value2: list[Any] = [2, 3]
#         byte_data1 = bytes(value1)
#         bits_data1 = bitarray(endian="little")
#         bits_data1.frombytes(byte_data1)
#         byte_data2 = bytes(value2)
#         bits_data2 = bitarray(endian="little")
#         bits_data2.frombytes(byte_data2)
#         count = 2
#         tst = TestData(
#             name="test",
#             value=value1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=OrderedDict(),
#         )
#         obj = ArrayField(
#             name=tst.name,
#             count=count,
#             array_item_class=UInt8Field,
#             value_list=value1,
#         )
#         check_array(
#             obj=obj,
#             tst=tst,
#         )

#         tst.parent = ParseBase(name="parent")
#         obj.parent = tst.parent
#         check_array(
#             obj=obj,
#             tst=tst,
#         )

#     # def test_array_set_children(self) -> None:
#     #     value1: list[Any] = [0, 1]
#     #     value2: list[Any] = [2, 3]
#     #     byte_data1 = bytes(value1)
#     #     bits_data1 = bitarray(endian="little")
#     #     bits_data1.frombytes(byte_data1)
#     #     byte_data2 = bytes(value2)
#     #     bits_data2 = bitarray(endian="little")
#     #     bits_data2.frombytes(byte_data2)
#     #     count = 2
#     #     tst = TestData(
#     #         name="test",
#     #         value=value1,
#     #         string_format="{}",
#     #         byte_data=byte_data1,
#     #         bits_data=bits_data1,
#     #         parent=None,
#     #         endian=DEFAULT_ENDIANNESS,
#     #         children=OrderedDict(),
#     #     )
#     #     obj = ArrayField(
#     #         name=tst.name,
#     #         count=count,
#     #         array_item_class=UInt8Field,
#     #         value=value1,
#     #     )
#     #     check_array(
#     #         obj=obj,
#     #         tst=tst,
#     #     )
#     #     child = ParseBase(name="child`")
#     #     with pytest.raises(NotImplementedError):
#     #         obj.children = OrderedDict({child.name: child})
