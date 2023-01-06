"""Modbus parser classes."""
from __future__ import annotations

from typing import Sequence, cast

from easyprotocol.base import ParseFieldDict, dataT
from easyprotocol.base.parse_base import ParseBase
from easyprotocol.base.parse_field_dict import K, T, parseGenericT
from easyprotocol.protocols.modbus.constants import (
    ModbusFieldNamesEnum,
    ModbusFunctionEnum,
)
from easyprotocol.protocols.modbus.fields import (
    ModbusAddress,
    ModbusByteCount,
    ModbusCoilArray,
    ModbusCount,
    ModbusCRC,
    ModbusDiscreteInputArray,
    ModbusFunction,
    ModbusLength,
    ModbusProtocolID,
    ModbusRegister,
    ModbusTransactionID,
)


class ModbusRTUFrame(ParseFieldDict):
    """Modbus header fields plus the checksum."""

    def __init__(
        self,
        function: ModbusFunctionEnum = ModbusFunctionEnum.ReadCoils,
        crc: int = 0,
        name: str = "modbusRTUHeader",
        data: dataT | None = None,
        address: int = 1,
        update_crc: bool = False,
        additional_fields: Sequence[ParseBase] | Sequence[ParseBase] | Sequence[parseGenericT[K, T]] | None = None,
    ) -> None:
        """Modbus header fields plus the checksum.

        Args:
            function: modbus function code
            crc: checksum value Defaults to 0.
            name: Defaults to "modbusHeader".
            data: data to parse.
            address: modbus device id, defaults to 1.
            update_crc: set true to calculate the checksum after assigning all field values.
            additional_fields: fields to add between header and checksum.
        """
        _crc = ModbusCRC(default=crc)
        if additional_fields is None:
            additional_fields = []
        super().__init__(
            name=name,
            data=data,
            default=[
                ModbusAddress(default=address),
                ModbusFunction(default=function),
            ]
            + list(additional_fields)
            + [
                _crc,
            ],
        )
        if update_crc is True:
            _crc.update_field()

    @property
    def address(self) -> ModbusAddress:
        """Get the modbus device id.

        Returns:
            the modbus device id
        """
        return cast(ModbusAddress, self[ModbusFieldNamesEnum.Address.value])

    @address.setter
    def address(self, value: int | ModbusAddress) -> None:
        if isinstance(value, ModbusAddress):
            self[ModbusFieldNamesEnum.Address.value] = value
        else:
            address = cast(ModbusAddress, self[ModbusFieldNamesEnum.Address.value])
            address.value = value

    @property
    def functionCode(self) -> ModbusFunction:
        """Get the modbus function code.

        Returns:
            the modbus function code
        """
        return cast(ModbusFunction, self[ModbusFieldNamesEnum.FunctionCode.value])

    @functionCode.setter
    def functionCode(self, value: ModbusFunctionEnum) -> None:
        if isinstance(value, ModbusFunction):
            self[ModbusFieldNamesEnum.FunctionCode.value] = value
        else:
            func = cast(ModbusFunction, self[ModbusFieldNamesEnum.FunctionCode.value])
            func.value = value

    @property
    def crc(self) -> ModbusCRC:
        """Get the modbus crc.

        Returns:
            the modbus crc
        """
        return cast(ModbusCRC, self[ModbusFieldNamesEnum.CRC.value])

    @crc.setter
    def crc(self, value: int) -> None:
        if isinstance(value, ModbusCRC):
            self[ModbusFieldNamesEnum.CRC.value] = value
        else:
            crc = cast(ModbusCRC, self[ModbusFieldNamesEnum.CRC.value])
            crc.value = value


class ModbusTCPFrame(ParseFieldDict):
    """Modbus header fields plus the checksum."""

    def __init__(
        self,
        function: ModbusFunctionEnum = ModbusFunctionEnum.ReadCoils,
        name: str = "modbusTCPHeader",
        data: dataT | None = None,
        transaction_id: int = 0,
        protocol_id: int = 0,
        length: int | None = None,
        address: int = 1,
        additional_fields: Sequence[ParseBase] | Sequence[ParseBase] | Sequence[parseGenericT[K, T]] | None = None,
    ) -> None:
        """Modbus header fields plus the checksum.

        Args:
            function: modbus function code
            name: Defaults to "modbusHeader".
            transaction_id: transaction id value
            protocol_id: protocol id value
            length: auto calculated if None
            data: data to parse.
            address: modbus device id, defaults to 1.
            additional_fields: fields to add between header and checksum.
        """
        __length = 0
        if length is not None:
            __length = length
        _length = ModbusLength(default=__length)
        if additional_fields is None:
            additional_fields = []
        super().__init__(
            name=name,
            data=data,
            default=[
                ModbusTransactionID(default=transaction_id),
                ModbusProtocolID(default=protocol_id),
                _length,
                ModbusAddress(default=address),
                ModbusFunction(default=function),
            ]
            + list(additional_fields),
        )
        if length is None:
            frame_len = len(self.byte_value) - 6
            _length.set_value(frame_len)

    @property
    def address(self) -> ModbusAddress:
        """Get the modbus device id.

        Returns:
            the modbus device id
        """
        return cast(ModbusAddress, self[ModbusFieldNamesEnum.Address.value])

    @address.setter
    def address(self, value: int | ModbusAddress) -> None:
        if isinstance(value, ModbusAddress):
            self[ModbusFieldNamesEnum.Address.value] = value
        else:
            address = cast(ModbusAddress, self[ModbusFieldNamesEnum.Address.value])
            address.value = value

    @property
    def functionCode(self) -> ModbusFunction:
        """Get the modbus function code.

        Returns:
            the modbus function code
        """
        return cast(ModbusFunction, self[ModbusFieldNamesEnum.FunctionCode.value])

    @functionCode.setter
    def functionCode(self, value: ModbusFunctionEnum) -> None:
        if isinstance(value, ModbusFunction):
            self[ModbusFieldNamesEnum.FunctionCode.value] = value
        else:
            func = cast(ModbusFunction, self[ModbusFieldNamesEnum.FunctionCode.value])
            func.value = value

    @property
    def crc(self) -> ModbusCRC:
        """Get the modbus crc.

        Returns:
            the modbus crc
        """
        return cast(ModbusCRC, self[ModbusFieldNamesEnum.CRC.value])

    @crc.setter
    def crc(self, value: int) -> None:
        if isinstance(value, ModbusCRC):
            self[ModbusFieldNamesEnum.CRC.value] = value
        else:
            crc = cast(ModbusCRC, self[ModbusFieldNamesEnum.CRC.value])
            crc.value = value


class ModbusRTUReadCoilsRequest(ModbusRTUFrame):
    """Modbus read coils request frame."""

    def __init__(
        self,
        address: int = 1,
        register: int = 0,
        count: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus read coils request frame.

        Args:
            address: modbus device id
            register: modbus coil register. Defaults to 0.
            count: modbus coil count
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=ModbusFunctionEnum.ReadCoils.name + "Request",
            data=data,
            address=address,
            function=ModbusFunctionEnum.ReadCoils,
            additional_fields=[
                ModbusRegister(default=register),
                ModbusCount(default=count),
            ],
            update_crc=True,
        )

    @property
    def register(self) -> ModbusRegister:
        """Get modbus coil register.

        Returns:
            modbus coil register
        """
        return cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])

    @register.setter
    def register(self, value: int) -> None:
        if isinstance(value, ModbusRegister):
            self[ModbusFieldNamesEnum.Register.value] = value
        else:
            addr = cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])
            addr.value = value

    @property
    def count(self) -> ModbusCount:
        """Get modbus coil count.

        Returns:
            modbus coil count
        """
        return cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])

    @count.setter
    def count(self, value: int) -> None:
        if isinstance(value, ModbusCount):
            self[ModbusFieldNamesEnum.Count.value] = value
        else:
            count = cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])
            count.value = value


class ModbusTCPReadCoilsRequest(ModbusTCPFrame):
    """Modbus read coils request frame."""

    def __init__(
        self,
        transaction_id: int = 0,
        protocol_id: int = 0,
        length: int | None = None,
        address: int = 1,
        register: int = 0,
        count: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus read coils request frame.

        Args:
            transaction_id: transaction id value
            protocol_id: protocol id value
            length: auto calculated if None
            address: modbus device id
            register: modbus coil register. Defaults to 0.
            count: modbus coil count
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=ModbusFunctionEnum.ReadCoils.name + "Request",
            data=data,
            transaction_id=transaction_id,
            protocol_id=protocol_id,
            length=length,
            address=address,
            function=ModbusFunctionEnum.ReadCoils,
            additional_fields=[
                ModbusRegister(default=register),
                ModbusCount(default=count),
            ],
        )

    @property
    def register(self) -> ModbusRegister:
        """Get modbus coil register.

        Returns:
            modbus coil register
        """
        return cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])

    @register.setter
    def register(self, value: int) -> None:
        if isinstance(value, ModbusRegister):
            self[ModbusFieldNamesEnum.Register.value] = value
        else:
            addr = cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])
            addr.value = value

    @property
    def count(self) -> ModbusCount:
        """Get modbus coil count.

        Returns:
            modbus coil count
        """
        return cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])

    @count.setter
    def count(self, value: int) -> None:
        if isinstance(value, ModbusCount):
            self[ModbusFieldNamesEnum.Count.value] = value
        else:
            count = cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])
            count.value = value


class ModbusRTUReadCoilsResponse(ModbusRTUFrame):
    """Modbus read coils response frame."""

    def __init__(
        self,
        address: int = 1,
        register: int = 0,
        byte_count: int = 0,
        coil_array: list[bool] | None = None,
        data: dataT | None = None,
    ) -> None:
        """Create modbus read coils response frame.

        Args:
            address: modbus device id
            register: modbus coil register. Defaults to 0.
            byte_count: byte count coils math.ceil(coil count / 8)
            coil_array: list of boolean values to use as the coil values
            data: data to parse. Defaults to None.
        """
        count_field = ModbusByteCount(default=byte_count)
        super().__init__(
            name=ModbusFunctionEnum.ReadCoils.name + "Response",
            address=address,
            function=ModbusFunctionEnum.ReadCoils,
            data=data,
            additional_fields=[
                ModbusRegister(default=register),
                count_field,
                ModbusCoilArray(
                    count=count_field,
                    default=coil_array,
                ),
            ],
            update_crc=True,
        )

    @property
    def register(self) -> ModbusRegister:
        """Get modbus coil register.

        Returns:
            modbus coil register
        """
        return cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])

    @register.setter
    def register(self, value: int) -> None:
        if isinstance(value, ModbusRegister):
            self[ModbusFieldNamesEnum.Register.value] = value
        else:
            addr = cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])
            addr.value = value

    @property
    def byteCount(self) -> ModbusByteCount:
        """Get modbus coil byte count.

        Returns:
            modbus coil byte count
        """
        return cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])

    @byteCount.setter
    def byteCount(self, value: int) -> None:
        if isinstance(value, ModbusByteCount):
            self[ModbusFieldNamesEnum.ByteCount.value] = value
        else:
            count = cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])
            count.value = value

    @property
    def coilArray(self) -> ModbusCoilArray:
        """Get modbus coil array.

        Returns:
            modbus coil array
        """
        return cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])

    @coilArray.setter
    def coilArray(self, value: Sequence[bool] | Sequence[int]) -> None:
        if isinstance(value, ModbusCoilArray):
            self[ModbusFieldNamesEnum.CoilArray.value].value = value.value
        else:
            func = cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])
            func.set_value(value)


class ModbusTCPReadCoilsResponse(ModbusTCPFrame):
    """Modbus read coils response frame."""

    def __init__(
        self,
        transaction_id: int = 0,
        protocol_id: int = 0,
        length: int | None = None,
        address: int = 1,
        byte_count: int = 0,
        coil_array: list[bool] | None = None,
        data: dataT | None = None,
    ) -> None:
        """Create modbus read coils response frame.

        Args:
            transaction_id: transaction id value
            protocol_id: protocol id value
            length: auto calculated if None
            address: modbus device id
            byte_count: byte count coils math.ceil(coil count / 8)
            coil_array: list of boolean values to use as the coil values
            data: data to parse. Defaults to None.
        """
        count_field = ModbusByteCount(default=byte_count)
        super().__init__(
            name=ModbusFunctionEnum.ReadCoils.name + "Response",
            transaction_id=transaction_id,
            protocol_id=protocol_id,
            length=length,
            address=address,
            function=ModbusFunctionEnum.ReadCoils,
            data=data,
            additional_fields=[
                count_field,
                ModbusCoilArray(
                    count=count_field,
                    default=coil_array,
                ),
            ],
        )

    @property
    def register(self) -> ModbusRegister:
        """Get modbus coil register.

        Returns:
            modbus coil register
        """
        return cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])

    @register.setter
    def register(self, value: int) -> None:
        if isinstance(value, ModbusRegister):
            self[ModbusFieldNamesEnum.Register.value] = value
        else:
            addr = cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])
            addr.value = value

    @property
    def byteCount(self) -> ModbusByteCount:
        """Get modbus coil byte count.

        Returns:
            modbus coil byte count
        """
        return cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])

    @byteCount.setter
    def byteCount(self, value: int) -> None:
        if isinstance(value, ModbusByteCount):
            self[ModbusFieldNamesEnum.ByteCount.value] = value
        else:
            count = cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])
            count.value = value

    @property
    def coilArray(self) -> ModbusCoilArray:
        """Get modbus coil array.

        Returns:
            modbus coil array
        """
        return cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])

    @coilArray.setter
    def coilArray(self, value: Sequence[bool] | Sequence[int]) -> None:
        if isinstance(value, ModbusCoilArray):
            self[ModbusFieldNamesEnum.CoilArray.value].value = value.value
        else:
            func = cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])
            func.set_value(value)


class ModbusRTUReadDiscreteInputsRequest(ModbusRTUFrame):
    """Modbus read discrete inputs request frame."""

    def __init__(
        self,
        address: int = 1,
        register: int = 0,
        count: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus read discrete inputs request frame.

        Args:
            address: modbus address
            register: modbus discrete input register. Defaults to 0.
            count: discrete input count
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=ModbusFunctionEnum.ReadDiscreteInputs.name + "Request",
            function=ModbusFunctionEnum.ReadDiscreteInputs,
            data=data,
            address=address,
            additional_fields=[
                ModbusRegister(
                    default=register,
                ),
                ModbusCount(
                    default=count,
                ),
            ],
            update_crc=True,
        )

    @property
    def register(self) -> ModbusRegister:
        """Get modbus coil register.

        Returns:
            modbus coil register
        """
        return cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])

    @register.setter
    def register(self, value: int) -> None:
        if isinstance(value, ModbusRegister):
            self[ModbusFieldNamesEnum.Register.value] = value
        else:
            addr = cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])
            addr.value = value

    @property
    def count(self) -> ModbusCount:
        """Get modbus input count.

        Returns:
            modbus input count
        """
        return cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])

    @count.setter
    def count(self, value: int) -> None:
        if isinstance(value, ModbusCount):
            self[ModbusFieldNamesEnum.Count.value] = value
        else:
            func = cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])
            func.set_value(value)


class ModbusTCPReadDiscreteInputsRequest(ModbusTCPFrame):
    """Modbus read discrete inputs request frame."""

    def __init__(
        self,
        address: int = 1,
        register: int = 0,
        count: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus read discrete inputs request frame.

        Args:
            address: modbus address
            register: modbus discrete input register. Defaults to 0.
            count: discrete input count
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=ModbusFunctionEnum.ReadDiscreteInputs.name + "Request",
            function=ModbusFunctionEnum.ReadDiscreteInputs,
            data=data,
            address=address,
            additional_fields=[
                ModbusRegister(
                    default=register,
                ),
                ModbusCount(
                    default=count,
                ),
            ],
        )

    @property
    def register(self) -> ModbusRegister:
        """Get modbus coil register.

        Returns:
            modbus coil register
        """
        return cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])

    @register.setter
    def register(self, value: int) -> None:
        if isinstance(value, ModbusRegister):
            self[ModbusFieldNamesEnum.Register.value] = value
        else:
            addr = cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])
            addr.value = value

    @property
    def count(self) -> ModbusCount:
        """Get modbus input count.

        Returns:
            modbus input count
        """
        return cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])

    @count.setter
    def count(self, value: int) -> None:
        if isinstance(value, ModbusCount):
            self[ModbusFieldNamesEnum.Count.value] = value
        else:
            func = cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])
            func.set_value(value)


class ModbusRTUReadDiscreteInputsResponse(ModbusRTUFrame):
    """Modbus read discrete inputs response frame."""

    def __init__(
        self,
        address: int = 1,
        register: int = 0,
        byte_count: int = 0,
        coil_array: list[bool] | None = None,
        data: dataT | None = None,
    ) -> None:
        """Create modbus read discrete inputs response frame.

        Args:
            address: modbus device id
            register: modbus coil register. Defaults to 0.
            byte_count: byte count coils math.ceil(coil count / 8)
            coil_array: list of boolean values to use as the coil values
            data: data to parse. Defaults to None.
        """
        count_field = ModbusByteCount(default=byte_count)
        super().__init__(
            name=ModbusFunctionEnum.ReadDiscreteInputs.name + "Response",
            address=address,
            function=ModbusFunctionEnum.ReadDiscreteInputs,
            data=data,
            additional_fields=[
                ModbusRegister(default=register),
                count_field,
                ModbusDiscreteInputArray(
                    count=count_field,
                    default=coil_array,
                ),
            ],
            update_crc=True,
        )

    @property
    def register(self) -> ModbusRegister:
        """Get modbus coil register.

        Returns:
            modbus coil register
        """
        return cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])

    @register.setter
    def register(self, value: int) -> None:
        if isinstance(value, ModbusRegister):
            self[ModbusFieldNamesEnum.Register.value] = value
        else:
            addr = cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])
            addr.value = value

    @property
    def byteCount(self) -> ModbusByteCount:
        """Get modbus coil byte count.

        Returns:
            modbus coil byte count
        """
        return cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])

    @byteCount.setter
    def byteCount(self, value: int) -> None:
        if isinstance(value, ModbusByteCount):
            self[ModbusFieldNamesEnum.ByteCount.value] = value
        else:
            count = cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])
            count.value = value

    @property
    def coilArray(self) -> ModbusCoilArray:
        """Get modbus coil array.

        Returns:
            modbus coil array
        """
        return cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])

    @coilArray.setter
    def coilArray(self, value: Sequence[bool] | Sequence[int]) -> None:
        if isinstance(value, ModbusCoilArray):
            self[ModbusFieldNamesEnum.CoilArray.value].value = value.value
        else:
            func = cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])
            func.set_value(value)


class ModbusTCPReadDiscreteInputsResponse(ModbusTCPFrame):
    """Modbus read discrete inputs response frame."""

    def __init__(
        self,
        transaction_id: int = 0,
        protocol_id: int = 0,
        length: int | None = None,
        address: int = 1,
        byte_count: int = 0,
        discrete_input_array: list[bool] | None = None,
        data: dataT | None = None,
    ) -> None:
        """Create modbus read discrete inputs response frame.

        Args:
            transaction_id: transaction id value
            protocol_id: protocol id value
            length: auto calculated if None
            address: modbus device id
            byte_count: byte count coils math.ceil(coil count / 8)
            discrete_input_array: list of boolean values to use as the coil values
            data: data to parse. Defaults to None.
        """
        count_field = ModbusByteCount(default=byte_count)
        super().__init__(
            name=ModbusFunctionEnum.ReadDiscreteInputs.name + "Response",
            transaction_id=transaction_id,
            protocol_id=protocol_id,
            length=length,
            address=address,
            function=ModbusFunctionEnum.ReadDiscreteInputs,
            data=data,
            additional_fields=[
                count_field,
                ModbusDiscreteInputArray(
                    count=count_field,
                    default=discrete_input_array,
                ),
            ],
        )

    @property
    def register(self) -> ModbusRegister:
        """Get modbus coil register.

        Returns:
            modbus coil register
        """
        return cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])

    @register.setter
    def register(self, value: int) -> None:
        if isinstance(value, ModbusRegister):
            self[ModbusFieldNamesEnum.Register.value] = value
        else:
            addr = cast(ModbusRegister, self[ModbusFieldNamesEnum.Register.value])
            addr.value = value

    @property
    def byteCount(self) -> ModbusByteCount:
        """Get modbus coil byte count.

        Returns:
            modbus coil byte count
        """
        return cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])

    @byteCount.setter
    def byteCount(self, value: int) -> None:
        if isinstance(value, ModbusByteCount):
            self[ModbusFieldNamesEnum.ByteCount.value] = value
        else:
            count = cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])
            count.value = value

    @property
    def coilArray(self) -> ModbusCoilArray:
        """Get modbus coil array.

        Returns:
            modbus coil array
        """
        return cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])

    @coilArray.setter
    def coilArray(self, value: Sequence[bool] | Sequence[int]) -> None:
        if isinstance(value, ModbusCoilArray):
            self[ModbusFieldNamesEnum.CoilArray.value].value = value.value
        else:
            func = cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])
            func.set_value(value)
