from __future__ import annotations
from typing import Any, Literal
from easyprotocol.fields import UInt8Field, BoolField, UIntField, UInt16Field, CRCField, UInt8EnumField, ArrayField
from easyprotocol.base import ParseList, ParseObject, T, InputT, input_to_bytes
from enum import IntEnum
import crc
from bitarray import bitarray
from bitarray.util import int2ba
from collections import OrderedDict


class DeviceId(UInt8Field):
    def __init__(
        self,
        data: InputT | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name="device id",
            data=data,
            value=value,
            format="{:02X}",
            endian="big",
        )


class FunctionEnum(IntEnum):
    Unknown = 0
    ReadCoils = 1
    ReadDiscreteInputs = 2
    ReadMultipleHoldingRegisters = 3
    ReadMultipleInputRegisters = 4
    WriteSingleCoil = 5
    WriteMultipleHoldingRegister = 6
    WriteMultipleCoils = 15
    WriteMultipleHoldingRegisters = 16


class Function(UInt8EnumField):
    def __init__(
        self,
        data: InputT | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name="function code",
            enum_type=FunctionEnum,
            data=data,
            value=value,
            endian="little",
        )


class ModbusCRC(CRCField):
    def __init__(
        self,
        data: InputT | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name="crc",
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

    def calculate(self, data: InputT | None = None) -> tuple[int, bytes, bitarray]:
        byte_data = bytes(self.parent)
        crc_int = self.crc_calculator.calculate_checksum(byte_data[:-2])
        crc_bytes = int.to_bytes(crc_int, length=2, byteorder=self.endian)
        crc_int = int.from_bytes(crc_bytes, byteorder="big", signed=False)
        crc_bits = int2ba(crc_int, length=self.bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)


class CoilArray(ArrayField):
    def __init__(
        self,
        count_field: UIntField,
        data: InputT | None = None,
        parent: ParseObject[Any] | None = None,
        children: list[ParseObject[T]] | OrderedDict[str, ParseObject[T]] | None = None,
    ) -> None:
        super().__init__(
            name="coil array",
            count_field=count_field,
            array_item_class=BoolField,
            data=data,
            parent=parent,
            children=children,
        )

    def parse(self, data: InputT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        count = self.count_field.value * 8
        for i in range(count):
            f = self.array_item_class(f"f{i}")
            bit_data = f.parse(data=bit_data)
            self.append(f)
        return bit_data


class Address(UInt16Field):
    def __init__(
        self,
        data: InputT | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name="address",
            data=data,
            value=value,
            format="{:04X}",
            endian="little",
        )


def ReadCoils(check_crc: bool = False) -> None:
    readCoilsRequest = ParseList(
        name=FunctionEnum.ReadCoils.name + "Request",
        children=[
            DeviceId(),
            Function(),
            Address(),
            UInt16Field(name="data count", endian="little"),
            ModbusCRC(),
        ],
    )
    readCoilsRequestBytes = bytearray(b"\x11\x01\x00\x13\x00\x25\x0E\x84")
    readCoilsRequest.parse(readCoilsRequestBytes)
    print(bytes(readCoilsRequestBytes))
    print(readCoilsRequest)
    print(bytes(readCoilsRequest))
    if check_crc is True:
        print(readCoilsRequest.children["crc"].calculate())
        print(readCoilsRequest)
        print(bytes(readCoilsRequest))

    readCoilsResponseBytes = bytearray(b"\x11\x01\x05\xCD\x6B\xB2\x0E\x1B\x45\xE6")
    count_field = UInt8Field(name="byte count")
    readCoilsResponse = ParseList(
        name=FunctionEnum.ReadCoils.name + "Response",
        children=[
            DeviceId(),
            Function(),
            count_field,
            CoilArray(count_field=count_field),
            ModbusCRC(),
        ],
    )
    print(readCoilsResponseBytes)
    readCoilsResponse.parse(readCoilsResponseBytes)
    print(readCoilsResponse)
    if check_crc is True:
        print(readCoilsResponse.children["crc"].calculate())
        print(readCoilsResponse)


def ReadDiscreteInputs(check_crc: bool = False) -> None:
    readDiscreteInputsRequestBytes = b"\x11\x02\x00\xC4\x00\x16\xBA\xA9"
    readDiscreteInputsRequest = ParseList(
        name=FunctionEnum.ReadDiscreteInputs.name + "Request",
        children=[
            DeviceId(),
            Function(),
            Address(),
            UInt16Field(name="coil count", endian="little"),
            ModbusCRC(),
        ],
    )
    readDiscreteInputsRequest.parse(readDiscreteInputsRequestBytes)
    print(readDiscreteInputsRequest)
    if check_crc is True:
        print(readDiscreteInputsRequest.children["crc"].calculate())
        print(readDiscreteInputsRequest)


if __name__ == "__main__":
    check_crc = True
    ReadCoils(check_crc=check_crc)
    # ReadDiscreteInputs(check_crc=check_crc)
