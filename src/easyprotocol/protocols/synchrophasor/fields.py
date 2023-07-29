"""Synchrophasor field classes."""
from __future__ import annotations

import math
from enum import IntEnum
from typing import cast

import crc
from bitarray import bitarray
from bitarray.util import int2ba

from easyprotocol.base import dataT, input_to_bytes
from easyprotocol.base.dict import DictField
from easyprotocol.fields import (
    ArrayFieldGeneric,
    BoolField,
    ChecksumField,
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

    DATA = 0
    CONFIGURATION1 = 2
    CONFIGURATION2 = 3
    COMMAND = 4


class FRAMETYPE(EnumField[FrameTypeEnum]):
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
            name="FRAMETYPE",
            enum_type=FrameTypeEnum,
            default=default,
            data=data,
            bit_count=3,
        )


class SYNC(DictField):
    """SYNC field parser."""

    def __init__(
        self,
        frame_type: FrameTypeEnum = FrameTypeEnum.DATA,
        data: dataT = None,
    ) -> None:
        """Parse the members of the sync field.

        Args:
            frame_type: frame type enum. Defaults to FrameTypeEnum.DATA.
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name="SYNC",
            data=data,
            default=[
                UInt8Field(name="START", default=0xAA),
                UIntField(name="VERSION", bit_count=4),
                FRAMETYPE(default=frame_type),
                BoolField(name="BIT"),
            ],
        )


class CHK(ChecksumField):
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
            name="CHK",
            default=default,
            data=data,
            bit_count=16,
            crc_configuration=crc.Crc16.CCITT.value,
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
        crc_int = int.from_bytes(crc_bytes, byteorder=self._endian, signed=False)
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


class FORMAT(DictField):
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

    @property
    def frequencies(self) -> NumberFormatEnum:
        """Get frequency format.

        Returns:
            frequency format
        """
        return cast(NumberFormatEnum, self["FREQFORMAT"].value)

    @property
    def analogs(self) -> NumberFormatEnum:
        """Get analog format.

        Returns:
            analog format
        """
        return cast(NumberFormatEnum, self["ANALOGFORMAT"].value)

    @property
    def phasors(self) -> NumberFormatEnum:
        """Get phasor format.

        Returns:
            phasor format
        """
        return cast(NumberFormatEnum, self["PHASORFORMAT"].value)

    @property
    def coordinates(self) -> CoordinateFormatEnum:
        """Get coordinate format.

        Returns:
            coordinate format
        """
        return cast(CoordinateFormatEnum, self["COORDINATEFORMAT"].value)


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


class STN(StringFixedLengthField):
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


class CHNAM(StringFixedLengthField):
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


class DIGNAMS(ArrayFieldGeneric[str]):
    """Array of digital names."""

    def __init__(
        self,
        count: UIntFieldGeneric[int],
        data: dataT | None = None,
    ) -> None:
        """Create array of digital names.

        Args:
            count: count of digital words (name count is word count * 16)
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name="DIGNAMS",
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
            count = 16 * self._count
        else:
            count = 16 * self._count.value
        for i in range(count):
            f = self._array_item_class(
                name=f"#{i}",
                default=self._array_item_default,
            )
            bit_data = f.parse(data=bit_data)
            self._children[f.name] = f
        return bit_data


class PHASOR:
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


class PHASOR_POLAR_FLOAT(DictField, PHASOR):
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


class PHASOR_POLAR_INT(DictField, PHASOR):
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


class PHASOR_RECTANGULAR_FLOAT(DictField, PHASOR):
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


class PHASOR_RECTANGULAR_INT(DictField, PHASOR):
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
