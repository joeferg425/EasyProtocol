from __future__ import annotations

import math
from collections import OrderedDict
from typing import Any

import crc
from bitarray import bitarray
from bitarray.util import int2ba

from easyprotocol.base import I, ParseObject, input_to_bytes
from easyprotocol.fields import (
    ArrayFieldGeneric,
    BoolField,
    ChecksumField,
    UInt8EnumField,
    UInt8Field,
    UInt16Field,
    UIntField,
)
from easyprotocol.protocols.modbus.constants import ModbusFieldNames, ModbusFunctionEnum


class ModbusDeviceId(UInt8Field):
    def __init__(
        self,
        data: I | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNames.DeviceID,
            data=data,
            value=value,
            endian="big",
        )


class ModbusFunction(UInt8EnumField):
    def __init__(
        self,
        data: I | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNames.FunctionCode,
            enum_type=ModbusFunctionEnum,
            data=data,
            value=value,
            endian="little",
        )


class ModbusAddress(UInt16Field):
    def __init__(
        self,
        data: I | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNames.Address,
            data=data,
            value=value,
            endian="little",
        )


class ModbusCount(UInt16Field):
    def __init__(
        self,
        data: I | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNames.Count,
            data=data,
            value=value,
            endian="little",
            format="{}",
        )


class ModbusByteCount(UInt8Field):
    def __init__(
        self,
        data: I | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNames.ByteCount,
            data=data,
            value=value,
            endian="big",
            format="{}",
        )


class ModbusCRC(ChecksumField):
    def __init__(
        self,
        data: I | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNames.CRC,
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

    def update_field(self, data: I | None = None) -> tuple[int, bytes, bitarray]:
        byte_data = bytes(self.parent)
        crc_int = self.crc_calculator.calculate_checksum(byte_data[:-2])
        crc_bytes = int.to_bytes(crc_int, length=2, byteorder=self.endian)
        crc_bits = int2ba(crc_int, length=self._bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)


class ModbusCoilArray(ArrayFieldGeneric):
    def __init__(
        self,
        count_field: UIntField,
        data: I | None = None,
        parent: ParseObject[Any] | None = None,
        children: list[ParseObject[bool]] | OrderedDict[str, ParseObject[bool]] | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNames.CoilArray,
            count=count_field,
            array_item_class=BoolField,
            data=data,
            parent=parent,
            children=children,
        )

    def parse(self, data: I) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        count = self._count.value * 8
        for i in range(count):
            f = self.array_item_class(f"+{i}")
            bit_data = f.parse(data=bit_data)
            self.append(f)
        return bit_data

    @property
    def formatted_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        chunks = {}
        keys = list(self._children.keys())
        bits_per_chunk = 8
        for i in range(0, len(keys), bits_per_chunk):
            chunk_key = keys[i]
            vals = "".join(["1" if self._children[keys[j]].value else "0" for j in range(i, i + bits_per_chunk)])
            chunks[chunk_key] = vals
        return f"[{', '.join([key+':'+value for key, value in chunks.items()])}]"

    @property
    def value(self) -> list[bool]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return list([v.value for f, v in self._children.items()])

    @value.setter
    def value(self, value: list[ParseObject[Any]] | list[bool] | list[int]) -> None:
        if not isinstance(value, list):
            raise TypeError(f"{self.__class__.__name__} cannot be assigned value {value} of type {type(value)}")
        temp = UInt8Field(name="temp", endian="little")
        for index, item in enumerate(value):
            if isinstance(item, ParseObject):
                if index < len(self._children):
                    self[index] = item
                    item.parent = self
                else:
                    self.append(item)
                    item.parent = self
            elif isinstance(item, int):
                temp.value = item
                bits = temp.bits
                bits.reverse()
                for i in range(len(bits)):
                    parse_object = self[index * 8 + i]
                    parse_object.value = True if bits[i] else False
            else:
                parse_object = self[index]
                parse_object.value = item
