# flake8:noqa
from __future__ import annotations

import struct

from bitarray import bitarray
from parse_data import ParseData

from easyprotocol.base.base import DEFAULT_ENDIANNESS
from easyprotocol.base.utils import hex
from easyprotocol.fields.string import (
    DEFAULT_BYTE_FORMAT,
    DEFAULT_BYTES_FORMAT,
    DEFAULT_CHAR_FORMAT,
    DEFAULT_STRING_FORMAT,
    ByteField,
    BytesField,
    CharField,
    StringField,
)


def check_str_byte_value(
    obj: CharField | StringField | ByteField | BytesField,
    tst: ParseData,
) -> None:
    if isinstance(obj, (StringField, BytesField)):
        assert (
            obj.value == tst.value
        ), f"{obj}: obj.value is not the expected value ({obj.value:.3e} != expected value: {tst.value:.3e})"
    else:
        assert (
            obj.value == tst.value
        ), f"{obj}: obj.value is not the expected value ({obj.value:.3e} != expected value: {tst.value:.3e})"


def check_str_byte_properties(
    obj: CharField | StringField | ByteField | BytesField,
    tst: ParseData,
) -> None:
    assert obj is not None, "Object is None"
    assert obj.name == tst.name, f"{obj}: obj.name is not the expected value ({obj.name} != expected value: {tst.name})"
    assert (
        obj.bits == tst.bits_data
    ), f"{obj}: obj.bits is not the expected value ({obj.bits} != expected value: {tst.bits_data})"
    assert (
        obj.parent == tst.parent
    ), f"{obj}: obj.parent is not the expected value ({obj.parent} != expected value: {tst.parent})"
    assert (
        bytes(obj) == tst.byte_data
    ), f"{obj}: bytes(obj) is not the expected value ({bytes(obj)!r} != expected value: {tst.byte_data!r})"
    assert (
        obj.endian == tst.endian
    ), f"{obj}: obj.endian is not the expected value ({obj.endian} != expected value: {tst.endian})"


def check_str_strings(
    obj: CharField | StringField,
    tst: ParseData,
) -> None:
    assert f"{tst.value}" == obj.value_as_string, (
        f"{obj}: obj.value_as_string is not the expected value "
        + f"({tst.string_format.format(tst.value)} != expected value: {obj.value_as_string})"
    )
    assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.value_as_string in str(
        obj
    ), f"{obj}: obj.value_as_string is not in the object's string vale ({obj.value_as_string} not in {str(obj)})"
    assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.value_as_string in repr(
        obj
    ), f"{obj}: obj.value_as_string is not in the object's repr vale ({obj.value_as_string} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def check_str(
    obj: CharField | StringField,
    tst: ParseData,
) -> None:
    check_str_byte_value(
        obj=obj,
        tst=tst,
    )
    check_str_byte_properties(
        obj=obj,
        tst=tst,
    )
    check_str_strings(
        obj=obj,
        tst=tst,
    )


def check_byte_strings(
    obj: ByteField | BytesField,
    tst: ParseData,
) -> None:
    assert f'"{tst.value.decode("latin1") }"(bytes)' == obj.value_as_string, (
        f"{obj}: obj.value_as_string is not the expected value "
        + f"({tst.string_format.format(tst.value)} != expected value: {obj.value_as_string})"
    )
    assert len(obj.value_as_string) > 0, (
        f"{obj}: obj.value_as_string is not the expected value " + f"(? != expected value: {obj.value_as_string})"
    )
    assert tst.name in str(obj), f"{obj}: obj.name is not in the object's string vale ({obj.name} not in {str(obj)})"
    assert obj.value_as_string in str(
        obj
    ), f"{obj}: obj.value_as_string is not in the object's string vale ({obj.value_as_string} not in {str(obj)})"
    assert tst.name in repr(obj), f"{obj}: obj.name is not in the object's repr vale ({obj.name} not in {repr(obj)})"
    assert obj.value_as_string in repr(
        obj
    ), f"{obj}: obj.value_as_string is not in the object's repr vale ({obj.value_as_string} not in {repr(obj)})"
    assert obj.__class__.__name__ in repr(
        obj
    ), f"{obj}: obj.__class__.__name__ is not in the object's repr vale ({obj.__class__.__name__} not in {repr(obj)})"


def check_bytes(
    obj: ByteField | BytesField,
    tst: ParseData,
) -> None:
    check_str_byte_value(
        obj=obj,
        tst=tst,
    )
    check_str_byte_properties(
        obj=obj,
        tst=tst,
    )
    check_byte_strings(
        obj=obj,
        tst=tst,
    )


class TestChar:
    def test_char_create_empty(self) -> None:
        value = "\x00"
        byte_data = b"\x00"
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_CHAR_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = CharField(
            name=tst.name,
        )

        check_str(
            obj=obj,
            tst=tst,
        )

    def test_char_create_parse(self) -> None:
        value = "G"
        byte_data = struct.pack("B", ord(value[0]))
        bits_data = bitarray(endian="big")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_CHAR_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = CharField(
            name=tst.name,
            data=byte_data,
        )

        check_str(
            obj=obj,
            tst=tst,
        )

    def test_char_create_init_value(self) -> None:
        value = "!"
        byte_data = struct.pack("B", ord(value[0]))
        bits_data = bitarray(endian="big")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_CHAR_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = CharField(
            name=tst.name,
            default=value,
        )

        check_str(
            obj=obj,
            tst=tst,
        )


class TestString:
    def test_string_create_empty(self) -> None:
        value = ""
        byte_data = value.encode("latin1")
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        count = 0
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = StringField(
            name=tst.name,
            byte_count=count,
        )

        check_str(
            obj=obj,
            tst=tst,
        )

    def test_string_create_parse(self) -> None:
        value = "\x00bob\x03"
        byte_data = value.encode("latin1")
        bits_data = bitarray(endian="big")
        bits_data.frombytes(byte_data)
        count = 5
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_STRING_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = StringField(
            name=tst.name,
            byte_count=count,
            data=byte_data,
        )

        check_str(
            obj=obj,
            tst=tst,
        )


class TestByte:
    def test_byte_create_empty(self) -> None:
        value = b"\x00"
        byte_data = bytes(value)
        bits_data = bitarray(endian="big")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_BYTE_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ByteField(
            name=tst.name,
        )

        check_bytes(
            obj=obj,
            tst=tst,
        )

    def test_byte_create_parse(self) -> None:
        value = b"G"
        byte_data = bytes(value)
        bits_data = bitarray(endian="big")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_BYTE_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ByteField(
            name=tst.name,
            data=byte_data,
        )

        check_bytes(
            obj=obj,
            tst=tst,
        )

    def test_byte_create_init_value(self) -> None:
        value = b"!"
        byte_data = bytes(value)
        bits_data = bitarray(endian="big")
        bits_data.frombytes(byte_data)
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_BYTE_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = ByteField(
            name=tst.name,
            default=value,
        )

        check_bytes(
            obj=obj,
            tst=tst,
        )


class TestBytes:
    def test_bytes_create_empty(self) -> None:
        value = b""
        byte_data = bytes(value)
        bits_data = bitarray(endian="little")
        bits_data.frombytes(byte_data)
        count = 0
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_BYTES_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = BytesField(
            name=tst.name,
            byte_count=count,
        )

        check_bytes(
            obj=obj,
            tst=tst,
        )

    def test_bytes_create_parse(self) -> None:
        value = b"\x00bob\x03"
        byte_data = bytes(value)
        bits_data = bitarray(endian="big")
        bits_data.frombytes(byte_data)
        count = 5
        tst = ParseData(
            name="test",
            value=value,
            string_format=DEFAULT_BYTES_FORMAT,
            byte_data=byte_data,
            bits_data=bits_data,
            parent=None,
            endian=DEFAULT_ENDIANNESS,
            children=dict(),
        )
        obj = BytesField(
            name=tst.name,
            byte_count=count,
            data=byte_data,
        )

        check_bytes(
            obj=obj,
            tst=tst,
        )
