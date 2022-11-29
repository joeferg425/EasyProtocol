from __future__ import annotations

from collections import OrderedDict
from typing import Any, cast

from easyprotocol.base import ParseBase, ParseDict, dataT
from easyprotocol.protocols.modbus.constants import ModbusFieldNames, ModbusFunctionEnum
from easyprotocol.protocols.modbus.fields import (
    ModbusAddress,
    ModbusByteCount,
    ModbusCoilArray,
    ModbusCount,
    ModbusCRC,
    ModbusDeviceId,
    ModbusFunction,
)


class ModbusHeader(ParseDict):
    def __init__(
        self,
        name: str = "modbusHeader",
        data: dataT | None = None,
        children: list[ParseBase[Any]]
        | OrderedDict[str, ParseBase[Any]] = [
            ModbusDeviceId(),
            ModbusFunction(),
            ModbusAddress(),
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
    def deviceId(self) -> ModbusDeviceId:
        return cast(ModbusDeviceId, self[ModbusFieldNames.DeviceID])

    @deviceId.setter
    def deviceId(self, value: ModbusDeviceId | int) -> None:
        if isinstance(value, ModbusDeviceId):
            self[ModbusFieldNames.DeviceID] = value
        else:
            self[ModbusFieldNames.DeviceID].value = value

    @property
    def functionCode(self) -> ModbusFunction:
        return cast(ModbusFunction, self[ModbusFieldNames.FunctionCode])

    @functionCode.setter
    def functionCode(self, value: ModbusFunction | int | ModbusFunctionEnum) -> None:
        if isinstance(value, ModbusFunction):
            self[ModbusFieldNames.FunctionCode] = value
        else:
            self[ModbusFieldNames.FunctionCode].value = value

    @property
    def address(self) -> ModbusAddress:
        return cast(ModbusAddress, self[ModbusFieldNames.Address])

    @address.setter
    def address(self, value: ModbusAddress | int) -> None:
        if isinstance(value, ModbusAddress):
            self[ModbusFieldNames.Address] = value
        else:
            self[ModbusFieldNames.Address].value = value

    @property
    def crc(self) -> ModbusCRC:
        return cast(ModbusCRC, self[ModbusFieldNames.CRC])

    @crc.setter
    def crc(self, value: ModbusCRC | int) -> None:
        if isinstance(value, ModbusCRC):
            self[ModbusFieldNames.CRC] = value
        else:
            self[ModbusFieldNames.CRC].value = value


class ModbusReadCoilsRequest(ModbusHeader):
    def __init__(
        self,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFunctionEnum.ReadCoils.name + "Request",
            data=data,
            children=[
                ModbusDeviceId(),
                ModbusFunction(),
                ModbusAddress(),
                ModbusCount(),
                ModbusCRC(),
            ],
        )


class ModbusReadCoilsResponse(ModbusHeader):
    def __init__(
        self,
        data: dataT | None = None,
    ) -> None:
        count_field = ModbusByteCount()
        super().__init__(
            name=ModbusFunctionEnum.ReadCoils.name + "Response",
            data=data,
            children=[
                ModbusDeviceId(),
                ModbusFunction(),
                count_field,
                ModbusCoilArray(count=count_field),
                ModbusCRC(),
            ],
        )


class ModbusReadDiscreteInputsRequest(ModbusHeader):
    def __init__(
        self,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFunctionEnum.ReadDiscreteInputs.name + "Request",
            data=data,
            children=[
                ModbusDeviceId(),
                ModbusFunction(),
                ModbusAddress(),
                ModbusCount(),
                ModbusCRC(),
            ],
        )
