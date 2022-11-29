from __future__ import annotations

from collections import OrderedDict

from easyprotocol.base.utils import hex
from easyprotocol.protocols.modbus import (
    ModbusFieldNames,
    ModbusReadCoilsRequest,
    ModbusReadCoilsResponse,
    ModbusReadDiscreteInputsRequest,
)
from easyprotocol.protocols.modbus.constants import ModbusFunctionEnum


def ReadCoils(check_crc: bool = False) -> None:
    print(f"┐  {ModbusFunctionEnum.ReadCoils.name}")
    print(f'├─┐  {ModbusFunctionEnum.ReadCoils.name} - {"Request"}')
    readCoilsRequestBytes = bytearray(b"\x11\x01\x00\x13\x00\x25\x0E\x84")
    print(f"│ ├─ input:\t\t{hex(bytes(readCoilsRequestBytes))}")
    print("│ │")

    readCoilsRequest = ModbusReadCoilsRequest()
    readCoilsRequest.parse(readCoilsRequestBytes)
    print(f"│ ├─ parser:\t\t{readCoilsRequest}")
    print(f"│ ├─ parser bytes:\t{hex(bytes(readCoilsRequest))}")
    print("│ │")

    if check_crc is True:
        print("│ ├─┐  Recalculating CRC")
        readCoilsRequest.crc.update_field()
        print(f"│ │ ├─ parser:\t\t{readCoilsRequest}")
        print(f"│ │ ├─ parser bytes:\t{hex(bytes(readCoilsRequest))}")
        print("│ ├─┘")
        print("│ │")

    print("│ ├─┐  Changing Frame data")
    readCoilsRequest.set_value(
        OrderedDict(
            {
                ModbusFieldNames.DeviceID.name: 17,
                ModbusFieldNames.FunctionCode.name: 1,
                ModbusFieldNames.Address.name: 19,
                ModbusFieldNames.Count.name: 37,
            }
        )
    )
    print(f"│ │ ├─ parser:\t\t{readCoilsRequest}")
    print(f"│ │ ├─ parser bytes:\t{hex(bytes(readCoilsRequest))}")
    print("│ │ │")
    print("│ │ ├─┐  Recalculating CRC")
    readCoilsRequest.crc.update_field()
    print(f"│ │ │ ├─ parser:\t{readCoilsRequest}")
    print(f"│ │ │ ├─ parser bytes:\t{hex(bytes(readCoilsRequest))}")
    print("│ │ ├─┘")
    print("│ ├─┘")
    print("├─┘")

    print(f'├─┐  {ModbusFunctionEnum.ReadCoils.name} - {"Response"}')
    readCoilsResponseBytes = bytearray(b"\x11\x01\x05\xCD\x6B\xB2\x0E\x1B\x45\xE6")
    print(f"│ ├─ input:\t\t{hex(bytes(readCoilsResponseBytes))}")
    print("│ │")

    readCoilsResponse = ModbusReadCoilsResponse()
    readCoilsResponse.parse(readCoilsResponseBytes)
    print(f"│ ├─ parser:\t\t{readCoilsResponse}")
    print(f"│ ├─ parser bytes:\t{hex(bytes(readCoilsResponse))}")
    print("│ │")
    if check_crc is True:
        print("│ ├─┐  Recalculating CRC")
        readCoilsResponse.crc.update_field()
        print(f"│ │ ├─ parser:\t{readCoilsResponse}")
        print(f"│ │ ├─ parser bytes:\t{hex(bytes(readCoilsResponse))}")
        print("│ ├─┘")
        print("│ │")

    print("│ ├─┐  Changing Frame data")
    readCoilsResponse.set_value(
        OrderedDict(
            {
                ModbusFieldNames.DeviceID.name: 17,
                ModbusFieldNames.FunctionCode.name: 1,
                ModbusFieldNames.ByteCount.name: 5,
                ModbusFieldNames.CoilArray.name: [0, 1, 2, 3, 4],
            }
        )
    )
    print(f"│ │ ├─ parser:\t\t{readCoilsResponse}")
    print(f"│ │ ├─ parser bytes:\t{hex(bytes(readCoilsResponse))}")
    print("│ │ │")
    print("│ │ ├─┐  Recalculating CRC")
    readCoilsResponse.crc.update_field()
    print(f"│ │ │ ├─ parser:\t\t{readCoilsResponse}")
    print(f"│ │ │ ├─ parser bytes:\t{hex(bytes(readCoilsResponse))}")
    print("│ │ ├─┘")
    print("│ ├─┘")
    print("├─┘")
    print("┘")


def ReadDiscreteInputs(check_crc: bool = False) -> None:
    print(f"┐  {ModbusFunctionEnum.ReadDiscreteInputs.name}")
    print(f'├─┐  {ModbusFunctionEnum.ReadDiscreteInputs.name} - {"Request"}')
    readDiscreteInputsRequestBytes = b"\x11\x02\x00\xC4\x00\x16\xBA\xA9"
    print(f"│ ├─ input:\t\t{hex(bytes(readDiscreteInputsRequestBytes))}")
    print("│ │")

    readDiscreteInputsRequest = ModbusReadDiscreteInputsRequest()
    readDiscreteInputsRequest.parse(readDiscreteInputsRequestBytes)
    print(f"│ ├─ parser:\t\t{readDiscreteInputsRequest}")
    print(f"│ ├─ parser bytes:\t{hex(bytes(readDiscreteInputsRequest))}")
    print("│ │")

    if check_crc is True:
        readDiscreteInputsRequest.crc.update_field()
        print("│ ├─┐  Recalculating CRC")
        print(f"│ │ ├─ parser:\t\t{readDiscreteInputsRequest}")
        print(f"│ │ ├─ parser bytes:\t{hex(bytes(readDiscreteInputsRequest))}")
        print("│ ├─┘")

    print("│ ├─┐  Changing Frame data")
    readDiscreteInputsRequest.set_value(
        OrderedDict(
            {
                ModbusFieldNames.DeviceID.name: 11,
                ModbusFieldNames.FunctionCode.name: 2,
                ModbusFieldNames.Address.name: 0xC400,
                ModbusFieldNames.Count.name: 16,
            }
        )
    )
    print(f"│ │ ├─ parser:\t\t{readDiscreteInputsRequest}")
    print(f"│ │ ├─ parser bytes:\t{hex(bytes(readDiscreteInputsRequest))}")
    print("│ │ ├─┐  Recalculating CRC")
    readDiscreteInputsRequest.crc.update_field()
    print(f"│ │ │ ├─ parser:\t{readDiscreteInputsRequest}")
    print(f"│ │ │ ├─ parser bytes:\t{hex(bytes(readDiscreteInputsRequest))}")
    print("│ │ ├─┘")
    print("│ ├─┘")
    print("├─┘")
    print("┘")


if __name__ == "__main__":
    check_crc = True
    ReadCoils(check_crc=check_crc)
    ReadDiscreteInputs(check_crc=check_crc)
