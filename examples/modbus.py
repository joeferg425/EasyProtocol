"""Simple Modbus Example."""
from __future__ import annotations

from easyprotocol.base.utils import hex
from easyprotocol.protocols.modbus import (
    ModbusAddress,
    ModbusCount,
    ModbusFunction,
    ModbusRTUReadCoilsRequest,
    ModbusRTUReadCoilsResponse,
    ModbusRTUReadDiscreteInputsRequest,
)
from easyprotocol.protocols.modbus.constants import ModbusFunctionEnum


def ReadCoils(check_crc: bool = False) -> None:
    """Test functionality of Modbus Read Coils Function.

    Args:
        check_crc: set true to check crc calculation. Defaults to False.
    """
    print(f"┐  {ModbusFunctionEnum.ReadCoils.value}")
    print(f'├─┐  {ModbusFunctionEnum.ReadCoils.value} - {"Request"}')
    readCoilsRequestBytes = bytearray(b"\x11\x01\x00\x13\x00\x25\x0E\x84")
    print(f"│ ├─ input:\t\t{hex(bytes(readCoilsRequestBytes))}")
    print("│ │")

    readCoilsRequest = ModbusRTUReadCoilsRequest()
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
        [
            ModbusAddress(default=17),
            ModbusFunction(default=ModbusFunctionEnum.ReadCoils),
            ModbusAddress(default=19),
            ModbusCount(default=37),
        ]
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

    readCoilsResponse = ModbusRTUReadCoilsResponse()
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
    readCoilsResponse.address.set_value(17)
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
    """Test function of Modbus Read Discrete Inputs function.

    Args:
        check_crc: set true to check crc calculation. Defaults to False.
    """
    print(f"┐  {ModbusFunctionEnum.ReadDiscreteInputs.name}")
    print(f'├─┐  {ModbusFunctionEnum.ReadDiscreteInputs.name} - {"Request"}')
    readDiscreteInputsRequestBytes = b"\x11\x02\x00\xC4\x00\x16\xBA\xA9"
    print(f"│ ├─ input:\t\t{hex(bytes(readDiscreteInputsRequestBytes))}")
    print("│ │")

    readDiscreteInputsRequest = ModbusRTUReadDiscreteInputsRequest()
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
    readDiscreteInputsRequest.address.set_value(11)
    readDiscreteInputsRequest.functionCode.set_value(ModbusFunctionEnum.ReadDiscreteInputs)
    readDiscreteInputsRequest.register.set_value(0xC400)
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
