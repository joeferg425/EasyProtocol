# from __future__ import annotations

# import struct
# from collections import OrderedDict
# from typing import Any

# import pytest
# from bitarray import bitarray
# from test_parse_object import TestData, check_parseobject

# from easyprotocol.base.parse_base import DEFAULT_ENDIANNESS, ParseBase, ParseBaseGeneric
# from easyprotocol.base.parse_dict import ParseDict
# from easyprotocol.fields import UInt8Field
# from easyprotocol.fields.unsigned_int import UIntField


# def check_parsedict_value(
#     obj: ParseDict,
#     tst: TestData,
# ) -> None:
#     assert len(obj.value_dict) == len(tst.value), (
#         f"{obj}: len(obj.value) is not the expected value "
#         + f"({len(obj.value_dict)} != expected value: {len(tst.value)})"
#     )
#     assert obj.value_dict.keys() == tst.value.keys(), (
#         f"{obj}: obj.value.keys() is not the expected value "
#         + f"({obj.value_dict.keys()} != expected value: {tst.value.keys()})"
#     )
#     for key in tst.value.keys():
#         assert obj.value_dict[key] == tst.value[key], (
#             f"{obj}: obj.value[key] is not the expected value "
#             + f"({obj.value_dict[key]} != expected value: {tst.value[key]})"
#         )

#     for key in obj.value_dict.keys():
#         value = obj[key]
#         assert value in obj.string
#         assert value in str(obj)
#         assert value in repr(obj)


# def check_parsedict_properties(
#     obj: ParseDict,
#     tst: TestData,
# ) -> None:
#     assert obj is not None, "Object is None"
#     assert obj.name == tst.name, f"{obj}: obj.name is not the expected value ({obj.name} != expected value: {tst.name})"
#     assert (
#         obj.string_format == tst.string_format
#     ), f"{obj}: obj.format is not the expected value ({obj.string_format} != expected value: {tst.string_format})"
#     assert (
#         obj.bits == tst.bits_data
#     ), f"{obj}: obj.bits is not the expected value ({obj.bits} != expected value: {tst.bits_data})"
#     assert (
#         obj.parent == tst.parent
#     ), f"{obj}: obj.parent is not the expected value ({obj.parent} != expected value: {tst.parent})"
#     assert (
#         bytes(obj) == tst.byte_data
#     ), f"{obj}: bytes(obj) is not the expected value ({bytes(obj)!r} != expected value: {tst.byte_data!r})"
#     assert (
#         obj.endian == tst.endian
#     ), f"{obj}: obj.endian is not the expected value ({obj.endian} != expected value: {tst.endian})"


# def check_parsedict_children(
#     obj: ParseDict,
#     tst: TestData,
# ) -> None:
#     assert len(obj.children) == len(tst.children), (
#         f"{obj}: len(obj.children) is not the expected value "
#         + f"({len(obj.children)} != expected value: {len(tst.children)})"
#     )
#     assert obj.children.keys() == tst.children.keys(), (
#         f"{obj}: obj.children.keys() is not the expected value "
#         + f"({obj.children.keys()} != expected value: {tst.children.keys()})"
#     )
#     for key in tst.children.keys():
#         assert obj.children[key] == tst.children[key], (
#             f"{obj}: obj.children[key] is not the expected value "
#             + f"({obj.children[key]} != expected value: {tst.children[key]})"
#         )
#         assert obj.children[key].parent == obj, (
#             f"{obj}: obj.children[key].parent is not the expected value "
#             + f"({obj.children[key].parent} != expected value: {obj})"
#         )

#     for v in tst.children.values():
#         assert v.string in obj.string
#         assert v.string in str(obj)
#         assert v.string in repr(obj)
#     assert tst.name in str(obj)
#     assert tst.name in repr(obj)


# def check_parsedict(
#     obj: ParseDict,
#     tst: TestData,
# ) -> None:
#     check_parsedict_properties(
#         obj=obj,
#         tst=tst,
#     )
#     check_parsedict_value(
#         obj=obj,
#         tst=tst,
#     )
#     check_parsedict_children(
#         obj=obj,
#         tst=tst,
#     )


# class TestParseDict:
#     def test_parsedict_create_empty(self) -> None:
#         values: OrderedDict[str, Any] = OrderedDict()
#         byte_data = b""
#         bits_data = bitarray(endian="little")
#         tst = TestData(
#             name="test",
#             value=values,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_create_children(self) -> None:
#         f1_name = "child"
#         f1_value = 0
#         f1_value = 0
#         f1_bytes = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
#         f1_bits = bitarray(endian="little")
#         f1_bits.frombytes(f1_bytes)
#         f1 = UInt8Field(name=f1_name)
#         bits_data = f1.bits
#         byte_data = bits_data.tobytes()
#         values = OrderedDict({f1.name: f1.value})
#         children: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1.name: f1})
#         tst = TestData(
#             name="test",
#             value=values,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=children,
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#             children=tst.children,
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_create_parse_single(self) -> None:
#         f1_name = "child"
#         f1_value = 0
#         f1_bytes = int.to_bytes(f1_value, length=1, byteorder="big", signed=False)
#         f1_bits = bitarray(endian="little")
#         f1_bits.frombytes(f1_bytes)
#         f1 = UInt8Field(name=f1_name)
#         children: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1.name: f1})
#         byte_data = f1_bytes
#         bits_data = f1_bits
#         tst = TestData(
#             name="test",
#             value=children,
#             byte_data=byte_data,
#             bits_data=bits_data,
#             string_format="{}",
#             parent=None,
#             children=children,
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#             children=tst.children,
#             data=tst.byte_data,
#         )
#         obj[f1.name] = f1
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_create_parse_multi_field(self) -> None:
#         f1_name = "f1"
#         f1_value = 170
#         f1_data = b"\xaa"
#         f1_bits = bitarray(endian="little")
#         f1_bits.frombytes(f1_data)
#         f1 = UInt8Field(name=f1_name)
#         f_children: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict()
#         f2_name = "f2"
#         f2_value = 187
#         f2_data = b"\xbb"
#         f2_bits = bitarray(endian="little")
#         f2_bits.frombytes(f2_data)
#         f2 = UInt8Field(name=f2_name)
#         f3_name = "f3"
#         f3_value = 204
#         f3_data = b"\xcc"
#         f3_bits = bitarray(endian="little")
#         f3_bits.frombytes(f3_data)
#         f3 = UInt8Field(name=f3_name)
#         byte_data = f1_data + f2_data + f3_data
#         bits_data = f1_bits + f2_bits + f3_bits
#         children: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
#         tst = TestData(
#             name="test",
#             value=children,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=children,
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#             data=byte_data,
#             children=children,
#         )
#         check_parseobject(
#             obj=f1,
#             tst=TestData(
#                 name=f1_name,
#                 value=f1_value,
#                 string_format=f1.string_format,
#                 bits_data=f1_bits,
#                 byte_data=f1_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parseobject(
#             obj=f2,
#             tst=TestData(
#                 name=f2_name,
#                 value=f2_value,
#                 string_format=f2.string_format,
#                 bits_data=f2_bits,
#                 byte_data=f2_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parseobject(
#             obj=f3,
#             tst=TestData(
#                 name=f3_name,
#                 value=f3_value,
#                 string_format=f3.string_format,
#                 bits_data=f3_bits,
#                 byte_data=f3_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_parse_single_field(self) -> None:
#         f1_data0 = b"\x00"
#         f1_bits0 = bitarray(endian="little")
#         f1_bits0.frombytes(f1_data0)
#         f1_name = "f1"
#         f1_value = 255
#         f1_data = int.to_bytes(f1_value, length=1, byteorder="big")
#         f1_bits = bitarray(endian="little")
#         f1_bits.frombytes(f1_data)
#         f1 = UInt8Field(name=f1_name)
#         byte_data1 = int.to_bytes(0, length=1, byteorder="big")
#         byte_data2 = f1_data
#         bits_data1 = bitarray(endian="little")
#         bits_data1.frombytes(byte_data1)
#         bits_data2 = f1_bits
#         left_over = bitarray(endian="little")
#         children1: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1})
#         children2: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1})
#         tst = TestData(
#             name="test",
#             value=children1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             children=children1,
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#         )
#         obj[f1.name] = f1

#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#         remainder = obj.parse(byte_data2)
#         assert remainder == left_over
#         tst.value = children2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_parse_multi_field(self) -> None:
#         u_data = b"\x00"
#         u_bits = bitarray(endian="little")
#         u_bits.frombytes(u_data)

#         init_value = 0
#         init_data = int.to_bytes(init_value, length=1, byteorder="big")
#         init_bits = bitarray(endian="little")
#         init_bits.frombytes(init_data)

#         f1_name = "f1"
#         f1_value = 170
#         f1_data = b"\xaa"
#         f1_bits = bitarray(endian="little")
#         f1_bits.frombytes(f1_data)
#         f1 = UInt8Field(name=f1_name)
#         f_children: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict()
#         f2_name = "f2"
#         f2_value = 187
#         f2_data = b"\xbb"
#         f2_bits = bitarray(endian="little")
#         f2_bits.frombytes(f2_data)
#         f2 = UInt8Field(name=f2_name)
#         f3_name = "f3"
#         f3_value = 204
#         f3_data = b"\xcc"
#         f3_bits = bitarray(endian="little")
#         f3_bits.frombytes(f3_data)
#         f3 = UInt8Field(name=f3_name)
#         left_over = bitarray(endian="little")
#         byte_data1 = init_data + init_data + init_data
#         byte_data2 = f1_data + f2_data + f3_data
#         bits_data1 = u_bits + u_bits + u_bits
#         bits_data2 = f1_bits + f2_bits + f3_bits
#         children1: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
#         children2: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
#         tst = TestData(
#             name="test",
#             value=children1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             children=children1,
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#         )
#         obj[f1.name] = f1
#         obj[f2.name] = f2
#         obj[f3.name] = f3

#         check_parseobject(
#             obj=f1,
#             tst=TestData(
#                 name=f1_name,
#                 value=init_value,
#                 string_format=f1.string_format,
#                 bits_data=init_bits,
#                 byte_data=init_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parseobject(
#             obj=f2,
#             tst=TestData(
#                 name=f2_name,
#                 value=init_value,
#                 string_format=f2.string_format,
#                 bits_data=init_bits,
#                 byte_data=init_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parseobject(
#             obj=f3,
#             tst=TestData(
#                 name=f3_name,
#                 value=init_value,
#                 string_format=f3.string_format,
#                 bits_data=init_bits,
#                 byte_data=init_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#         remainder = obj.parse(byte_data2)
#         assert remainder == left_over
#         tst.value = children2
#         tst.children = children2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2
#         check_parseobject(
#             obj=f1,
#             tst=TestData(
#                 name=f1_name,
#                 value=f1_value,
#                 string_format=f1.string_format,
#                 bits_data=f1_bits,
#                 byte_data=f1_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parseobject(
#             obj=f2,
#             tst=TestData(
#                 name=f2_name,
#                 value=f2_value,
#                 string_format=f2.string_format,
#                 bits_data=f2_bits,
#                 byte_data=f2_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parseobject(
#             obj=f3,
#             tst=TestData(
#                 name=f3_name,
#                 value=f3_value,
#                 string_format=f3.string_format,
#                 bits_data=f3_bits,
#                 byte_data=f3_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_parse_multi_bit_field_little_endian(self) -> None:
#         f1_bit_count = 2
#         f1_name = "f1"
#         f1_value = 0b11
#         f1_byte = struct.pack("B", f1_value)
#         f1_bits = bitarray(endian="little")
#         f1_bits.frombytes(f1_byte)
#         f1_bits = f1_bits[:f1_bit_count]
#         f1 = UIntField(
#             name=f1_name,
#             bit_count=f1_bit_count,
#             endian=DEFAULT_ENDIANNESS,
#         )

#         f2_bit_count = 5
#         f2_name = "f2"
#         f2_value = 0b00000
#         f2_data = struct.pack("B", f2_value)
#         f2_bits = bitarray(endian="little")
#         f2_bits.frombytes(f2_data)
#         f2_bits = f2_bits[:f2_bit_count]
#         f2 = UIntField(
#             name=f2_name,
#             bit_count=f2_bit_count,
#             endian=DEFAULT_ENDIANNESS,
#         )

#         f3_bit_count = 9
#         f3_name = "f3"
#         f3_value = 0b111111111
#         f3_data = struct.pack("<H", f3_value)
#         f3_bits = bitarray(endian="little")
#         f3_bits.frombytes(f3_data)
#         f3_bits = f3_bits[:f3_bit_count]
#         f3 = UIntField(
#             name=f3_name,
#             bit_count=f3_bit_count,
#             endian=DEFAULT_ENDIANNESS,
#         )

#         f_children: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict()

#         left_over = bitarray(endian="little")
#         byte_data1 = b"\x00\x00"
#         byte_data2 = b"\x83\xFF"
#         bits_data1 = bitarray(endian="little")
#         bits_data1.frombytes(byte_data1)
#         bits_data2 = bitarray(endian="little")
#         bits_data2.frombytes(byte_data2)
#         children1: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
#         children2: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1, f2_name: f2, f3_name: f3})
#         tst = TestData(
#             name="test",
#             value=children1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             children=children1,
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#             children=OrderedDict(
#                 {
#                     f1.name: f1,
#                     f2.name: f2,
#                     f3.name: f3,
#                 }
#             ),
#         )
#         remainder = obj.parse(byte_data2)
#         assert remainder == left_over
#         tst.value = children2
#         tst.children = children2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2
#         check_parseobject(
#             obj=f1,
#             tst=TestData(
#                 name=f1_name,
#                 value=f1_value,
#                 string_format=f1.string_format,
#                 bits_data=f1_bits,
#                 byte_data=f1_byte,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parseobject(
#             obj=f2,
#             tst=TestData(
#                 name=f2_name,
#                 value=f2_value,
#                 string_format=f2.string_format,
#                 bits_data=f2_bits,
#                 byte_data=f2_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parseobject(
#             obj=f3,
#             tst=TestData(
#                 name=f3_name,
#                 value=f3_value,
#                 string_format=f3.string_format,
#                 bits_data=f3_bits,
#                 byte_data=f3_data,
#                 parent=obj,
#                 children=f_children,
#                 endian=DEFAULT_ENDIANNESS,
#             ),
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_set_name(self) -> None:
#         name1 = "test"
#         name2 = "new_name"
#         byte_data = b""
#         bits_data = bitarray(endian="little")
#         values: OrderedDict[str, Any] = OrderedDict()
#         tst = TestData(
#             name=name1,
#             value=values,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#         tst.name = name2
#         obj.name = tst.name
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_set_value(self) -> None:
#         f1_name = "object1"
#         v2 = 0
#         v3 = 1
#         byte_data1 = b""
#         byte_data2 = int.to_bytes(v2, length=1, byteorder="big")
#         byte_data3 = int.to_bytes(v3, length=1, byteorder="big")
#         bits_data1 = bitarray(endian="little")
#         bits_data2 = bitarray(endian="little")
#         bits_data3 = bitarray(endian="little")
#         bits_data2.frombytes(byte_data2)
#         bits_data3.frombytes(byte_data3)
#         f1 = UInt8Field(name=f1_name, value=v2)
#         values1: OrderedDict[str, Any] = OrderedDict()
#         values3: OrderedDict[str, Any] = OrderedDict({f1_name: v3})
#         children1: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict()
#         children2: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1.name: f1})
#         children3: OrderedDict[str, ParseBaseGeneric[Any]] = children2.copy()
#         tst = TestData(
#             name="test",
#             value=values1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             children=children1,
#             endian=DEFAULT_ENDIANNESS,
#         )

#         obj = ParseDict(
#             name=tst.name,
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#         obj.value = children2
#         tst.children = children2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2
#         tst.value = children2
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#         obj.value = values3
#         tst.children = children3
#         tst.byte_data = byte_data3
#         tst.bits_data = bits_data3
#         tst.value = children3
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#         value = 1
#         obj = ParseDict(name=tst.name)
#         with pytest.raises(TypeError):
#             obj.value = value

#     def test_parsedict_set_parent(self) -> None:
#         f1_value = 0
#         f1_data = int.to_bytes(f1_value, length=1, byteorder="big")
#         f1_bits = bitarray(endian="little")
#         f1_bits.frombytes(b"\x00")
#         f1_name = "parent"
#         byte_data1 = b""
#         bits_data1 = bitarray(endian="little")
#         byte_data2 = f1_data
#         bits_data2 = f1_bits
#         f1 = UInt8Field(name=f1_name)
#         values1: OrderedDict[str, Any] = OrderedDict()
#         children1: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict()
#         children2: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1})
#         tst = TestData(
#             name="test",
#             value=values1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             children=children1,
#             endian=DEFAULT_ENDIANNESS,
#         )
#         obj = ParseDict(
#             name=tst.name,
#         )

#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#         obj.children = children2
#         tst.children = children2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2
#         tst.value = children2
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#     def test_parsedict_set_children(self) -> None:
#         f1_value = 0
#         f1_data = int.to_bytes(f1_value, length=1, byteorder="big")
#         f1_bits = bitarray(endian="little")
#         f1_bits.frombytes(b"\x00")
#         f1_name = "parent"
#         byte_data1 = b""
#         bits_data1 = bitarray(endian="little")
#         byte_data2 = f1_data
#         bits_data2 = f1_bits
#         f1 = UInt8Field(name=f1_name)
#         values1: OrderedDict[str, Any] = OrderedDict()
#         values2: OrderedDict[str, Any] = OrderedDict({f1.name: f1.value})
#         children1: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict()
#         children2: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1_name: f1})
#         tst = TestData(
#             name="test",
#             value=values1,
#             string_format="{}",
#             byte_data=byte_data1,
#             bits_data=bits_data1,
#             parent=None,
#             endian=DEFAULT_ENDIANNESS,
#             children=children1,
#         )
#         obj = ParseDict(
#             name=tst.name,
#         )
#         check_parsedict(
#             obj=obj,
#             tst=tst,
#         )

#         obj.children = children2
#         tst.children = children2
#         tst.value = values2
#         tst.byte_data = byte_data2
#         tst.bits_data = bits_data2

#     def test_parsedict_set_item(self) -> None:
#         name = "test"
#         obj = ParseDict(name=name)
#         with pytest.raises(TypeError):
#             obj["x"] = "popcorn"

#     def test_parsedict_pop(self) -> None:
#         name = "test"
#         f1_name = "f1"
#         f1 = UInt8Field(name=f1_name)
#         f2_name = "f2"
#         f2 = UInt8Field(name=f2_name)
#         children: OrderedDict[str, ParseBaseGeneric[Any]] = OrderedDict({f1.name: f1, f2.name: f2})
#         obj = ParseDict(name=name, children=children)

#         assert len(obj) == 2
#         assert f1.parent == obj
#         assert f2.parent == obj
#         obj.pop(f2_name)
#         assert len(obj) == 1
#         assert f2.parent is None
