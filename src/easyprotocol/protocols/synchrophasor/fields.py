"""Synchrophasor field classes.
"""
from __future__ import annotations

import struct
from enum import IntEnum
from typing import Sequence, cast

import crc
from bitarray import bitarray
from bitarray.util import int2ba

from easyprotocol.base import dataT, input_to_bytes
from easyprotocol.base.parse_base import T
from easyprotocol.base.parse_field_dict import ParseFieldDict
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.fields import (
    ArrayField,
    BoolField,
    ChecksumField,
    Float32Field,
    StringField,
    UInt8EnumField,
    UInt8Field,
    UInt16Field,
    UIntField,
)
from easyprotocol.fields.enum import EnumField
from easyprotocol.fields.unsigned_int import UInt32Field, UIntFieldGeneric
from easyprotocol.protocols.modbus.constants import (
    ModbusFieldNamesEnum,
    ModbusFunctionEnum,
)


class START(UInt8Field):
    def __init__(
        self,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name="START",
            default=0xAA,
            data=data,
        )


class FrameTypeEnum(IntEnum):
    DATA = 0
    CONFIGURATION1 = 2
    CONFIGURATION2 = 3
    COMMAND = 4


class FRAMETYPE(EnumField[FrameTypeEnum]):
    def __init__(
        self,
        default: FrameTypeEnum,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name="FRAMETYPE",
            enum_type=FrameTypeEnum,
            default=default,
            data=data,
            bit_count=3,
        )


class SYNC(ParseFieldDict):
    def __init__(
        self,
        frame_type: FrameTypeEnum = FrameTypeEnum.DATA,
        data: dataT = None,
    ) -> None:
        super().__init__(
            name="SYNC",
            data=data,
            default=[
                START(),
                UIntField(name="VERSION", bit_count=4),
                FRAMETYPE(default=frame_type),
                BoolField(name="BIT"),
            ],
        )


class CHK(ChecksumField):
    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:

        super().__init__(
            name="CHK",
            default=default,
            data=data,
            bit_count=16,
            crc_configuration=crc.Crc16.CCITT.value,
        )


class NumberFormatEnum(IntEnum):
    INT = 0
    FLOAT = 1


class CoordinateFormatEnum(IntEnum):
    RECTANGULAR = 0
    POLAR = 1


class FORMAT(ParseFieldDict):
    def __init__(
        self,
        data: dataT = None,
    ) -> None:
        super().__init__(
            name="FORMAT",
            default=[
                UIntField(
                    name="EXTRA1",
                    bit_count=8,
                ),
                EnumField(
                    name="COORDINATEFORMAT",
                    bit_count=1,
                    enum_type=CoordinateFormatEnum,
                    default=CoordinateFormatEnum.POLAR,
                ),
                EnumField(
                    name="PHASORFORMAT",
                    bit_count=1,
                    enum_type=NumberFormatEnum,
                    default=NumberFormatEnum.FLOAT,
                ),
                EnumField(
                    name="ANALOGFORMAT",
                    bit_count=1,
                    enum_type=NumberFormatEnum,
                    default=NumberFormatEnum.FLOAT,
                ),
                EnumField(
                    name="FREQFORMAT",
                    bit_count=1,
                    enum_type=NumberFormatEnum,
                    default=NumberFormatEnum.FLOAT,
                ),
                UIntField(
                    name="EXTRA2",
                    bit_count=4,
                ),
            ],
            data=data,
        )

    def frequencies(self) -> NumberFormatEnum:
        return cast(NumberFormatEnum, self["FREQFORMAT"].value)

    def analogs(self) -> NumberFormatEnum:
        return cast(NumberFormatEnum, self["ANALOGFORMAT"].value)

    def phasors(self) -> NumberFormatEnum:
        return cast(NumberFormatEnum, self["PHASORFORMAT"].value)

    def coordinates(self) -> CoordinateFormatEnum:
        return cast(CoordinateFormatEnum, self["COORDINATEFORMAT"].value)


class StringFixedLengthField(StringField):
    def __init__(
        self,
        name: str,
        count: int,
        default_char: str = " ",
        default: str = "",
        data: dataT | None = None,
    ) -> None:
        if len(default) < count:
            default += default_char * (count - len(default))
        if len(default) > count:
            default = default[:count]
        super().__init__(
            name=name,
            count=count,
            default=default,
            data=data,
        )


class STN(StringFixedLengthField):
    def __init__(
        self,
        default: str = "",
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name="STN",
            count=16,
            default=default,
            data=data,
        )


class CHNAM(StringFixedLengthField):
    def __init__(
        self,
        name: str = "CHNAM",
        default: str = "",
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=name,
            default=default,
            data=data,
            count=16,
        )


class CHNAMS(ArrayField[CHNAM]):
    def __init__(
        self,
        phasor_count: UIntFieldGeneric[int],
        analog_count: UIntFieldGeneric[int],
        digital_count: UIntFieldGeneric[int],
        data: dataT | None = None,
    ) -> None:
        self.phasor_count = phasor_count
        self.analog_count = analog_count
        self.digital_count = digital_count
        super().__init__(
            name="CHNAMS",
            count=0,
            array_item_class=CHNAM,
            array_item_default=CHNAM(),
            data=data,
        )

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
        count = self.phasor_count.value + self.analog_count.value + (16 * self.digital_count.value)
        if count is not None:
            for i in range(count):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=self._array_item_default,
                )
                bit_data = f.parse(data=bit_data)
                self._children[f.name] = f
        return bit_data

    def create_default(self, default: Sequence[T] | Sequence[ParseGenericValue[T]]) -> None:
        """Create an array of default valued sub-fields for this array field.

        Args:
            default: default values for the sub-fields
        """
        for i, item in enumerate(default):
            if isinstance(item, ParseGenericValue):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(ParseGenericValue[T], item).value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(T, item),
                )
            self._children[f.name] = f


class PHASOR_POLAR_FLOAT(ParseFieldDict):
    def __init__(
        self,
        name: str = "PHASOR",
        default: None = None,
        data: dataT = None,
    ) -> None:
        super().__init__(
            name=name,
            default=[
                Float32Field(name="MAGNITUDE"),
                Float32Field(name="ANGLE"),
            ],
            data=data,
        )


class PHASOR_POLAR_INT(ParseFieldDict):
    def __init__(
        self,
        name: str = "PHASOR",
        default: None = None,
        data: dataT = None,
    ) -> None:
        super().__init__(
            name=name,
            default=[
                UInt16Field(name="MAGNITUDE"),
                UInt16Field(name="ANGLE"),
            ],
            data=data,
        )


class PHASOR_RECTANGULAR_FLOAT(ParseFieldDict):
    def __init__(
        self,
        name: str = "PHASOR",
        default: None = None,
        data: dataT = None,
    ) -> None:
        super().__init__(
            name=name,
            default=[
                Float32Field(name="REAL"),
                Float32Field(name="IMAGINARY"),
            ],
            data=data,
        )


class PHASOR_RECTANGULAR_INT(ParseFieldDict):
    def __init__(
        self,
        name: str = "PHASOR",
        default: None = None,
        data: dataT = None,
    ) -> None:
        super().__init__(
            name=name,
            default=[
                UInt16Field(name="REAL"),
                UInt16Field(name="IMAGINARY"),
            ],
            data=data,
        )
