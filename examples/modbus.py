from __future__ import annotations

from collections import dict

from easyprotocol.base.utils import hex
from easyprotocol.protocols.modbus import (
    ModbusAddress,
    ModbusCount,
    ModbusDeviceId,
    ModbusFieldNamesEnum,
    ModbusFunction,
    ModbusReadCoilsRequest,
    ModbusReadCoilsResponse,
    ModbusReadDiscreteInputsRequest,
)
from easyprotocol.protocols.modbus.constants import ModbusFunctionEnum


def ReadCoils(check_crc: bool = False) -> None:
    print(f"┐  {ModbusFunctionEnum.ReadCoils.value}")
    print(f'├─┐  {ModbusFunctionEnum.ReadCoils.value} - {"Request"}')
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
        dict(
            {
                ModbusFieldNamesEnum.DeviceID.value: ModbusDeviceId(default=17),
                ModbusFieldNamesEnum.FunctionCode.value: ModbusFunction(default=ModbusFunctionEnum.ReadCoils),
                ModbusFieldNamesEnum.Address.value: ModbusAddress(default=19),
                ModbusFieldNamesEnum.Count.value: ModbusCount(default=37),
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
    readCoilsResponse.deviceId.set_value(17)
    readCoilsResponse.functionCode.set_value(ModbusFunctionEnum.ReadCoils)
    readCoilsResponse.byteCount.set_value(5)
    readCoilsResponse.coilArray.set_value([0, 1, 2, 3, 4])
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
    readDiscreteInputsRequest.deviceId.set_value(11)
    readDiscreteInputsRequest.functionCode.set_value(ModbusFunctionEnum.ReadDiscreteInputs)
    readDiscreteInputsRequest.address.set_value(0xC400)
    readDiscreteInputsRequest.count.set_value(16)
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
