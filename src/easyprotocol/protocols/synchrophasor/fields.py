"""Synchrophasor field classes."""
from __future__ import annotations

import math
from enum import Enum, IntEnum, IntFlag
from typing import cast

from bitarray import bitarray
from bitarray.util import int2ba
from crc import Configuration

from easyprotocol.base import DEFAULT_ENDIANNESS, BaseField, dataT, input_to_bytes
from easyprotocol.base.dict import DictField
from easyprotocol.fields import (
    BoolField,
    ChecksumField,
    FlagsField,
    Float32Field,
    StringField,
    UInt8Field,
    UInt16Field,
    UIntField,
)
from easyprotocol.fields.array import ArrayFieldGeneric
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
    def start(self) -> int:
        """Get start value integer.

        Returns:
            start value
        """
        return cast("UInt8Field", self[FieldNameEnum.Start.value]).value

    @property
    def version(self) -> int:
        """Get version integer.

        Returns:
            version value
        """
        return cast("UIntField", self[FieldNameEnum.Version.value]).value

    @property
    def frameType(self) -> FrameTypeEnum:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("FrameType", self[FieldNameEnum.FrameType.value]).value

    @property
    def syncBit(self) -> bool:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("BoolField", self[FieldNameEnum.SyncBit.value]).value


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
            byte_data = input_to_bytes(data=data, bit_count=self._bit_count).tobytes()
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
                EnumField(
                    name=FieldNameEnum.CoordinateFormat.value,
                    bit_count=1,
                    enum_type=CoordinateFormatEnum,
                    default=CoordinateFormatEnum.POLAR,
                ),
                EnumField(
                    name=FieldNameEnum.PhasorFormat.value,
                    bit_count=1,
                    enum_type=NumberFormatEnum,
                    default=NumberFormatEnum.FLOAT,
                ),
                EnumField(
                    name=FieldNameEnum.AnalogFormat.value,
                    bit_count=1,
                    enum_type=NumberFormatEnum,
                    default=NumberFormatEnum.FLOAT,
                ),
                EnumField(
                    name=FieldNameEnum.FrequencyFormat.value,
                    bit_count=1,
                    enum_type=NumberFormatEnum,
                    default=NumberFormatEnum.FLOAT,
                ),
                UIntField(
                    name=FieldNameEnum.FormatExtra2.value,
                    bit_count=4,
                ),
            ],
            data=data,
        )

    @property
    def frequencies(self) -> NumberFormatEnum:
        """Get frequency format.

        Returns:
            frequency format
        """
        return cast(NumberFormatEnum, self[FieldNameEnum.FrequencyFormat.value].value)

    @property
    def analogs(self) -> NumberFormatEnum:
        """Get analog format.

        Returns:
            analog format
        """
        return cast(NumberFormatEnum, self[FieldNameEnum.AnalogFormat.value].value)

    @property
    def phasors(self) -> NumberFormatEnum:
        """Get phasor format.

        Returns:
            phasor format
        """
        return cast(NumberFormatEnum, self[FieldNameEnum.PhasorFormat.value].value)

    @property
    def coordinates(self) -> CoordinateFormatEnum:
        """Get coordinate format.

        Returns:
            coordinate format
        """
        return cast(CoordinateFormatEnum, self[FieldNameEnum.CoordinateFormat.value].value)


class StringFixedLengthField(StringField):
    """Fixed length 16-byte string field."""

    def __init__(
        self,
        name: str,
        count: int = 16,
        default_char: str = " ",
        default: str = "",
        data: dataT | None = None,
    ) -> None:
        """Create fixed length 16-byte string field.

        Args:
            name: name of field
            count: byte count. Defaults to 16.
            default_char: default character value. Defaults to " ".
            default: default field value. Defaults to "".
            data: data to parse. Defaults to None.
        """
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


class Station(StringFixedLengthField):
    """Station name field."""

    def __init__(
        self,
        default: str = "",
        data: dataT | None = None,
    ) -> None:
        """Create station name field.

        Args:
            default: default value. Defaults to "".
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name="STN",
            count=16,
            default=default,
            data=data,
        )


class ChannelName(StringFixedLengthField):
    """Channel name string."""

    def __init__(
        self,
        name: str = "CHNAM",
        default: str = "",
        data: dataT | None = None,
    ) -> None:
        """Create channel name string.

        Args:
            name: name of field. Defaults to "CHNAM".
            default: default value. Defaults to "".
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=name,
            default=default,
            data=data,
            count=16,
        )


class FixedLengthStringArray(
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
            array_item_class=StringFixedLengthField,
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
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, int):
            count = self._fixed_string_length * self._count
        else:
            count = self._fixed_string_length * self._count.value
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
