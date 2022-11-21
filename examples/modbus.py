from __future__ import annotations
from easyprotocol.protocols.modbus import (
    ModbusReadCoilsRequest,
    ModbusReadCoilsResponse,
    ModbusFieldNames,
    ModbusReadDiscreteInputsRequest,
)
from easyprotocol.protocols.modbus.constants import ModbusFunctionEnum
from easyprotocol.utils import hex


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
        readCoilsRequest.crc.update()
        print(f"│ │ ├─ parser:\t\t{readCoilsRequest}")
        print(f"│ │ ├─ parser bytes:\t{hex(bytes(readCoilsRequest))}")
        print("│ ├─┘")
        print("│ │")

    print("│ ├─┐  Changing Frame data")
    readCoilsRequest.value = {
        ModbusFieldNames.DeviceID: 17,
        ModbusFieldNames.FunctionCode: 1,
        ModbusFieldNames.Address: 19,
        ModbusFieldNames.Count: 37,
    }
    print(f"│ │ ├─ parser:\t\t{readCoilsRequest}")
    print(f"│ │ ├─ parser bytes:\t{hex(bytes(readCoilsRequest))}")
    print("│ │ │")
    print("│ │ ├─┐  Recalculating CRC")
    readCoilsRequest.crc.update()
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
        readCoilsResponse.crc.update()
        print(f"│ │ ├─ parser:\t{readCoilsResponse}")
        print(f"│ │ ├─ parser bytes:\t{hex(bytes(readCoilsResponse))}")
        print("│ ├─┘")
        print("│ │")

    print("│ ├─┐  Changing Frame data")
    readCoilsResponse.value = {
        ModbusFieldNames.DeviceID: 17,
        ModbusFieldNames.FunctionCode: 1,
        ModbusFieldNames.ByteCount: 5,
        ModbusFieldNames.CoilArray: [0, 1, 2, 3, 4],
    }
    print(f"│ │ ├─ parser:\t\t{readCoilsResponse}")
    print(f"│ │ ├─ parser bytes:\t{hex(bytes(readCoilsResponse))}")
    print("│ │ │")
    print("│ │ ├─┐  Recalculating CRC")
    readCoilsResponse.crc.update()
    print(f"│ │ │ ├─ parser:\t{readCoilsResponse}")
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
        readDiscreteInputsRequest.crc.update()
        print("│ ├─┐  Recalculating CRC")
        print(f"│ │ ├─ parser:\t\t{readDiscreteInputsRequest}")
        print(f"│ │ ├─ parser bytes:\t{hex(bytes(readDiscreteInputsRequest))}")
        print("│ ├─┘")

    print("│ ├─┐  Changing Frame data")
    readDiscreteInputsRequest.value = {
        ModbusFieldNames.DeviceID: 11,
        ModbusFieldNames.FunctionCode: 2,
        ModbusFieldNames.Address: 0xC400,
        ModbusFieldNames.Count: 16,
    }
    print(f"│ │ ├─ parser:\t\t{readDiscreteInputsRequest}")
    print(f"│ │ ├─ parser bytes:\t{hex(bytes(readDiscreteInputsRequest))}")
    print("│ │ ├─┐  Recalculating CRC")
    readDiscreteInputsRequest.crc.update()
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
