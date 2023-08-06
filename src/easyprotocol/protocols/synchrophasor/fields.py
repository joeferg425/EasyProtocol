"""Synchrophasor field classes."""
from __future__ import annotations

import math
from enum import Enum, IntEnum, IntFlag
from typing import Any, Union, cast

from bitarray import bitarray
from bitarray.util import int2ba
from crc import Configuration

from easyprotocol.base import DEFAULT_ENDIANNESS, BaseField, dataT, input_to_bitarray
from easyprotocol.base.dict import DictField
from easyprotocol.fields import (
    ArrayFieldGeneric,
    BoolField,
    ChecksumField,
    FlagsField,
    Float32Field,
    StringField,
    UInt8Field,
    UInt16Field,
    UIntField,
)
from easyprotocol.fields.enum import EnumField
from easyprotocol.fields.unsigned_int import UIntFieldGeneric


class FrameTypeEnum(IntEnum):
    """Frame type enumeration."""

    Frame = -1
    Data = 0
    Configuration1 = 2
    Configuration2 = 3
    Command = 4


class FrameTypeNameEnum(str, Enum):
    """Frame type enumeration."""

    Frame = FrameTypeEnum.Frame.name
    Data = FrameTypeEnum.Data.name
    Configuration1 = FrameTypeEnum.Configuration1.name
    Configuration2 = FrameTypeEnum.Configuration2.name
    Command = FrameTypeEnum.Command.name


class FieldNameEnum(str, Enum):
    """Enumerated field names."""

    Sync = "Sync"
    Start = "Start"
    Version = "Version"
    FrameType = "FrameType"
    SyncBit = "SyncBit"
    PMUConfiguration = "PMUConfiguration"
    PMUConfigurations = "PMUConfigurations"
    PMUCount = "PMUCount"
    PhasorCount = "PhasorCount"
    AnalogCount = "AnalogCount"
    DigitalCount = "DigitalCount"
    StationName = "StationName"
    IDCode = "IDCode"
    Format = "Format"
    FormatExtra1 = "FormatExtra1"
    FormatExtra2 = "FormatExtra2"
    CoordinateFormat = "CoordinateFormat"
    PhasorFormat = "PhasorFormat"
    AnalogFormat = "AnalogFormat"
    FrequencyFormat = "FrequencyFormat"
    PhasorNames = "PhasorNames"
    AnalogNames = "AnalogNames"
    DigitalNames = "DigitalNames"
    PhasorUnit = "PhasorUnit"
    AnalogUnit = "AnalogUnit"
    DigitalUnit = "DigitalUnit"
    NominalFrequency = "NominalFrequency"
    ConfigurationCount = "ConfigurationCount"
    FrameSize = "FrameSize"
    SecondsOfCentury = "SecondsOfCentury"
    FractionalSeconds = "FractionalSeconds"
    TimeBase = "TimeBase"
    DataRate = "DataRate"
    Checksum = "Checksum"
    Command = "Command"
    PMUData = "PMUData"
    StatusFlags = "StatusFlags"
    PhasorList = "PhasorList"
    AnalogList = "AnalogList"
    DigitalList = "DigitalList"
    Frequency = "Frequency"
    FrequencyDelta = "FrequencyDelta"
    TimeQuality = "TimeQuality"
    TimeQualityFlags = "TimeQualityFlags"
    TimeQualityCode = "TimeQualityCode"
    Resolution = "Resolution"


class FrameType(EnumField[FrameTypeEnum]):
    """Frame Type field."""

    def __init__(
        self,
        default: FrameTypeEnum,
        data: dataT | None = None,
    ) -> None:
        """Parse the frame type field into its enum values.

        Args:
            default: default value of this field
            data: data to be parsed. Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.FrameType.value,
            enum_type=FrameTypeEnum,
            default=default,
            data=data,
            bit_count=3,
        )


class Sync(DictField):
    """SYNC field parser."""

    def __init__(
        self,
        start: int | None = None,
        version: int | None = None,
        frame_type: FrameTypeEnum | None = None,
        sync_bit: bool | None = None,
        data: dataT = None,
    ) -> None:
        """Parse the members of the sync field.

        Args:
            start: start bits. Defaults to AA.
            version: defaults to 1.
            frame_type: frame type enum. Defaults to FrameTypeEnum.DATA.
            sync_bit: defaults to false
            data: data to parse. Defaults to None.
        """
        if start is None:
            start = 0xAA
        if version is None:
            version = 1
        if frame_type is None:
            frame_type = FrameTypeEnum.Data
        if sync_bit is None:
            sync_bit = False
        super().__init__(
            name=FieldNameEnum.Sync.value,
            data=data,
            default=[
                UInt8Field(
                    name=FieldNameEnum.Start.value,
                    default=start,
                ),
                UIntField(
                    name=FieldNameEnum.Version.value,
                    default=version,
                    bit_count=4,
                ),
                FrameType(
                    default=frame_type,
                ),
                BoolField(
                    name=FieldNameEnum.SyncBit.value,
                    default=sync_bit,
                ),
            ],
        )

    @property
    def start(self) -> UInt8Field:
        """Get start value integer.

        Returns:
            start value
        """
        return cast("UInt8Field", self[FieldNameEnum.Start.value])

    @property
    def version(self) -> UIntField:
        """Get version integer.

        Returns:
            version value
        """
        return cast("UIntField", self[FieldNameEnum.Version.value])

    @property
    def frameType(self) -> FrameType:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("FrameType", self[FieldNameEnum.FrameType.value])

    @property
    def syncBit(self) -> BoolField:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("BoolField", self[FieldNameEnum.SyncBit.value])


class TimeQualityFlags(IntFlag):
    """Time quality flags."""

    LeapSecondPending = 0b0001
    LeapSecondOccurred = 0b0010
    LeapSecondAdd = 0b0100
    Reserved = 0b1000


class TimeQualityFlagsField(FlagsField[TimeQualityFlags]):
    """Time quality flags."""

    def __init__(
        self,
        default: TimeQualityFlags | None = None,
        data: dataT = None,
        string_format: str = "{}",
    ) -> None:
        """Time quality flags.

        Args:
            default:  Defaults to None.
            data:  Defaults to None.
            string_format:  Defaults to "{}".
        """
        if default is None:
            default = TimeQualityFlags(0)
        super().__init__(
            name=FieldNameEnum.TimeQualityFlags.value,
            bit_count=4,
            flags_type=TimeQualityFlags,
            default=default,
            data=data,
            string_format=string_format,
            endian=DEFAULT_ENDIANNESS,
        )


class TimeQualityCodeEnum(IntEnum):
    """Time quality codes."""

    ClockLocked = 0
    One = 1
    Two = 2
    Four = 4


class TimeQualityCode(EnumField[TimeQualityCodeEnum]):
    """Time quality codes."""

    def __init__(
        self,
        default: TimeQualityCodeEnum | None = None,
        data: dataT = None,
        string_format: str = "{}",
    ) -> None:
        """Time quality codes.

        Args:
            default: _description_
            data: _description_. Defaults to None.
            string_format: _description_. Defaults to "{}".
        """
        if default is None:
            default = TimeQualityCodeEnum.ClockLocked
        super().__init__(
            name=FieldNameEnum.TimeQualityCode.value,
            bit_count=4,
            enum_type=TimeQualityCodeEnum,
            default=default,
            data=data,
            endian=DEFAULT_ENDIANNESS,
            string_format=string_format,
        )


class TimeQuality(
    DictField,
    BaseField,
):
    """Time Quality fields."""

    def __init__(
        self,
        time_quality_flags: TimeQualityFlags | None = None,
        time_quality_code: TimeQualityCodeEnum | None = None,
        data: dataT | None = None,
    ) -> None:
        """Time quality fields.

        Args:
            time_quality_flags: time quality flags.
            time_quality_code: time quality code.
            data: _description_. Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.TimeQuality.value,
            default=[
                TimeQualityFlagsField(default=time_quality_flags),
                TimeQualityCode(default=time_quality_code),
            ],
            data=data,
            bit_count=-1,
            string_format=None,
            endian=DEFAULT_ENDIANNESS,
        )


class SynchrophasorChecksum(
    ChecksumField,
    BaseField,
):
    """Checksum class."""

    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:
        """Create a checksum field.

        Args:
            default: default value. Defaults to 0.
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.Checksum.value,
            default=default,
            data=data,
            bit_count=16,
            crc_configuration=Configuration(
                width=16,
                polynomial=0x1021,
                init_value=0xFFFF,
                final_xor_value=0x0000,
                reverse_input=False,
                reverse_output=False,
            ),
        )

    def update_field(self, data: dataT | None = None) -> tuple[int, bytes, bitarray]:
        """Update the field value by calculating it from the appropriate bytes.

        Args:
            data: optional data to calculate the new checksum value from

        Returns:
            the new checksum, the bytes of the checksum, and the bits of the checksum
        """
        if data is None:
            if self.parent is not None:
                byte_data = bytes(self.parent)[:-2]
            else:
                byte_data = b""
        else:
            byte_data = input_to_bitarray(data=data, bit_count=self._bit_count).tobytes()
        crc_int = self.crc_calculator.checksum(byte_data)
        byte_length = math.ceil(self._bit_count / 8)
        crc_bytes = int.to_bytes(crc_int, length=byte_length, byteorder="little")
        crc_int = int.from_bytes(crc_bytes, byteorder="little", signed=False)
        crc_bits = int2ba(crc_int, length=self._bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)


class NumberFormatEnum(IntEnum):
    """Number format enumeration."""

    INT = 0
    FLOAT = 1


class CoordinateFormatEnum(IntEnum):
    """Coordinate format enumeration."""

    POLAR = 0
    RECTANGULAR = 1


class CoordinateFormat(EnumField[CoordinateFormatEnum]):
    """Coordinate format field."""

    def __init__(
        self,
        default: CoordinateFormatEnum = CoordinateFormatEnum.POLAR,
        data: dataT = None,
    ) -> None:
        """Create coordinate format field.

        Args:
            default: Defaults to CoordinateFormatEnum.POLAR.
            data: Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.CoordinateFormat.value,
            bit_count=1,
            enum_type=CoordinateFormatEnum,
            default=default,
            data=data,
            endian=DEFAULT_ENDIANNESS,
            string_format="{}",
        )


class PhasorFormat(EnumField[NumberFormatEnum]):
    """Phasor format field."""

    def __init__(
        self,
        default: NumberFormatEnum = NumberFormatEnum.FLOAT,
        data: dataT = None,
    ) -> None:
        """Create phasor format field.

        Args:
            default: Defaults to CoordinateFormatEnum.POLAR.
            data: Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.PhasorFormat.value,
            bit_count=1,
            enum_type=NumberFormatEnum,
            default=default,
            data=data,
            endian=DEFAULT_ENDIANNESS,
            string_format="{}",
        )


class AnalogFormat(EnumField[NumberFormatEnum]):
    """Analog format field."""

    def __init__(
        self,
        default: NumberFormatEnum = NumberFormatEnum.FLOAT,
        data: dataT = None,
    ) -> None:
        """Create analog format field.

        Args:
            default: Defaults to CoordinateFormatEnum.POLAR.
            data: Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.AnalogFormat.value,
            bit_count=1,
            enum_type=NumberFormatEnum,
            default=default,
            data=data,
            endian=DEFAULT_ENDIANNESS,
            string_format="{}",
        )


class FrequencyFormat(EnumField[NumberFormatEnum]):
    """Frequency format field."""

    def __init__(
        self,
        default: NumberFormatEnum = NumberFormatEnum.FLOAT,
        data: dataT = None,
    ) -> None:
        """Create frequency format field.

        Args:
            default: Defaults to CoordinateFormatEnum.POLAR.
            data: Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.FrequencyFormat.value,
            bit_count=1,
            enum_type=NumberFormatEnum,
            default=default,
            data=data,
            endian=DEFAULT_ENDIANNESS,
            string_format="{}",
        )


class Format(DictField):
    """Number and coordinate format field."""

    def __init__(
        self,
        data: dataT = None,
    ) -> None:
        """Create number and coordinate format field.

        Args:
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.Format.value,
            default=[
                UIntField(
                    name=FieldNameEnum.FormatExtra1.value,
                    bit_count=8,
                ),
                CoordinateFormat(),
                PhasorFormat(),
                AnalogFormat(),
                FrequencyFormat(),
                UIntField(
                    name=FieldNameEnum.FormatExtra2.value,
                    bit_count=4,
                ),
            ],
            data=data,
        )

    @property
    def frequencies(self) -> FrequencyFormat:
        """Get frequency format.

        Returns:
            frequency format
        """
        return cast("FrequencyFormat", self[FieldNameEnum.FrequencyFormat.value])

    @frequencies.setter
    def frequencies(self, value: FrequencyFormat | NumberFormatEnum) -> None:
        if isinstance(value, FrequencyFormat):
            self.frequencies = value
        else:
            self.frequencies.value = value

    @property
    def analogs(self) -> AnalogFormat:
        """Get analog format.

        Returns:
            analog format
        """
        return cast("AnalogFormat", self[FieldNameEnum.AnalogFormat.value])

    @analogs.setter
    def analogs(self, value: AnalogFormat | NumberFormatEnum) -> None:
        if isinstance(value, AnalogFormat):
            self.analogs = value
        else:
            self.analogs.value = value

    @property
    def phasors(self) -> PhasorFormat:
        """Get phasor format.

        Returns:
            phasor format
        """
        return cast(PhasorFormat, self[FieldNameEnum.PhasorFormat.value])

    @phasors.setter
    def phasors(self, value: PhasorFormat | NumberFormatEnum) -> None:
        if isinstance(value, PhasorFormat):
            self.phasors = value
        else:
            self.phasors.value = value

    @property
    def coordinates(self) -> CoordinateFormat:
        """Get coordinate format.

        Returns:
            coordinate format
        """
        return cast("CoordinateFormat", self[FieldNameEnum.CoordinateFormat.value])

    @coordinates.setter
    def coordinates(self, value: CoordinateFormatEnum | CoordinateFormat) -> None:
        if isinstance(value, CoordinateFormat):
            self.coordinates = value
        else:
            self.coordinates.value = value


class SynchrophasorString(StringField):
    """Fixed length 16-byte string field."""

    def __init__(
        self,
        name: str,
        default: str = "",
        data: dataT | None = None,
    ) -> None:
        """Create fixed length 16-byte string field.

        Args:
            name: name of field
            default: default field value. Defaults to "".
            data: data to parse. Defaults to None.
        """
        length = 16
        if len(default) < length:
            default += " " * (length - len(default))
        if len(default) > length:
            default = default[:length]
        super().__init__(
            name=name,
            byte_count=length,
            default=default,
            data=data,
        )

    def get_value(self) -> str:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        _bits = self.bits_lsb
        m = len(_bits) % 8
        if m != 0:
            bits = _bits + bitarray([False] * (8 - m))
        else:
            bits = _bits
        b = bits.tobytes()
        return b.decode(self._string_encoding).strip()

    def set_value(self, value: str) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        if len(value) < 16:
            value = value.ljust(16)
        my_bytes = value.encode()
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]


class SynchrophasorStringArray(
    ArrayFieldGeneric[str],
    BaseField,
):
    """Array of digital names."""

    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int],
        fixed_string_length: int = 16,
        data: dataT | None = None,
    ) -> None:
        """Create array of digital names.

        Args:
            name: name of the field
            count: count of digital words (name count is word count * 16)
            data: data to parse. Defaults to None.
            fixed_string_length: the length of each parsed string
        """
        self._fixed_string_length = fixed_string_length
        super().__init__(
            name=name,
            count=count,
            array_item_class=SynchrophasorString,
            array_item_default="",
            data=data,
        )

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bitarray(data=data)
        if isinstance(self._count, int):
            count = self._count
        else:
            count = self._count.value
        for i in range(count):
            f = self._array_item_class(
                name=f"#{i}",
                default=self._array_item_default,
            )
            bit_data = f.parse(data=bit_data)
            self._children[f.name] = f
        return bit_data


class Phasor:
    """Base phasor class."""

    @property
    def magnitude(self) -> float:
        """Get magnitude value.

        Raises:
            NotImplementedError: until implemented
        """
        raise NotImplementedError()

    @property
    def angle(self) -> float:
        """Get angle value in radians.

        Raises:
            NotImplementedError: until implemented
        """
        raise NotImplementedError()

    @property
    def imaginary(self) -> float:
        """Get imaginary value.

        Raises:
            NotImplementedError: until implemented
        """
        raise NotImplementedError()

    @property
    def real(self) -> float:
        """Get real value.

        Raises:
            NotImplementedError: until implemented
        """
        raise NotImplementedError()

    @property
    def degrees(self) -> float:
        """Get angle value in degrees.

        Raises:
            NotImplementedError: until implemented
        """
        raise NotImplementedError()

    def get_summary(
        self,
        coords: CoordinateFormatEnum | None = CoordinateFormatEnum.POLAR,
        names: bool = False,
    ) -> str:
        """Get phasor summary.

        Args:
            coords: choose coordinate type for summary. Defaults to CoordinateFormatEnum.POLAR.
            names: include names (real, magnitude, etc.). Defaults to False.

        Returns:
            a summary string
        """
        s = ""
        if coords is CoordinateFormatEnum.POLAR or coords is None:
            if names:
                s += f"MAGNITUDE: {self.magnitude:.3f}, DEGREES: {self.degrees:.3f}"
            else:
                s += f"{self.magnitude:.3f}, {self.degrees:.3f}"
        if coords is CoordinateFormatEnum.RECTANGULAR or coords is None:
            if names:
                s += f"IMAGINARY: {self.imaginary:.3f}j, REAL: {self.real:.3f}"
            else:
                s += f"{self.imaginary:.3f}j, {self.real:.3f}"
        return s

    @property
    def summary(self) -> str:
        """Get default phasor summary.

        Returns:
            default phasor summary
        """
        return self.get_summary()


class PhasorPolarFloat(DictField, Phasor):
    """Phasor field with polar and floating point values."""

    def __init__(
        self,
        name: str = "PHASOR",
        default: None = None,
        data: dataT = None,
    ) -> None:
        """Create phasor field with polar and floating point values.

        Args:
            name: name of field. Defaults to "PHASOR".
            default: default value. Defaults to None.
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=name,
            default=[
                Float32Field(name="MAGNITUDE"),
                Float32Field(name="ANGLE"),
            ],
            data=data,
        )

    def get_value_as_string(self) -> str:
        """Override the default string value of field with phasor summary.

        Returns:
            phasor summary
        """
        return self.summary

    @property
    def magnitude(self) -> float:
        """Get magnitude value.

        Returns:
            magnitude value
        """
        return cast("Float32Field", self["MAGNITUDE"]).value

    @property
    def angle(self) -> float:
        """Get angle value in radians.

        Returns:
            angle value in radians
        """
        return cast("Float32Field", self["ANGLE"]).value

    @property
    def imaginary(self) -> float:
        """Get imaginary value.

        Returns:
            imaginary value
        """
        return self.magnitude * math.cos(self.angle)

    @property
    def real(self) -> float:
        """Get real value.

        Returns:
            real value
        """
        return self.magnitude * math.sin(self.angle)

    @property
    def degrees(self) -> float:
        """Get angle value in degrees.

        Returns:
            angle value in degrees
        """
        return math.degrees(self.angle)


class PhasorPolarInt(DictField, Phasor):
    """Phasor field with polar and integer values."""

    def __init__(
        self,
        name: str = "PHASOR",
        default: None = None,
        data: dataT = None,
    ) -> None:
        """Create phasor field with polar and integer values.

        Args:
            name: name of field. Defaults to "PHASOR".
            default: default value. Defaults to None.
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=name,
            default=[
                UInt16Field(name="MAGNITUDE"),
                UInt16Field(name="ANGLE"),
            ],
            data=data,
        )

    def get_value_as_string(self) -> str:
        """Override the default string value of field with phasor summary.

        Returns:
            phasor summary
        """
        return self.summary


class PhasorRectangularFloat(DictField, Phasor):
    """Phasor field with rectangular and floating-point values."""

    def __init__(
        self,
        name: str = "PHASOR",
        default: None = None,
        data: dataT = None,
    ) -> None:
        """Create phasor field with rectangular and floating-point values.

        Args:
            name: name of field. Defaults to "PHASOR".
            default: default value. Defaults to None.
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=name,
            default=[
                Float32Field(name="REAL"),
                Float32Field(name="IMAGINARY"),
            ],
            data=data,
        )

    def get_value_as_string(self) -> str:
        """Override the default string value of field with phasor summary.

        Returns:
            phasor summary
        """
        return self.summary

    @property
    def real(self) -> float:
        """Get real value.

        Returns:
            real value
        """
        return cast("Float32Field", self["REAL"]).value

    @property
    def imaginary(self) -> float:
        """Get imaginary value.

        Returns:
            imaginary value
        """
        return cast("Float32Field", self["IMAGINARY"]).value

    @property
    def magnitude(self) -> float:
        """Get magnitude value.

        Returns:
            magnitude value
        """
        return math.sqrt(self.real**2 + self.imaginary**2)

    @property
    def angle(self) -> float:
        """Get angle value in radians.

        Returns:
            angle value in radians
        """
        return math.atan2(self.imaginary, self.real)

    @property
    def degrees(self) -> float:
        """Get angle value in degrees.

        Returns:
            angle value in degrees
        """
        return math.degrees(self.angle)


class PhasorRectangularInt(DictField, Phasor):
    """Phasor field with rectangular and integer values."""

    def __init__(
        self,
        name: str = "PHASOR",
        default: None = None,
        data: dataT = None,
    ) -> None:
        """Create phasor field with rectangular and integer values.

        Args:
            name: name of field. Defaults to "PHASOR".
            default: default value. Defaults to None.
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=name,
            default=[
                UInt16Field(name="REAL"),
                UInt16Field(name="IMAGINARY"),
            ],
            data=data,
        )

    def get_value_as_string(self) -> str:
        """Override the default string value of field with phasor summary.

        Returns:
            phasor summary
        """
        return self.summary


class CommandEnum(IntEnum):
    """Synchrophasor command enumeration."""

    DataTransmissionOff = 1
    DataTransmissionOn = 2
    SendConfiguration2 = 5


class Command(EnumField[CommandEnum]):
    """Synchrophasor command enumeration."""

    def __init__(
        self,
        default: CommandEnum | None = None,
        data: dataT = None,
    ) -> None:
        """Synchrophasor command enumeration.

        Args:
            default:  Defaults to None.
            data:  Defaults to None.
        """
        if default is None:
            default = CommandEnum.SendConfiguration2
        super().__init__(
            name=FieldNameEnum.Command.value,
            bit_count=16,
            enum_type=CommandEnum,
            default=default,
            data=data,
            endian=DEFAULT_ENDIANNESS,
            string_format="{}",
        )


class PhasorUnits(ArrayFieldGeneric[float]):
    """Phasor Units."""

    def __init__(
        self,
        count: UIntFieldGeneric[int] | int,
        data: dataT = None,
    ) -> None:
        """Create phasor Units.

        Args:
            count: number of items in array
            data: Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.PhasorUnit.value,
            count=count,
            array_item_class=Float32Field,
            array_item_default=0.0,
            default=None,
            data=data,
        )


class AnalogUnits(ArrayFieldGeneric[float]):
    """Analog Units."""

    def __init__(
        self,
        count: UIntFieldGeneric[int] | int,
        data: dataT = None,
    ) -> None:
        """Create analog Units.

        Args:
            count: number of items in array
            data: Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.AnalogUnit.value,
            count=count,
            array_item_class=Float32Field,
            array_item_default=0.0,
            default=None,
            data=data,
        )


class DigitalUnits(ArrayFieldGeneric[float]):
    """Digital Units."""

    def __init__(
        self,
        count: UIntFieldGeneric[int] | int,
        data: dataT = None,
    ) -> None:
        """Create digital Units.

        Args:
            count: number of items in array
            data: Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.DigitalUnit.value,
            count=count,
            array_item_class=Float32Field,
            array_item_default=0.0,
            default=None,
            data=data,
        )


class NominalFrequencyEnum(IntEnum):
    """Nominal frequency enum."""

    SixtyHertz = 0
    FiftyHertz = 1


class NominalFrequency(EnumField[NominalFrequencyEnum]):
    """Nominal frequency."""

    def __init__(
        self,
        data: dataT = None,
    ) -> None:
        """Create nominal frequency.

        Args:
            data: Defaults to None.
        """
        super().__init__(
            name=FieldNameEnum.NominalFrequency.value,
            bit_count=16,
            enum_type=NominalFrequencyEnum,
            default=NominalFrequencyEnum.SixtyHertz,
            data=data,
        )


class SynchrophasorConfiguration(DictField):
    """PMU configuration object."""

    def __init__(
        self,
        name: str = FieldNameEnum.PMUConfiguration.value,
        phasor_count: int = 0,
        analog_count: int = 0,
        digital_count: int = 0,
        default: Any = None,
        data: dataT = None,
    ) -> None:
        """Create PMU configuration object.

        Args:
            name: name of field. Defaults to "PMU_CONFIGURATION".
            phasor_count: number of phasors
            analog_count: number of analogs
            digital_count: number of digitals
            default: required, but unused
            data: data to parse. Defaults to None.
        """
        self._ph_nmr = UInt16Field(
            name=FieldNameEnum.PhasorCount.value,
            default=phasor_count,
        )
        self._an_nmr = UInt16Field(
            name=FieldNameEnum.AnalogCount.value,
            default=analog_count,
        )
        self._dg_nmr = UInt16Field(
            name=FieldNameEnum.DigitalCount.value,
            default=digital_count,
        )
        super().__init__(
            name=name,
            data=data,
            default=[
                SynchrophasorString(name=FieldNameEnum.StationName.value),
                UInt16Field(name=FieldNameEnum.IDCode.value),
                Format(),
                self._ph_nmr,
                self._an_nmr,
                self._dg_nmr,
                SynchrophasorStringArray(
                    name=FieldNameEnum.PhasorNames.value,
                    count=self._ph_nmr,
                ),
                SynchrophasorStringArray(
                    name=FieldNameEnum.AnalogNames.value,
                    count=self._an_nmr,
                ),
                SynchrophasorStringArray(
                    name=FieldNameEnum.DigitalNames.value,
                    count=self._dg_nmr,
                ),
                PhasorUnits(
                    count=self._ph_nmr,
                ),
                AnalogUnits(
                    count=self._an_nmr,
                ),
                DigitalUnits(
                    count=self._dg_nmr,
                ),
                NominalFrequency(),
                UInt16Field(name=FieldNameEnum.ConfigurationCount.value),
            ],
        )

    @property
    def stationName(self) -> SynchrophasorString:
        """Get the station name.

        Returns:
            the station name
        """
        return cast("SynchrophasorString", self[FieldNameEnum.StationName.value])

    @stationName.setter
    def stationName(self, value: str | SynchrophasorString) -> None:
        if isinstance(value, SynchrophasorString):
            self.stationName = value
        else:
            self.stationName.value = value

    @property
    def phasorCount(self) -> UInt16Field:
        """Get the station name.

        Returns:
            the station name
        """
        return cast("UInt16Field", self[FieldNameEnum.PhasorCount.value])

    @phasorCount.setter
    def phasorCount(self, value: int | UInt16Field) -> None:
        if isinstance(value, UInt16Field):
            self.phasorCount = value
        else:
            self.phasorCount.value = value

    @property
    def analogCount(self) -> UInt16Field:
        """Get the station name.

        Returns:
            the station name
        """
        return cast("UInt16Field", self[FieldNameEnum.AnalogCount.value])

    @analogCount.setter
    def analogCount(self, value: int | UInt16Field) -> None:
        if isinstance(value, UInt16Field):
            self.analogCount = value
        else:
            self.analogCount.value = value

    @property
    def digitalCount(self) -> UInt16Field:
        """Get the station name.

        Returns:
            the station name
        """
        return cast("UInt16Field", self[FieldNameEnum.DigitalCount.value])

    @digitalCount.setter
    def digitalCount(self, value: int | UInt16Field) -> None:
        if isinstance(value, UInt16Field):
            self.digitalCount = value
        else:
            self.digitalCount.value = value

    @property
    def idCode(self) -> UInt16Field:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("UInt16Field", self[FieldNameEnum.IDCode.value])

    @idCode.setter
    def idCode(self, value: UInt16Field | int) -> None:
        if isinstance(value, UInt16Field):
            self.idCode.value = value.value
        else:
            self.idCode.value = value

    @property
    def formats(self) -> Format:
        """Get the phasor names.

        Returns:
            the phasor names
        """
        return cast("Format", self[FieldNameEnum.Format.value])

    @property
    def phasorNames(self) -> list[str]:
        """Get the phasor names.

        Returns:
            the phasor names
        """
        name_list = cast(
            "list[SynchrophasorString]",
            cast("SynchrophasorStringArray", self[FieldNameEnum.PhasorNames.value]).value,
        )
        return [v.value_as_string for v in name_list]

    @property
    def analogNames(self) -> list[str]:
        """Get the analog names.

        Returns:
            the analog names
        """
        name_list = cast(
            "list[SynchrophasorString]",
            cast("SynchrophasorStringArray", self[FieldNameEnum.AnalogNames.value]).value_list,
        )
        return [v.value_as_string for v in name_list]

    @property
    def digitalNames(self) -> list[str]:
        """Get the digital names.

        Returns:
            the digital names
        """
        name_list = cast(
            "list[SynchrophasorString]",
            cast("SynchrophasorStringArray", self[FieldNameEnum.DigitalNames.value]).value_list,
        )
        return [v.value_as_string for v in name_list]

    @property
    def phasorUnits(self) -> list[float]:
        """Get the station name.

        Returns:
            the station name
        """
        units = cast("PhasorUnits", self[FieldNameEnum.PhasorUnit.value])
        return [u.value for u in units]

    @property
    def analogUnits(self) -> list[float]:
        """Get the station name.

        Returns:
            the station name
        """
        units = cast("AnalogUnits", self[FieldNameEnum.AnalogUnit.value])
        return [u.value for u in units]

    @property
    def digitalUnits(self) -> list[float]:
        """Get the station name.

        Returns:
            the station name
        """
        units = cast("AnalogUnits", self[FieldNameEnum.DigitalUnit.value])
        return [u.value for u in units]

    @property
    def nominalFrequency(self) -> NominalFrequency:
        """Get the station name.

        Returns:
            the station name
        """
        return cast("NominalFrequency", self[FieldNameEnum.NominalFrequency.value])

    @nominalFrequency.setter
    def nominalFrequency(self, value: NominalFrequency | NominalFrequencyEnum) -> None:
        if isinstance(value, NominalFrequency):
            self.nominalFrequency = value
        else:
            self.nominalFrequency.value = value

    @property
    def configurationCount(self) -> UInt16Field:
        """Get the station name.

        Returns:
            the station name
        """
        return cast("UInt16Field", self[FieldNameEnum.ConfigurationCount.value])

    @configurationCount.setter
    def configurationCount(self, value: int | UInt16Field) -> None:
        if isinstance(value, UInt16Field):
            self.configurationCount = value
        else:
            self.configurationCount.value = value


class PMUData(DictField):
    """Data field of a Data frame."""

    def __init__(
        self,
        phasor_count: int,
        analog_count: int,
        digital_count: int,
        pmu_format: Format,
        name: str = FieldNameEnum.PMUData.value,
        default: None = None,
        data: dataT = None,
    ) -> None:
        """Create Data field of a Data frame.

        Args:
            phasor_count: number of phasors in pmu
            analog_count: number of analog values in pmu
            digital_count: number of digital words in pmu
            pmu_format: pmu format from configuration frame
            name: name of frame. Defaults to "PMU_DATA".
            default: default value (not used). Defaults to None.
            data: data to parse. Defaults to None.
        """
        self._format = pmu_format
        if self._format.phasors is NumberFormatEnum.FLOAT:
            if self._format.coordinates is CoordinateFormatEnum.POLAR:
                self._phasor_class = type(PhasorRectangularFloat)
            else:
                self._phasor_class = type(PhasorPolarFloat)
        else:
            if self._format.coordinates is CoordinateFormatEnum.POLAR:
                self._phasor_class = type(PhasorRectangularInt)
            else:
                self._phasor_class = type(PhasorPolarInt)
        if self._format.frequencies is NumberFormatEnum.FLOAT:
            self._freq_class = Float32Field
        else:
            self._freq_class = UInt16Field
        if self._format.analogs is NumberFormatEnum.FLOAT:
            self._analogs_class = Float32Field
        else:
            self._analogs_class = UInt16Field
        super().__init__(
            name=name,
            default=[
                UInt16Field(name=FieldNameEnum.StatusFlags.value),
                ArrayFieldGeneric(
                    name=FieldNameEnum.PhasorList.value,
                    array_item_class=self._phasor_class,
                    array_item_default=0,
                    count=phasor_count,
                ),
                self._freq_class(name=FieldNameEnum.Frequency.value),
                self._freq_class(name=FieldNameEnum.FrequencyDelta.value),
                ArrayFieldGeneric(
                    name=FieldNameEnum.AnalogList.value,
                    array_item_class=self._analogs_class,
                    array_item_default=0,
                    count=analog_count,
                ),
                ArrayFieldGeneric(
                    name=FieldNameEnum.DigitalList.value,
                    array_item_class=UInt16Field,
                    array_item_default=0,
                    count=digital_count,
                ),
            ],
            data=data,
        )

    @property
    def phasor_list(
        self,
    ) -> list[Phasor]:
        """Get phasor fields.

        Returns:
            phasor fields
        """
        return cast("ArrayFieldGeneric[Phasor]", self[FieldNameEnum.PhasorList.value]).value_list

    @property
    def analog_list(
        self,
    ) -> list[Float32Field] | list[UInt16Field]:
        """Get phasor fields.

        Returns:
            phasor fields
        """
        return cast(
            "Union[ArrayFieldGeneric[Float32Field], ArrayFieldGeneric[UInt16Field]]",
            self[FieldNameEnum.AnalogList.value],
        ).value_list

    @property
    def digital_list(
        self,
    ) -> list[UInt16Field]:
        """Get phasor fields.

        Returns:
            phasor fields
        """
        return cast("ArrayFieldGeneric[UInt16Field]", self[FieldNameEnum.AnalogList.value]).value_list
