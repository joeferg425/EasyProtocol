from __future__ import annotations
import math
from typing import Literal
from easyprotocol.fields.unsigned_int import UIntField
from crc import Configuration, CrcCalculator
from bitarray import bitarray
from bitarray.util import int2ba


class CRCField(UIntField):
    def __init__(
        self,
        name: str,
        bit_count: int,
        crc_configuration: Configuration,
        data: bytes | bitarray | None = None,
        value: int | None = None,
        format: str | None = "{:X}",
        endian: Literal["little", "big"] = "big",
    ) -> None:
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            value=value,
            format=format,
            endian=endian,
        )
        self.crc_calculator = CrcCalculator(
            configuration=crc_configuration,
        )

    def calculate(self, data: bytes | bitarray | None = None) -> tuple[int, bytes, bitarray]:
        if data is None:
            byte_data = bytes(self.parent)
        else:
            byte_data = data
        crc_int = self.crc_calculator.calculate_checksum(byte_data)
        byte_length = math.ceil(self.bit_count / 8)
        crc_bytes = int.to_bytes(crc_int, length=byte_length, byteorder="big")
        crc_int = int.from_bytes(crc_bytes, byteorder=self._endian, signed=False)
        crc_bits = int2ba(crc_int, length=self.bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)


class ModbusCRC(CRCField):
    def __init__(
        self,
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name="modbus crc",
            bit_count=16,
            crc_configuration=Configuration(
                width=16,
                polynomial=0x8005,
                init_value=0xFFFF,
                final_xor_value=0x0000,
                reverse_input=True,
                reverse_output=True,
            ),
            data=data,
            value=value,
            format="{:04X}",
            endian="little",
        )

    def calculate(self, data: bytes | bitarray | None = None) -> tuple[int, bytes, bitarray]:
        if data is None:
            byte_data = bytes(self.parent)
        else:
            byte_data = data
        crc_int = self.crc_calculator.calculate_checksum(byte_data[:-2])
        crc_bytes = int.to_bytes(crc_int, length=2, byteorder="big")
        crc_int = int.from_bytes(crc_bytes, byteorder=self._endian, signed=False)
        crc_bits = int2ba(crc_int, length=self.bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)
