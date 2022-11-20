from __future__ import annotations
import math
from typing import Any, cast
from easyprotocol.fields import UInt8Field, BoolField, UIntField, UInt16Field, ChecksumField, UInt8EnumField, ArrayField
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
            name="functionCode",
            enum_type=FunctionEnum,
            data=data,
            value=value,
            endian="little",
        )


class ModbusCRC(ChecksumField):
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
            format="{:04X}(hex)",
            endian="little",
        )

    def update(self, data: InputT | None = None) -> tuple[int, bytes, bitarray]:
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

    @property
    def bits(self) -> bitarray:
        """Get the bytes value of the field.

        Returns:
            the bytes value of the field
        """
        data = bitarray()
        values = list(self._children.values())
        for value in values:
            data = value.bits + data
        b_big_endian = data.tobytes()
        byte_count = math.ceil(len(data) / 8)
        temp_int = int.from_bytes(b_big_endian, byteorder="big", signed=False)
        b_little_endian = int.to_bytes(temp_int, length=byte_count, byteorder="little", signed=False)
        data = bitarray()
        data.frombytes(b_little_endian)
        return data

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        chunks = {}
        keys = list(self._children.keys())
        for i in range(0, len(keys), 8):
            chunk_key = keys[i]
            vals = "".join(["1" if self._children[keys[j]].value else "0" for j in range(i, i + 8)])
            chunks[chunk_key] = vals
        return f"[{', '.join([key+':'+value for key, value in chunks.items()])}]"


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
            endian="little",
        )


class ModbusHeader(ParseList):
    def __init__(
        self,
        name: str = "modbusHeader",
        data: InputT | None = None,
        children: list[ParseObject[Any]]
        | OrderedDict[str, ParseObject[Any]] = [
            DeviceId(),
            Function(),
            Address(),
            ModbusCRC(),
        ],
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            parent=None,
            children=children,
        )

    @property
    def deviceId(self) -> DeviceId:
        return cast(DeviceId, self._children["deviceId"])

    @deviceId.setter
    def deviceId(self, value: DeviceId | int) -> None:
        if isinstance(value, DeviceId):
            self._children["deviceId"] = value
        else:
            self._children["deviceId"].value = value

    @property
    def functionCode(self) -> Function:
        return cast(Function, self._children["functionCode"])

    @functionCode.setter
    def functionCode(self, value: Function | int | FunctionEnum) -> None:
        if isinstance(value, Function):
            self._children["functionCode"] = value
        else:
            self._children["functionCode"].value = value

    @property
    def address(self) -> Address:
        return cast(Address, self._children["address"])

    @address.setter
    def address(self, value: Address | int) -> None:
        if isinstance(value, Address):
            self._children["address"] = value
        else:
            self._children["address"].value = value

    @property
    def crc(self) -> ModbusCRC:
        return cast(ModbusCRC, self._children["crc"])

    @crc.setter
    def crc(self, value: ModbusCRC | int) -> None:
        if isinstance(value, ModbusCRC):
            self._children["crc"] = value
        else:
            self._children["crc"].value = value


class ModbusReadCoilsRequest(ModbusHeader):
    def __init__(
        self,
        data: InputT | None = None,
        children: list[ParseObject[Any]]
        | OrderedDict[str, ParseObject[Any]] = [
            DeviceId(),
            Function(),
            Address(),
            UInt16Field(name="data count", endian="little"),
            ModbusCRC(),
        ],
    ) -> None:
        super().__init__(
            name=FunctionEnum.ReadCoils.name + "Request",
            data=data,
            children=children,
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
    readCoilsRequest2 = ModbusReadCoilsRequest()
    readCoilsRequest2.parse(readCoilsRequestBytes)
    print(bytes(readCoilsRequestBytes))
    print(readCoilsRequest)
    print(bytes(readCoilsRequest))
    print(readCoilsRequest2)
    print(bytes(readCoilsRequest2))
    if check_crc is True:
        readCoilsRequest.children["crc"].update()
        readCoilsRequest2.crc.update()
        print(readCoilsRequest)
        print(bytes(readCoilsRequest))
        print(readCoilsRequest2)
        print(bytes(readCoilsRequest2))

    readCoilsRequest.value = [
        17,
        1,
        19,
        37,
    ]
    readCoilsRequest.value = [
        17,
        1,
        19,
        37,
    ]
    print(readCoilsRequest)
    print(bytes(readCoilsRequest))
    print(readCoilsRequest2)
    print(bytes(readCoilsRequest2))

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
    print(bytes(readCoilsResponseBytes))
    readCoilsResponse.parse(readCoilsResponseBytes)
    print(bytes(readCoilsResponse))
    print(readCoilsResponse)
    if check_crc is True:
        print(readCoilsResponse.children["crc"].update())
        print(bytes(readCoilsResponse))
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
        print(readDiscreteInputsRequest.children["crc"].update())
        print(readDiscreteInputsRequest)

    readDiscreteInputsRequest.value = [11, 2, 0xC400, 16]


if __name__ == "__main__":
    check_crc = True
    ReadCoils(check_crc=check_crc)
    # ReadDiscreteInputs(check_crc=check_crc)
