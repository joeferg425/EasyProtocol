"""Modbus constants."""
from enum import Enum, IntEnum


class ModbusFieldNamesEnum(str, Enum):
    """Modbus field name constants."""

    Address = "address"
    FunctionCode = "function"
    Register = "register"
    CRC = "crc"
    CoilArray = "bit array"
    DiscreteInputArray = "bit array"
    Count = "count"
    ByteCount = "byte count"
    TransactionID = "transactionID"
    ProtocolID = "protocolID"
    Length = "length"


class ModbusFunctionEnum(IntEnum):
    """Modbus function constants."""

    Unknown = 0
    ReadCoils = 1
    ReadDiscreteInputs = 2
    ReadMultipleHoldingRegisters = 3
    ReadMultipleInputRegisters = 4
    WriteSingleCoil = 5
    WriteMultipleHoldingRegister = 6
    WriteMultipleCoils = 15
    WriteMultipleHoldingRegisters = 16
