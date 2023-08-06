# flake8:noqa
from __future__ import annotations

import struct

import pytest
from bitarray import bitarray

from easyprotocol.base import DictField
from easyprotocol.fields import UInt8Field
from easyprotocol.fields.checksum import ChecksumField, Crc16


class TestValue:
    def test_checksum_update_none(self) -> None:
        name = "test"
        initial_value = 2
        checksum = ChecksumField(name=name, bit_count=16, default=initial_value, crc_configuration=Crc16.CCITT.value)
        assert checksum.value == initial_value
        checksum.update_field(None)
        assert checksum.value != initial_value
        assert checksum.value == 0

    def test_checksum_update_with_value(self) -> None:
        name = "test"
        initial_value = 2
        new_value = 3
        byte_data = struct.pack("<H", new_value)
        checksum_value = 0x5355
        checksum_byte_data = struct.pack(">H", checksum_value)
        checksum_bit_data = bitarray()
        checksum_bit_data.frombytes(checksum_byte_data)
        checksum = ChecksumField(name=name, bit_count=16, default=initial_value, crc_configuration=Crc16.CCITT.value)
        assert checksum.value == initial_value
        checksum.update_field(byte_data)
        assert checksum.value != initial_value
        assert checksum.value == checksum_value
        assert checksum.value_as_bytes == checksum_byte_data
        assert checksum.bits == checksum_bit_data

    def test_checksum_update_from_parent_value(self) -> None:
        name = "checksum"
        initial_value = 0
        checksum_value = 0x5059
        checksum_byte_data = struct.pack(">H", checksum_value)
        checksum_bit_data = bitarray()
        checksum_bit_data.frombytes(checksum_byte_data)
        checksum = ChecksumField(name=name, bit_count=16, default=initial_value, crc_configuration=Crc16.CCITT.value)
        other = UInt8Field(name="other", default=3)
        DictField(name="parent", default=[other, checksum])
        assert checksum.value == initial_value
        checksum.update_field()
        assert checksum.value != initial_value
        assert checksum.value == checksum_value
        assert checksum.value_as_bytes == checksum_byte_data
        assert checksum.bits == checksum_bit_data
