# flake8:noqa
from __future__ import annotations

import struct
from typing import Any

import pytest
from bitarray import bitarray
from parse_data import ParseData

from easyprotocol.base.base import DEFAULT_ENDIANNESS
from easyprotocol.fields.array import ArrayFieldGeneric
from easyprotocol.fields.unsigned_int import BoolField, UInt8Field
from easyprotocol.protocols.modbus import (
    ModbusFunctionEnum,
    ModbusTCPReadCoilsRequest,
    ModbusTCPReadCoilsResponse,
    ModbusTCPReadHoldingRegisterRequest,
    ModbusTCPReadHoldingRegisterResponse,
    ModbusTCPWriteHoldingRegisterRequest,
    ModbusTCPWriteHoldingRegisterResponse,
)


class TestModbusTCP:
    def test_modbus_tcp_read_coils_request(self) -> None:
        data = b"\x00\x01\x00\x00\x00\x06\x0a\x01\x00\x00\x00\x01"
        transactionID = 1
        protocolID = 0
        length = 6
        address = 10
        functionCode = ModbusFunctionEnum.ReadCoils.value
        register = 0
        coilCount = 1
        frame = ModbusTCPReadCoilsRequest(data=data)
        assert frame.transactionID.value == transactionID
        assert frame.protocolID.value == protocolID
        assert frame.length.value == length
        assert frame.address.value == address
        assert frame.functionCode.value == functionCode
        assert frame.register.value == register
        assert frame.count.value == coilCount

    def test_modbus_tcp_read_coils_response(self) -> None:
        data = b"\x00\x01\x00\x00\x00\x04\x0a\x01\x01\x00"
        transactionID = 1
        protocolID = 0
        length = 4
        address = 10
        functionCode = ModbusFunctionEnum.ReadCoils.value
        coilValues = [False, False, False, False, False, False, False, False]
        byteCount = 1
        frame = ModbusTCPReadCoilsResponse(data=data)
        assert frame.transactionID.value == transactionID
        assert frame.protocolID.value == protocolID
        assert frame.length.value == length
        assert frame.address.value == address
        assert frame.functionCode.value == functionCode
        assert frame.byteCount.value == byteCount
        assert frame.coilArray.value_list == coilValues

    def test_modbus_tcp_write_single_register_request(self) -> None:
        data = b"\x00\x01\x00\x00\x00\x06\xff\x06\x00\x64\x00\x00"
        transactionID = 1
        protocolID = 0
        length = 6
        address = 255
        functionCode = ModbusFunctionEnum.WriteHoldingRegister.value
        register = 100
        writeValue = 0
        frame = ModbusTCPWriteHoldingRegisterRequest(data=data)
        assert frame.transactionID.value == transactionID
        assert frame.protocolID.value == protocolID
        assert frame.length.value == length
        assert frame.address.value == address
        assert frame.functionCode.value == functionCode
        assert frame.register.value == register
        assert frame.writeValue.value == writeValue

    def test_modbus_tcp_write_single_register_response(self) -> None:
        data = b"\x00\x01\x00\x00\x00\x06\xff\x06\x00\x64\x00\x00"
        transactionID = 1
        protocolID = 0
        length = 6
        address = 255
        functionCode = ModbusFunctionEnum.WriteHoldingRegister.value
        register = 100
        writeValue = 0
        frame = ModbusTCPWriteHoldingRegisterResponse(data=data)
        assert frame.transactionID.value == transactionID
        assert frame.protocolID.value == protocolID
        assert frame.length.value == length
        assert frame.address.value == address
        assert frame.functionCode.value == functionCode
        assert frame.register.value == register
        assert frame.writeValue.value == writeValue

    def test_modbus_tcp_read_holding_registers_request(self) -> None:
        data = b"\x00\x0c\x00\x00\x00\x06\xff\x03\x00\x64\x00\x64"
        transactionID = 12
        protocolID = 0
        length = 6
        address = 255
        functionCode = ModbusFunctionEnum.ReadHoldingRegisters.value
        register = 100
        wordCount = 100
        frame = ModbusTCPReadHoldingRegisterRequest(data=data)
        assert frame.transactionID.value == transactionID
        assert frame.protocolID.value == protocolID
        assert frame.length.value == length
        assert frame.address.value == address
        assert frame.functionCode.value == functionCode
        assert frame.register.value == register
        assert frame.wordCount.value == wordCount

    def test_modbus_tcp_read_holding_registers_response(self) -> None:
        data = (
            b"\x00\x0c\x00\x00\x00\xcb\xff\x03\xc8\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )

        transactionID = 12
        protocolID = 0
        length = 203
        address = 255
        functionCode = ModbusFunctionEnum.ReadHoldingRegisters.value
        byteCount = 200
        register_values = [0] * 100
        frame = ModbusTCPReadHoldingRegisterResponse(data=data)
        assert frame.transactionID.value == transactionID
        assert frame.protocolID.value == protocolID
        assert frame.length.value == length
        assert frame.address.value == address
        assert frame.functionCode.value == functionCode
        assert frame.byteCount.value == byteCount
        assert frame.registerValues.value_list == register_values
