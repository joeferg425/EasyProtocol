# flake8:noqa
from __future__ import annotations

import struct
from datetime import datetime

import pytest
from bitarray import bitarray

from easyprotocol.base.utils import hex, input_to_bitarray
from easyprotocol.fields import UInt24Field


class TestUtils:
    def test_hex_bytes(self) -> None:
        s = hex(b"\xAB\xCD\xEF")
        assert s == "AB CD EF"

    def test_hex_list(self) -> None:
        s = hex(bytearray([0xAB, 0xCD, 0xEF]))
        assert s == "AB CD EF"

    def test_hex_list_msb(self) -> None:
        s = hex(bytearray([0xAA, 0x88]), lsB=False)
        assert s == "88 AA"

    def test_input_to_bytes_from_bytes(self) -> None:
        initial = b"\xAB\xCD\xEF"
        bits = input_to_bitarray(initial)
        expected = bitarray(endian="little")
        expected.frombytes(initial)
        assert bits == expected

    def test_input_to_bytes_from_bits(self) -> None:
        initial = b"\xAB\xCD\xEF"
        expected = bitarray(endian="little")
        expected.frombytes(initial)
        bits = input_to_bitarray(expected)
        assert bits == expected

    def test_input_to_bytes_from_field(self) -> None:
        initial = 0xABCDEF
        initial_bytes = struct.pack(">I", initial)[1:]
        field = UInt24Field(name="test", default=initial)
        expected = bitarray(endian="little")
        expected.frombytes(initial_bytes)
        bits = input_to_bitarray(field)
        assert bits == expected

    def test_input_to_bytes_from_invalid(self) -> None:
        with pytest.raises(TypeError):
            input_to_bitarray(7.0)  # pyright:ignore[reportGeneralTypeIssues]

    def test_input_to_bytes_fixed_length(self) -> None:
        initial = b"\xAB\xCD\xEF"
        bits = input_to_bitarray(initial, bit_count=32)
        expected = bitarray(endian="little")
        expected.frombytes(initial + b"\x00")
        assert bits == expected
