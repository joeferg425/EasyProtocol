"""Modbus field classes."""
from __future__ import annotations

import struct
from typing import Sequence

import crc
from bitarray import bitarray
from bitarray.util import int2ba

from easyprotocol.base import dataT, input_to_bytes
from easyprotocol.fields import (
    BoolField,
    ChecksumField,
    ParseArrayField,
    UInt8EnumField,
    UInt8Field,
    UInt16Field,
    UIntField,
)
from easyprotocol.protocols.modbus.constants import (
    ModbusFieldNamesEnum,
    ModbusFunctionEnum,
)


class ModbusAddress(UInt8Field):
    """Modbus device id field."""

    def __init__(
        self,
        default: int = 1,
        data: dataT | None = None,
    ) -> None:
        """Create modbus device id field.

        Args:
            default: default device id value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.Address.value,
            data=data,
            default=default,
            endian="big",
        )


class ModbusFunction(UInt8EnumField[ModbusFunctionEnum]):
    """Modbus function field."""

    def __init__(
        self,
        default: ModbusFunctionEnum = ModbusFunctionEnum.ReadCoils,
        data: dataT | None = None,
    ) -> None:
        """Create modbus function field.

        Args:
            default: default function value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.FunctionCode.value,
            enum_type=ModbusFunctionEnum,
            default=default,
            data=data,
            endian="little",
        )


class ModbusRegister(UInt16Field):
    """Modbus register field."""

    def __init__(
        self,
        default: int = 1,
        data: dataT | None = None,
    ) -> None:
        """Create modbus register field.

        Args:
            default: default register value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.Register.value,
            default=default,
            data=data,
            endian="big",
        )


class ModbusTransactionID(UInt16Field):
    """Modbus register field."""

    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus register field.

        Args:
            default: default register value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.TransactionID.value,
            default=default,
            data=data,
            endian="big",
        )


class ModbusProtocolID(UInt16Field):
    """Modbus register field."""

    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus register field.

        Args:
            default: default register value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.ProtocolID.value,
            default=default,
            data=data,
            endian="big",
        )


class ModbusLength(UInt16Field):
    """Modbus register field."""

    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus register field.

        Args:
            default: default register value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.Length.value,
            default=default,
            data=data,
            endian="big",
        )


class ModbusCount(UInt16Field):
    """Modbus count field."""

    def __init__(
        self,
        default: int = 1,
        data: dataT | None = None,
    ) -> None:
        """Create modbus count field.

        Args:
            default: default count value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.Count.value,
            default=default,
            data=data,
            endian="big",
            string_format="{}",
        )


class ModbusByteCount(UInt8Field):
    """Modbus byte count field."""

    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus byte count field.

        Args:
            default: default byte count value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.ByteCount.value,
            default=default,
            data=data,
            endian="big",
            string_format="{}",
        )


class ModbusCRC(ChecksumField):
    """Modbus Cyclic Redundancy Checksum (CRC) field."""

    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create modbus Cyclic Redundancy Checksum (CRC) field.

        Args:
            default: default crc value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.CRC.value,
            bit_count=16,
            default=default,
            crc_configuration=crc.Configuration(
                width=16,
                polynomial=0x8005,
                init_value=0xFFFF,
                final_xor_value=0x0000,
                reverse_input=True,
                reverse_output=True,
            ),
            data=data,
            string_format="{:04X}(hex)",
            endian="little",
        )

    def update_field(self, data: dataT | None = None) -> tuple[int, bytes, bitarray]:
        """Update the field value by calculating it from the appropriate bytes.

        Args:
            data: optional data to calculate the new checksum value from

        Returns:
            the new checksum, the bytes of the checksum, and the bits of the checksum
        """
        byte_data = b""
        if self.parent is not None:
            byte_data = bytes(self.parent)
        crc_int = self.crc_calculator.checksum(byte_data[:-2])
        crc_bytes = int.to_bytes(crc_int, length=2, byteorder=self.endian)
        crc_bits = int2ba(crc_int, length=self._bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)


class ModbusCoilArray(ParseArrayField[bool]):
    """Modbus coil array field."""

    def __init__(
        self,
        count: int | UIntField,
        data: dataT | None = None,
        default: Sequence[bool] | Sequence[int] | None = None,
    ) -> None:
        """Create modbus coil array field.

        Args:
            count: _description_
            default: default crc value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.CoilArray.value,
            count=count,
            array_item_class=BoolField,
            array_item_default=False,
            data=data,
        )
        if default:
            self.set_value(default)

    def set_value(  # pyright:ignore[reportIncompatibleMethodOverride]
        self, value: Sequence[bool] | Sequence[int]
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if len(value) == 0:
            return
        if isinstance(value[0], bool):
            _value = [True if b else False for b in value]
        else:
            bit_array = bitarray(endian="little")
            for v in value:
                bit_array.frombytes(struct.pack("B", v))
            _value = [True if b else False for b in bit_array]
        keys = list(self._children.keys())
        for i, _bool in enumerate(_value):
            if i < len(self.children):
                self.children[keys[i]].value = _bool
            else:
                f = BoolField(
                    name=f"+{i}",
                    default=_bool,
                )
                self.append(f)

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, int):
            _count = self._count * 8
        else:
            if self._count.value is None:
                _count = 0
            else:
                _count = self._count.value * 8
        for i in range(_count):
            f = self._array_item_class(
                f"+{i}",
                self._array_item_default,
            )
            bit_data = f.parse(data=bit_data)
            self.append(f)
        return bit_data

    @property
    def string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        chunks: list[str] = []
        keys = list(self._children.keys())
        bits_per_chunk = 8
        for i in range(0, len(keys), bits_per_chunk):
            chunk_key = keys[i]
            if (i + bits_per_chunk) < len(keys):
                vals = "".join(["1" if self.children[keys[j]].value else "0" for j in range(i, i + bits_per_chunk)])
            else:
                xtra = "0" * (bits_per_chunk - (len(keys) - i))
                vals = "".join(["1" if self.children[keys[j]].value else "0" for j in range(i, len(keys))]) + xtra
            chunks.append(chunk_key + ":" + vals)
        return f"[{', '.join( chunks)}]"


class ModbusDiscreteInputArray(ParseArrayField[bool]):
    """Modbus discrete input array field."""

    def __init__(
        self,
        count: int | UIntField,
        data: dataT | None = None,
        default: Sequence[bool] | Sequence[int] | None = None,
    ) -> None:
        """Create modbus discrete input array field.

        Args:
            count: _description_
            default: default crc value
            data: bytes to be parsed
        """
        super().__init__(
            name=ModbusFieldNamesEnum.DiscreteInputArray.value,
            count=count,
            array_item_class=BoolField,
            array_item_default=False,
            data=data,
        )
        if default:
            self.set_value(default)

    def set_value(  # pyright:ignore[reportIncompatibleMethodOverride]
        self, value: Sequence[bool] | Sequence[int]
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if len(value) == 0:
            return
        if isinstance(value[0], bool):
            _value = [True if b else False for b in value]
        else:
            bit_array = bitarray(endian="little")
            for v in value:
                bit_array.frombytes(struct.pack("B", v))
            _value = [True if b else False for b in bit_array]
        keys = list(self._children.keys())
        for i, _bool in enumerate(_value):
            if i < len(self.children):
                self.children[keys[i]].value = _bool
            else:
                f = BoolField(
                    name=f"+{i}",
                    default=_bool,
                )
                self.append(f)

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, int):
            _count = self._count * 8
        else:
            if self._count.value is None:
                _count = 0
            else:
                _count = self._count.value * 8
        for i in range(_count):
            f = self._array_item_class(
                f"+{i}",
                self._array_item_default,
            )
            bit_data = f.parse(data=bit_data)
            self.append(f)
        return bit_data

    @property
    def string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        chunks: list[str] = []
        keys = list(self._children.keys())
        bits_per_chunk = 8
        for i in range(0, len(keys), bits_per_chunk):
            chunk_key = keys[i]
            if (i + bits_per_chunk) < len(keys):
                vals = "".join(["1" if self.children[keys[j]].value else "0" for j in range(i, i + bits_per_chunk)])
            else:
                xtra = "0" * (bits_per_chunk - (len(keys) - i))
                vals = "".join(["1" if self.children[keys[j]].value else "0" for j in range(i, len(keys))]) + xtra
            chunks.append(chunk_key + ":" + vals)
        return f"[{', '.join( chunks)}]"
