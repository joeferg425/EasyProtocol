import struct
from collections import OrderedDict
from typing import Literal

import pytest
from bitarray import bitarray
from parse_data import ParseData, get_bitarray
from test_parse_uint import (  # TEST_VALUES_08_BIT,; TEST_VALUES_16_BIT,; TEST_VALUES_24_BIT,; TEST_VALUES_32_BIT,; TEST_VALUES_64_BIT,
    check_int,
)

from easyprotocol.base.parse_generic import endianT
from easyprotocol.base.utils import hex
from easyprotocol.fields.signed_int import (
    Int8Field,
    Int16Field,
    Int24Field,
    Int32Field,
    Int64Field,
    IntField,
)


def get_8bit_value(v: int) -> int:
    return struct.unpack(">b", struct.pack(">B", v))[0]


def get_8bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">b", struct.unpack(">b", struct.pack(">B", v))[0])
    else:
        return struct.pack("<b", struct.unpack("<b", struct.pack("<B", v))[0])


def get_16bit_value(v: int) -> int:
    return struct.unpack(">h", struct.pack(">H", v))[0]


def get_16bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">h", struct.unpack(">h", struct.pack(">H", v))[0])
    else:
        return struct.pack("<h", struct.unpack("<h", struct.pack("<H", v))[0])


def get_24bit_value(v: int) -> int:
    b = struct.pack(">I", v)
    # bl = b[:2]
    _b = b"\xff" if b[1] & 0x80 else b"\x00"
    b = _b + b[1:]
    return struct.unpack(">i", b)[0]
    # return struct.unpack("<i", struct.pack("<I", v))[0]


def get_24bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">i", struct.unpack(">i", struct.pack(">I", v))[0])[1:]
    else:
        return struct.pack("<i", struct.unpack("<i", struct.pack("<I", v))[0])[:-1]


def get_32bit_value(v: int) -> int:
    return struct.unpack("<i", struct.pack("<I", v))[0]


def get_32bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">i", struct.unpack(">i", struct.pack(">I", v))[0])
    else:
        return struct.pack("<i", struct.unpack("<i", struct.pack("<I", v))[0])


def get_64bit_value(v: int) -> int:
    return struct.unpack("<q", struct.pack("<Q", v))[0]


def get_64bit_bytes(v: int, endian: Literal["little", "big"]) -> bytes:
    if endian == "big":
        return struct.pack(">q", struct.unpack(">q", struct.pack(">Q", v))[0])
    else:
        return struct.pack("<q", struct.unpack("<q", struct.pack("<Q", v))[0])


# TEST_VALUES_08_BIT_INT_LE = [
#     pytest.param(
#         get_8bit_value(v),
#         get_8bit_bytes(v, "big"),
#         get_8bit_bytes(v, "little"),
#         get_bitarray(get_8bit_bytes(v, "big")),
#         get_bitarray(get_8bit_bytes(v, "little")),
#         "little",
#         id=f'{get_8bit_value(v)}, "{hex(get_8bit_bytes(v, "little"))}", "{get_bitarray(get_8bit_bytes(v, "little")).to01()}", "little"',
#     )
#     for v in TEST_VALUES_08_BIT
# ]
# TEST_VALUES_08_BIT_INT_BE = [
#     pytest.param(
#         get_8bit_value(v),
#         get_8bit_bytes(v, "big"),
#         get_8bit_bytes(v, "little"),
#         get_bitarray(get_8bit_bytes(v, "big")),
#         get_bitarray(get_8bit_bytes(v, "little")),
#         "big",
#         id=f'{get_8bit_value(v)}, "{hex(get_8bit_bytes(v, "big"))}", "{get_bitarray(get_8bit_bytes(v, "big")).to01()}", "big"',
#     )
#     for v in TEST_VALUES_08_BIT
# ]
# TEST_VALUES_16_BIT_INT_LE = [
#     pytest.param(
#         get_16bit_value(v),
#         get_16bit_bytes(v, "big"),
#         get_16bit_bytes(v, "little"),
#         get_bitarray(get_16bit_bytes(v, "big")),
#         get_bitarray(get_16bit_bytes(v, "little")),
#         "little",
#         id=f'{get_16bit_value(v)}, "{hex(get_16bit_bytes(v, "little"))}", "{get_bitarray(get_16bit_bytes(v, "little")).to01()}", "little"',
#     )
#     for v in TEST_VALUES_16_BIT
# ]
# TEST_VALUES_16_BIT_INT_BE = [
#     pytest.param(
#         get_16bit_value(v),
#         get_16bit_bytes(v, "big"),
#         get_16bit_bytes(v, "little"),
#         get_bitarray(get_16bit_bytes(v, "big")),
#         get_bitarray(get_16bit_bytes(v, "little")),
#         "big",
#         id=f'{get_16bit_value(v)}, "{hex(get_16bit_bytes(v, "big"))}", "{get_bitarray(get_16bit_bytes(v, "big")).to01()}", "big"',
#     )
#     for v in TEST_VALUES_16_BIT
# ]
# TEST_VALUES_24_BIT_INT_LE = [
#     pytest.param(
#         get_24bit_value(v),
#         get_24bit_bytes(v, "big"),
#         get_24bit_bytes(v, "little"),
#         get_bitarray(get_24bit_bytes(v, "big")),
#         get_bitarray(get_24bit_bytes(v, "little")),
#         "little",
#         id=f'{get_24bit_value(v)}, "{hex(get_24bit_bytes(v, "little"))}", "{get_bitarray(get_24bit_bytes(v, "little")).to01()}", "little"',
#     )
#     for v in TEST_VALUES_24_BIT
# ]
# TEST_VALUES_24_BIT_INT_BE = [
#     pytest.param(
#         get_24bit_value(v),
#         get_24bit_bytes(v, "big"),
#         get_24bit_bytes(v, "little"),
#         get_bitarray(get_24bit_bytes(v, "big")),
#         get_bitarray(get_24bit_bytes(v, "little")),
#         "big",
#         id=f'{get_24bit_value(v)}, "{hex(get_24bit_bytes(v, "big"))}", "{get_bitarray(get_24bit_bytes(v, "big")).to01()}", "big"',
#     )
#     for v in TEST_VALUES_24_BIT
# ]
# TEST_VALUES_32_BIT_INT_LE = [
#     pytest.param(
#         get_32bit_value(v),
#         get_32bit_bytes(v, "big"),
#         get_32bit_bytes(v, "little"),
#         get_bitarray(get_32bit_bytes(v, "big")),
#         get_bitarray(get_32bit_bytes(v, "little")),
#         "little",
#         id=f'{get_32bit_value(v)}, "{hex(get_32bit_bytes(v, "little"))}", "{get_bitarray(get_32bit_bytes(v, "little")).to01()}", "little"',
#     )
#     for v in TEST_VALUES_32_BIT
# ]
# TEST_VALUES_32_BIT_INT_BE = [
#     pytest.param(
#         get_32bit_value(v),
#         get_32bit_bytes(v, "big"),
#         get_32bit_bytes(v, "little"),
#         get_bitarray(get_32bit_bytes(v, "big")),
#         get_bitarray(get_32bit_bytes(v, "little")),
#         "big",
#         id=f'{get_32bit_value(v)}, "{hex(get_32bit_bytes(v, "big"))}", "{get_bitarray(get_32bit_bytes(v, "big")).to01()}", "big"',
#     )
#     for v in TEST_VALUES_32_BIT
# ]
# TEST_VALUES_64_BIT_INT_LE = [
#     pytest.param(
#         get_64bit_value(v),
#         get_64bit_bytes(v, "big"),
#         get_64bit_bytes(v, "little"),
#         get_bitarray(get_64bit_bytes(v, "big")),
#         get_bitarray(get_64bit_bytes(v, "little")),
#         "little",
#         id=f'{get_64bit_value(v)}, "{hex(get_64bit_bytes(v, "little"))}", "{get_bitarray(get_64bit_bytes(v, "little")).to01()}", "little"',
#     )
#     for v in TEST_VALUES_64_BIT
# ]
# TEST_VALUES_64_BIT_INT_BE = [
#     pytest.param(
#         get_64bit_value(v),
#         get_64bit_bytes(v, "big"),
#         get_64bit_bytes(v, "little"),
#         get_bitarray(get_64bit_bytes(v, "big")),
#         get_bitarray(get_64bit_bytes(v, "little")),
#         "big",
#         id=f'{get_64bit_value(v)}, "{hex(get_64bit_bytes(v, "big"))}", "{get_bitarray(get_64bit_bytes(v, "big")).to01()}", "big"',
#     )
#     for v in TEST_VALUES_64_BIT
# ]


class TestIntField:
    def test_intfield_create_empty_big_endian(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack(">b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_create_empty_little_endian(self) -> None:
        value = 0
        endian = "little"
        byte_data = struct.pack("<b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_name(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack("b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        tst.name = "new_name"
        obj.name = tst.name
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_value(self) -> None:
        value1 = 0
        byte_data1 = struct.pack(">b", value1)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 10
        endian = "big"
        byte_data2 = struct.pack(">b", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
            name="test",
            value=value1,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        obj.value = value2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_bits(self) -> None:
        value1 = 0
        byte_data1 = struct.pack("b", value1)
        bits_data1 = bitarray(endian="little")
        bits_data1.frombytes(byte_data1)
        value2 = 100
        endian = "big"
        byte_data2 = struct.pack("b", value2)
        bits_data2 = bitarray(endian="big")
        bits_data2.frombytes(byte_data2)
        tst = ParseData(
            name="test",
            value=value1,
            string_format="{}",
            byte_data=byte_data1,
            bits_data=bits_data1,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )

        obj.bits_lsb = bits_data2
        tst.value = value2
        tst.byte_data = byte_data2
        tst.bits_data = bits_data2
        check_int(
            obj=obj,
            tst=tst,
        )

    def test_intfield_set_parent(self) -> None:
        value = 0
        endian = "big"
        byte_data = struct.pack("b", value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format="{}",
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=endian,
            children=OrderedDict(),
        )
        obj = IntField(
            name=tst.name,
            bit_count=8,
            endian=tst.endian,
            default=tst.value,
        )
        check_int(
            obj=obj,
            tst=tst,
        )
        tst.parent = Int8Field(name="parent")
        obj.parent = tst.parent
        check_int(
            obj=obj,
            tst=tst,
        )


# class TestInt08:
#     def test_int8_create_empty_big_endian(self) -> None:
#         value = 0
#         endian = "big"
#         byte_data = struct.pack(">b", value)
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=0,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int8Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int8_create_empty_little_endian(self) -> None:
#         value = 0
#         endian = "little"
#         byte_data = struct.pack("<b", value)
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             bits_data=bits_data,
#             byte_data=byte_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int8Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_08_BIT_INT_BE,
#     )
#     def test_int8_create_parse_bytes_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             string_format="{}",
#             value=value,
#             bits_data=bits_data_be,
#             byte_data=byte_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int8Field(
#             name=tst.name,
#             data=byte_data_be,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_08_BIT_INT_LE,
#     )
#     def test_int8_create_parse_bytes_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             string_format="{}",
#             value=value,
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int8Field(
#             name=tst.name,
#             data=byte_data_le,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_08_BIT_INT_BE,
#     )
#     def test_int8_create_parse_bits_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             string_format="{}",
#             value=value,
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int8Field(
#             name=tst.name,
#             data=bits_data_be,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_08_BIT_INT_LE,
#     )
#     def test_int8_create_parse_bits_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             string_format="{}",
#             value=value,
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int8Field(
#             name=tst.name,
#             data=bits_data_le,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int8_create_parse_bits_short(self) -> None:
#         value1 = 0xFFFF
#         value2 = 0xFF
#         byte_data1 = struct.pack("H", value1)
#         byte_data2 = struct.pack("B", value2)
#         bits_data1 = bitarray(endian="little")
#         bits_data1.frombytes(byte_data1)
#         bits_data2 = bitarray(endian="little")
#         bits_data2.frombytes(byte_data2)
#         name = "test"
#         obj = Int8Field(
#             name=name,
#             data=byte_data1,
#         )

#         assert obj.bits == bits_data2
#         assert obj.bytes == byte_data2

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_08_BIT_INT_BE,
#     )
#     def test_int8_create_init_value_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             string_format="{}",
#             value=value,
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int8Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_08_BIT_INT_LE,
#     )
#     def test_int8_create_init_value_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             string_format="{}",
#             value=value,
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int8Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int8_set_value_invalid_type(self) -> None:
#         name = "test"
#         value = "invalid"
#         obj = Int8Field(
#             name=name,
#         )
#         with pytest.raises(ValueError):
#             obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

#     def test_int8_set_value_invalid_value(self) -> None:
#         name = "test"
#         value = 0x100
#         obj = Int8Field(
#             name=name,
#         )
#         with pytest.raises(OverflowError):
#             obj.value = value


# class TestInt16:
#     def test_int16_create_empty_big_endian(self) -> None:
#         value = 0
#         endian = "big"
#         byte_data = struct.pack(">h", value)
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int16Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int16_create_empty_little_endian(self) -> None:
#         value = 0
#         endian = "little"
#         byte_data = struct.pack("<h", value)
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int16Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_16_BIT_INT_BE,
#     )
#     def test_int16_create_parse_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int16Field(
#             name=tst.name,
#             data=byte_data_be,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_16_BIT_INT_LE,
#     )
#     def test_int16_create_parse_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int16Field(
#             name=tst.name,
#             data=byte_data_le,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_16_BIT_INT_BE,
#     )
#     def test_int16_create_init_value_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int16Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_16_BIT_INT_LE,
#     )
#     def test_int16_create_init_value_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int16Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int16_set_value_invalid_type(self) -> None:
#         name = "test"
#         value = "invalid"
#         obj = Int16Field(
#             name=name,
#         )
#         with pytest.raises(ValueError):
#             obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

#     def test_int16_set_value_invalid_value(self) -> None:
#         name = "test"
#         value = 0x10000
#         obj = Int16Field(
#             name=name,
#         )
#         with pytest.raises(OverflowError):
#             obj.value = value


# class TestInt24:
#     def test_int24_create_empty_big_endian(self) -> None:
#         value = 0
#         endian = "big"
#         byte_data = struct.pack(">i", value)[1:]
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int24Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int24_create_empty_little_endian(self) -> None:
#         value = 0
#         endian = "little"
#         byte_data = struct.pack("<i", value)[:-1]
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int24Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_24_BIT_INT_BE,
#     )
#     def test_int24_create_parse_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int24Field(
#             name=tst.name,
#             data=byte_data_be,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_24_BIT_INT_LE,
#     )
#     def test_int24_create_parse_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int24Field(
#             name=tst.name,
#             data=byte_data_le,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_24_BIT_INT_BE,
#     )
#     def test_int24_create_init_value_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int24Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_24_BIT_INT_LE,
#     )
#     def test_int24_create_init_value_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int24Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int24_set_value_invalid_type(self) -> None:
#         name = "test"
#         value = "invalid"
#         obj = Int24Field(
#             name=name,
#         )
#         with pytest.raises(ValueError):
#             obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

#     def test_int24_set_value_invalid_value(self) -> None:
#         name = "test"
#         value = 0x1000000
#         obj = Int24Field(
#             name=name,
#         )
#         with pytest.raises(OverflowError):
#             obj.value = value


# class TestInt32:
#     def test_int32_create_empty_big_endian(self) -> None:
#         value = 0
#         endian = "big"
#         byte_data = struct.pack(">i", value)
#         bits_data = bitarray(endian="big")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int32Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int32_create_empty_little_endian(self) -> None:
#         value = 0
#         endian = "little"
#         byte_data = struct.pack("<i", value)
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int32Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_32_BIT_INT_BE,
#     )
#     def test_int32_create_parse_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int32Field(
#             name=tst.name,
#             data=byte_data_be,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_32_BIT_INT_LE,
#     )
#     def test_int32_create_parse_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int32Field(
#             name=tst.name,
#             data=byte_data_le,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_32_BIT_INT_BE,
#     )
#     def test_int32_create_init_value_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int32Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_32_BIT_INT_LE,
#     )
#     def test_int32_create_init_value_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int32Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int32_set_value_invalid_type(self) -> None:
#         name = "test"
#         value = "invalid"
#         obj = Int32Field(
#             name=name,
#         )
#         with pytest.raises(ValueError):
#             obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

#     def test_int32_set_value_invalid_value(self) -> None:
#         name = "test"
#         value = 900000000001
#         obj = Int32Field(
#             name=name,
#         )
#         with pytest.raises(OverflowError):
#             obj.value = value


# class TestInt64:
#     def test_int64_create_empty_big_endian(self) -> None:
#         value = 0
#         endian = "big"
#         byte_data = struct.pack(">q", value)
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int64Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int64_create_empty_little_endian(self) -> None:
#         value = 0
#         endian = "little"
#         byte_data = struct.pack("<q", value)
#         bits_data = bitarray(endian="little")
#         bits_data.frombytes(byte_data)
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data,
#             bits_data=bits_data,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int64Field(
#             name=tst.name,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_64_BIT_INT_BE,
#     )
#     def test_int64_create_parse_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int64Field(
#             name=tst.name,
#             data=byte_data_be,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_64_BIT_INT_LE,
#     )
#     def test_int64_create_parse_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int64Field(
#             name=tst.name,
#             data=byte_data_le,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_64_BIT_INT_BE,
#     )
#     def test_int64_create_init_value_big_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_be,
#             bits_data=bits_data_be,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int64Field(
#             name=tst.name,
#             default=value,
#             endian=endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     @pytest.mark.parametrize(
#         [
#             "value",
#             "byte_data_be",
#             "byte_data_le",
#             "bits_data_be",
#             "bits_data_le",
#             "endian",
#         ],
#         TEST_VALUES_64_BIT_INT_LE,
#     )
#     def test_int64_create_init_value_little_endian(
#         self,
#         value: int,
#         byte_data_be: bytes,
#         byte_data_le: bytes,
#         bits_data_be: bitarray,
#         bits_data_le: bitarray,
#         endian: endianT,
#     ) -> None:
#         tst = ParseData(
#             name="test",
#             value=value,
#             string_format="{}",
#             byte_data=byte_data_le,
#             bits_data=bits_data_le,
#             parent=None,
#             children=OrderedDict(),
#             endian=endian,
#         )
#         obj = Int64Field(
#             name=tst.name,
#             default=tst.value,
#             endian=tst.endian,
#         )
#         check_int(
#             obj=obj,
#             tst=tst,
#         )

#     def test_int64_set_value_invalid_type(self) -> None:
#         name = "test"
#         value = "invalid"
#         obj = Int64Field(name=name)
#         with pytest.raises(ValueError):
#             obj.value = value  # pyright:ignore[reportGeneralTypeIssues]

#     def test_int64_set_value_invalid_value(self) -> None:
#         name = "test"
#         value = 0x10000000000000000
#         obj = Int64Field(name=name)
#         with pytest.raises(OverflowError):
#             obj.value = value
