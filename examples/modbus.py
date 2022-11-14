from __future__ import annotations
from typing import Literal
from easyprotocol.fields import UInt8Field, UIntField, UInt16Field, CRCField, UInt8EnumField
from easyprotocol.base import ParseList
from enum import IntEnum
import crc
from bitarray import bitarray
from bitarray.util import int2ba

read_coil_bytes = bytearray(b"\x11\x01\x00\x13\x00\x25\x0E\x84")


class FunctionEnum(IntEnum):
    Unknown = 0
    ReadSingleCoil = 1
    ReadMultipleDiscreteInputs = 2
    ReadMultipleHoldingRegisters = 3
    ReadMultipleInputRegisters = 4
    WriteSingleCoil = 5
    WriteMultipleHoldingRegister = 6
    WriteMultipleCoils = 15
    WriteMultipleHoldingRegisters = 16


function_code = UInt8EnumField(
    name="function code",
    enum_type=FunctionEnum,
)


class ModbusCRC(CRCField):
    def __init__(
        self,
        data: bytes | bitarray | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name="modbus crc",
            bit_count=16,
            crc_configuration=crc.Configuration(
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
        byte_data = bytes(self.parent)
        crc_int = self.crc_calculator.calculate_checksum(byte_data[:-2])
        crc_bytes = int.to_bytes(crc_int, length=2, byteorder="big")
        crc_int = int.from_bytes(crc_bytes, byteorder=self._endian, signed=False)
        crc_bits = int2ba(crc_int, length=self.bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)


crc_field = ModbusCRC()

modbusReadCoilRequest = ParseList(
    name=FunctionEnum.ReadSingleCoil.name,
    children=[
        UInt8Field(name="device id"),
        function_code,
        UInt16Field(name="data address", endian="little"),
        UInt16Field(name="data count", endian="little"),
        crc_field,
    ],
)
modbusReadCoilRequest.parse(read_coil_bytes)
print(modbusReadCoilRequest)
print(crc_field.calculate())
print(modbusReadCoilRequest)
