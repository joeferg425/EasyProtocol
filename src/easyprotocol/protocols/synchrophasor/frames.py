"""Synchrophasor packet classes."""
from __future__ import annotations

from datetime import datetime
from typing import cast

from bitarray import bitarray

from easyprotocol.base import DictField, dataT
from easyprotocol.base.base import BaseField
from easyprotocol.base.utils import input_to_bitarray
from easyprotocol.fields import (
    ArrayFieldGeneric,
    DateTimeField,
    UInt16Field,
    UInt24Field,
    UInt32Field,
)
from easyprotocol.fields.unsigned_int import (
    BoolField,
    UInt8Field,
    UIntField,
    UIntFieldGeneric,
)
from easyprotocol.protocols.synchrophasor.fields import (
    Command,
    CommandEnum,
    CoordinateFormatEnum,
    FieldNameEnum,
    Format,
    FrameType,
    FrameTypeEnum,
    FrameTypeNameEnum,
    Phasor,
    PMUData,
    Sync,
    SynchrophasorChecksum,
    SynchrophasorConfiguration,
    TimeQuality,
    TimeQualityCode,
    TimeQualityCodeEnum,
    TimeQualityFlags,
    TimeQualityFlagsField,
)


class SynchrophasorFrame(DictField):
    """Packet header class for determining what type of frame it is."""

    def __init__(
        self,
        name: str = FrameTypeNameEnum.Frame.value,
        start: int | None = None,
        version: int | None = None,
        frame_type: FrameTypeEnum | None = None,
        sync_bit: bool | None = None,
        data: dataT = None,
        fields: list[BaseField] | None = None,
    ) -> None:
        """Create packet header with frame type information.

        Args:
            name: name of frame
            start: start bits. Defaults to AA.
            version: defaults to 1.
            frame_type: frame type enum. Defaults to FrameTypeEnum.DATA.
            sync_bit: defaults to false
            data: data to parse. Defaults to None.
            fields: default child fields
        """
        if fields is None:
            fields = []
        super().__init__(
            name=name,
            default=[
                Sync(
                    start=start,
                    version=version,
                    frame_type=frame_type,
                    sync_bit=sync_bit,
                ),
            ]
            + fields,
            data=data,
        )

    @property
    def start(self) -> UInt8Field:
        """Get start value integer.

        Returns:
            start value
        """
        return cast("Sync", self[FieldNameEnum.Sync.value]).start

    @start.setter
    def start(self, value: UInt8Field | int) -> None:
        if isinstance(value, UInt8Field):
            self.start.value = value.value
        else:
            self.start.value = value

    @property
    def version(self) -> UIntField:
        """Get version integer.

        Returns:
            version value
        """
        return cast("Sync", self[FieldNameEnum.Sync.value]).version

    @version.setter
    def version(self, value: UIntField | int) -> None:
        if isinstance(value, UIntField):
            self.version.value = value.value
        else:
            self.version.value = value

    @property
    def frameType(self) -> FrameType:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("Sync", self[FieldNameEnum.Sync.value]).frameType

    @frameType.setter
    def frameType(self, value: FrameType | FrameTypeEnum) -> None:
        if isinstance(value, FrameType):
            self.frameType.value = value.value
        else:
            self.frameType.value = value

    @property
    def syncBit(self) -> BoolField:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("Sync", self[FieldNameEnum.Sync.value]).syncBit

    @syncBit.setter
    def syncBit(self, value: BoolField | bool) -> None:
        if isinstance(value, BoolField):
            self.syncBit.value = value.value
        else:
            self.syncBit.value = value


class SynchrophasorConfiguration1Frame(SynchrophasorFrame):
    """Configuration Frame Type 1."""

    def __init__(
        self,
        name: str = FrameTypeNameEnum.Configuration1.value,
        time_quality_flags: TimeQualityFlags | None = None,
        time_quality_code: TimeQualityCodeEnum | None = None,
        data: dataT = None,
    ) -> None:
        """Create Configuration Frame Type 1.

        Args:
            name: name of field. Defaults to "CONFIGURATION1".
            time_quality_flags: time quality flags
            time_quality_code: time quality code
            data: data to be parsed. Defaults to None.
        """
        self._num_pmu = UInt16Field(name=FieldNameEnum.PMUCount.value)
        super().__init__(
            name=name,
            fields=[
                UInt16Field(name=FieldNameEnum.FrameSize.value),
                UInt16Field(name=FieldNameEnum.IDCode.value),
                DateTimeField(name=FieldNameEnum.SecondsOfCentury.value),
                TimeQuality(
                    time_quality_code=time_quality_code,
                    time_quality_flags=time_quality_flags,
                ),
                UInt24Field(name=FieldNameEnum.FractionalSeconds.value),
                UInt8Field(name=FieldNameEnum.TimeBase.value),
                UInt24Field(name=FieldNameEnum.Resolution.value),
                self._num_pmu,
                ArrayFieldGeneric[SynchrophasorConfiguration](
                    name=FieldNameEnum.PMUConfigurations.value,
                    array_item_class=SynchrophasorConfiguration,
                    array_item_default=SynchrophasorConfiguration(),
                    count=self._num_pmu,
                ),
                UInt16Field(name=FieldNameEnum.DataRate.value),
                SynchrophasorChecksum(),
            ],
            data=data,
        )

    @property
    def frameSize(self) -> UInt16Field:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("UInt16Field", self[FieldNameEnum.FrameSize.value])

    @frameSize.setter
    def frameSize(self, value: UInt16Field | int) -> None:
        if isinstance(value, UInt16Field):
            self.frameSize.value = value.value
        else:
            self.frameSize.value = value

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
    def soc(self) -> DateTimeField:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("DateTimeField", self[FieldNameEnum.SecondsOfCentury.value])

    @soc.setter
    def soc(self, value: DateTimeField | datetime) -> None:
        if isinstance(value, DateTimeField):
            self.soc.value = value.value
        else:
            self.soc.value = value

    @property
    def timeQualityFlags(self) -> TimeQualityFlagsField:
        """Get time quality flags.

        Returns:
            time quality flags
        """
        tq = cast("TimeQuality", self[FieldNameEnum.TimeQuality.value])
        return cast("TimeQualityFlagsField", tq[FieldNameEnum.TimeQualityFlags.value])

    @timeQualityFlags.setter
    def timeQualityFlags(self, value: TimeQualityFlagsField | TimeQualityFlags) -> None:
        if isinstance(value, TimeQualityFlagsField):
            self.timeQualityFlags.value = value.value
        else:
            self.timeQualityFlags.value = value

    @property
    def timeQualityCode(self) -> TimeQualityCode:
        """Get time quality code.

        Returns:
            time quality code
        """
        tq = cast("TimeQuality", self[FieldNameEnum.TimeQuality.value])
        return cast("TimeQualityCode", tq[FieldNameEnum.TimeQualityCode.value])

    @timeQualityCode.setter
    def timeQualityCode(self, value: TimeQualityCode | TimeQualityCodeEnum) -> None:
        if isinstance(value, TimeQualityCode):
            self.timeQualityCode.value = value.value
        else:
            self.timeQualityCode.value = value

    @property
    def fractionalSeconds(self) -> UInt24Field:
        """Get fractional seconds.

        Returns:
            fractional seconds
        """
        return cast("UInt24Field", self[FieldNameEnum.FractionalSeconds.value])

    @fractionalSeconds.setter
    def fractionalSeconds(self, value: UInt24Field | int) -> None:
        if isinstance(value, UInt24Field):
            self.fractionalSeconds.value = value.value
        else:
            self.fractionalSeconds.value = value

    @property
    def pmuCount(self) -> int:
        """Get fractional seconds.

        Returns:
            fractional seconds
        """
        return cast("UInt16Field", self[FieldNameEnum.PMUCount.value]).value

    @property
    def pmuConfigs(self) -> list[SynchrophasorConfiguration]:
        """Get pmu configuration list.

        Returns:
            pmu configuration list
        """
        return cast(
            "list[SynchrophasorConfiguration]",
            cast("ArrayFieldGeneric[SynchrophasorConfiguration]", self[FieldNameEnum.PMUConfigurations.value]).value,
        )

    @property
    def formats(self) -> list[Format]:
        """Get pmu formats.

        Returns:
            pmu formats
        """
        pmu_configs = cast(
            "ArrayFieldGeneric[SynchrophasorConfiguration]", self[FieldNameEnum.PMUConfiguration.value]
        ).value_list
        formats: list[Format] = []
        for pmu_config in pmu_configs:
            fmt = cast("Format", pmu_config[FieldNameEnum.Format.value])
            formats.append(fmt)
        return formats

    @property
    def phasor_counts(self) -> list[int]:
        """Get phasor counts.

        Returns:
            phasor counts
        """
        pmu_configs = cast(
            "ArrayFieldGeneric[SynchrophasorConfiguration]", self[FieldNameEnum.PMUConfigurations.value]
        ).value_list
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config[FieldNameEnum.PhasorCount.value]).value)
        return counts

    @property
    def analog_counts(self) -> list[int]:
        """Get analog counts.

        Returns:
            analog counts
        """
        pmu_configs = cast(
            "ArrayFieldGeneric[SynchrophasorConfiguration]", self[FieldNameEnum.PMUConfiguration.value]
        ).value_list
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config[FieldNameEnum.AnalogCount.value]).value)
        return counts

    @property
    def digital_counts(self) -> list[int]:
        """Get digital counts.

        Returns:
            digital counts
        """
        pmu_configs = cast(
            "ArrayFieldGeneric[SynchrophasorConfiguration]", self[FieldNameEnum.PMUConfiguration.value]
        ).value_list
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config[FieldNameEnum.DigitalCount.value]).value)
        return counts

    @property
    def timeBase(self) -> UInt8Field:
        """Get fractional seconds.

        Returns:
            fractional seconds
        """
        return cast("UInt8Field", self[FieldNameEnum.TimeBase.value])

    @timeBase.setter
    def timeBase(self, value: UInt8Field | int) -> None:
        if isinstance(value, UInt8Field):
            self.timeBase.value = value.value
        else:
            self.timeBase.value = value

    @property
    def resolution(self) -> UInt24Field:
        """Get fractional seconds.

        Returns:
            fractional seconds
        """
        return cast("UInt24Field", self[FieldNameEnum.Resolution.value])

    @resolution.setter
    def resolution(self, value: UInt24Field | int) -> None:
        if isinstance(value, UInt24Field):
            self.resolution.value = value.value
        else:
            self.resolution.value = value

    @property
    def dataRate(self) -> UInt16Field:
        """Get fractional seconds.

        Returns:
            fractional seconds
        """
        return cast("UInt16Field", self[FieldNameEnum.DataRate.value])

    @dataRate.setter
    def dataRate(self, value: UInt16Field | int) -> None:
        if isinstance(value, UInt16Field):
            self.dataRate.value = value.value
        else:
            self.dataRate.value = value

    @property
    def checksum(self) -> SynchrophasorChecksum:
        """Get checksum.

        Returns:
            checksum
        """
        return cast("SynchrophasorChecksum", self[FieldNameEnum.Checksum.value])

    @checksum.setter
    def checksum(self, value: SynchrophasorChecksum | int) -> None:
        if isinstance(value, SynchrophasorChecksum):
            self.checksum.value = value.value
        else:
            self.checksum.value = value


class SynchrophasorConfiguration2Frame(SynchrophasorConfiguration1Frame):
    """Configuration Frame Type 2."""

    def __init__(
        self,
        data: dataT = None,
    ) -> None:
        """Create Configuration Frame Type 2.

        Args:
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=FrameTypeNameEnum.Configuration2.value,
            data=data,
        )


class SynchrophasorCommandFrame(SynchrophasorFrame):
    """Command frame."""

    def __init__(
        self,
        start: int | None = None,
        version: int | None = None,
        frame_type: FrameTypeEnum | None = None,
        sync_bit: bool | None = None,
        frame_size: int | None = None,
        id_code: int | None = None,
        fractional_seconds: int | None = None,
        time_quality_flags: TimeQualityFlags | None = None,
        time_quality_code: TimeQualityCodeEnum | None = None,
        time_stamp: datetime | None = None,
        command: CommandEnum | None = None,
        checksum_value: int | None = None,
        update_checksum: bool = False,
        data: dataT = None,
    ) -> None:
        """Create Command frame.

        Args:
            start: start bits. Defaults to AA.
            version: defaults to 1.
            frame_type: frame type enum. Defaults to FrameTypeEnum.DATA.
            sync_bit: defaults to false
            frame_size: frame size, defaults to 18
            id_code: defaults to 1
            time_quality_flags: time quality flags.
            time_quality_code: time quality code.
            time_stamp: frame timestamp
            fractional_seconds: fraction of a second. defaults to 0
            command: defaults to send config2
            checksum_value: defaults to 0
            update_checksum: set true to update checksum. defaults to false
            data: data to parse. Defaults to None.
        """
        if frame_size is None:
            frame_size = 18
        if id_code is None:
            id_code = 1
        if time_stamp is None:
            time_stamp = datetime.utcfromtimestamp(0)
        if fractional_seconds is None:
            fractional_seconds = 0
        if command is None:
            command = CommandEnum.SendConfiguration2
        if checksum_value is None:
            checksum_value = 0
        super().__init__(
            name=FrameTypeNameEnum.Command.value,
            start=start,
            version=version,
            frame_type=frame_type,
            sync_bit=sync_bit,
            fields=[
                UInt16Field(
                    name=FieldNameEnum.FrameSize.value,
                    default=frame_size,
                ),
                UInt16Field(
                    name=FieldNameEnum.IDCode.value,
                    default=id_code,
                ),
                DateTimeField(
                    name=FieldNameEnum.SecondsOfCentury.value,
                    default=time_stamp,
                ),
                TimeQuality(
                    time_quality_code=time_quality_code,
                    time_quality_flags=time_quality_flags,
                ),
                UInt24Field(
                    name=FieldNameEnum.FractionalSeconds.value,
                    default=fractional_seconds,
                ),
                UInt16Field(
                    name=FieldNameEnum.Command.value,
                    default=command,
                ),
                SynchrophasorChecksum(
                    default=checksum_value,
                ),
            ],
            data=data,
        )
        if update_checksum:
            self.update_checksum()

    def update_checksum(self) -> SynchrophasorChecksum:
        """Update the checksum using the current field values.

        Returns:
            the updated checksum field
        """
        self.checksum.update_field(self.bits[:-16])
        return self.checksum

    @property
    def frameSize(self) -> UInt16Field:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("UInt16Field", self[FieldNameEnum.FrameSize.value])

    @frameSize.setter
    def frameSize(self, value: UInt16Field | int) -> None:
        if isinstance(value, UInt16Field):
            self.frameSize.value = value.value
        else:
            self.frameSize.value = value

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
    def soc(self) -> DateTimeField:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("DateTimeField", self[FieldNameEnum.SecondsOfCentury.value])

    @soc.setter
    def soc(self, value: DateTimeField | datetime) -> None:
        if isinstance(value, DateTimeField):
            self.soc.value = value.value
        else:
            self.soc.value = value

    @property
    def timeQualityFlags(self) -> TimeQualityFlagsField:
        """Get time quality flags.

        Returns:
            time quality flags
        """
        tq = cast("TimeQuality", self[FieldNameEnum.TimeQuality.value])
        return cast("TimeQualityFlagsField", tq[FieldNameEnum.TimeQualityFlags.value])

    @timeQualityFlags.setter
    def timeQualityFlags(self, value: TimeQualityFlagsField | TimeQualityFlags) -> None:
        if isinstance(value, TimeQualityFlagsField):
            self.timeQualityFlags.value = value.value
        else:
            self.timeQualityFlags.value = value

    @property
    def timeQualityCode(self) -> TimeQualityCode:
        """Get time quality code.

        Returns:
            time quality code
        """
        tq = cast("TimeQuality", self[FieldNameEnum.TimeQuality.value])
        return cast("TimeQualityCode", tq[FieldNameEnum.TimeQualityCode.value])

    @timeQualityCode.setter
    def timeQualityCode(self, value: TimeQualityCode | TimeQualityCodeEnum) -> None:
        if isinstance(value, TimeQualityCode):
            self.timeQualityCode.value = value.value
        else:
            self.timeQualityCode.value = value

    @property
    def fractionalSeconds(self) -> UInt24Field:
        """Get fractional seconds.

        Returns:
            fractional seconds
        """
        return cast("UInt24Field", self[FieldNameEnum.FractionalSeconds.value])

    @fractionalSeconds.setter
    def fractionalSeconds(self, value: UInt24Field | int) -> None:
        if isinstance(value, UInt24Field):
            self.fractionalSeconds.value = value.value
        else:
            self.fractionalSeconds.value = value

    @property
    def command(self) -> Command:
        """Get command.

        Returns:
            command
        """
        return cast("Command", self[FieldNameEnum.Command.value])

    @command.setter
    def command(self, value: Command | CommandEnum) -> None:
        if isinstance(value, Command):
            self.command.value = value.value
        else:
            self.command.value = value

    @property
    def checksum(self) -> SynchrophasorChecksum:
        """Get checksum.

        Returns:
            checksum
        """
        return cast("SynchrophasorChecksum", self[FieldNameEnum.Checksum.value])

    @checksum.setter
    def checksum(self, value: SynchrophasorChecksum | int) -> None:
        if isinstance(value, SynchrophasorChecksum):
            self.checksum.value = value.value
        else:
            self.checksum.value = value


class PMUDataArray(ArrayFieldGeneric[PMUData]):
    """PMU data array field."""

    def __init__(
        self,
        name: str,
        phasor_counts: list[int],
        analog_counts: list[int],
        digital_counts: list[int],
        config: SynchrophasorConfiguration1Frame | SynchrophasorConfiguration2Frame,
        data: dataT | None = None,
    ) -> None:
        """Create PMU data array field.

        Args:
            name: name of field
            phasor_counts: number of phasors
            analog_counts: number of analog values
            digital_counts: number of digital words
            config: configuration frame associated with synchrophasor stream
            data: data to parse. Defaults to None.
        """
        self._phasor_counts = phasor_counts
        self._analog_counts = analog_counts
        self._digital_counts = digital_counts
        self._config = config
        super().__init__(
            name,
            count=len(self._config.pmuConfigs),
            array_item_class=type(PMUData),
            array_item_default=PMUData(phasor_count=0, analog_count=0, digital_count=0, pmu_format=Format()),
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
        if isinstance(self._count, UIntFieldGeneric):
            count = self._count.value
        else:
            count = self._count
        for i in range(count):
            f = PMUData(
                name=f"#{i}",
                default=None,
                phasor_count=self._phasor_counts[i],
                analog_count=self._analog_counts[i],
                digital_count=self._digital_counts[i],
                pmu_format=self._config.formats[i],
            )
            bit_data = f.parse(data=bit_data)
            self._children[f.name] = f
        return bit_data


class SynchrophasorDataFrame(DictField):
    """Data parser."""

    def __init__(
        self,
        config: SynchrophasorConfiguration1Frame | SynchrophasorConfiguration2Frame,
        phasor_counts: list[int],
        analog_counts: list[int],
        digital_counts: list[int],
        data: dataT = None,
    ) -> None:
        """Create data parser.

        Args:
            phasor_counts: number of phasors
            analog_counts: number of analog values
            digital_counts: number of digital words
            config: configuration frame associated with synchrophasor stream
            data: data to parse. Defaults to None.
        """
        self._config = config
        super().__init__(
            name=FrameTypeNameEnum.Data.value,
            default=[
                Sync(),
                UInt16Field(name=FieldNameEnum.FrameSize.value),
                UInt16Field(name=FieldNameEnum.IDCode.value),
                DateTimeField(name=FieldNameEnum.SecondsOfCentury.value),
                UInt32Field(name=FieldNameEnum.FractionalSeconds.value),
                PMUDataArray(
                    name=FieldNameEnum.PMUData.value,
                    config=self._config,
                    analog_counts=analog_counts,
                    digital_counts=digital_counts,
                    phasor_counts=phasor_counts,
                ),
                SynchrophasorChecksum(),
            ],
            data=data,
        )

    @property
    def pmu_list(self) -> list[PMUData]:
        """Get pmu list.

        Returns:
            pmu list
        """
        return cast("PMUDataArray", self[FieldNameEnum.PMUData.value]).value_list

    @property
    def summary(self) -> dict[str, dict[str, Phasor]]:
        """Get summary.

        Returns:
            summary
        """
        summary: dict[str, dict[str, Phasor]] = {}
        for pmu_idx, pmu_config in enumerate(self._config.pmuConfigs):
            pmu_name = pmu_config.stationName.value_as_string
            pmu = self.pmu_list[pmu_idx]
            summary[pmu_name] = {}
            for phasor_index, phasor_name in enumerate(pmu_config.phasorNames):
                summary[pmu_name][phasor_name] = pmu.phasor_list[phasor_index]
        return summary

    def get_summary_str(
        self, coords: CoordinateFormatEnum | None = CoordinateFormatEnum.POLAR, names: bool = False
    ) -> str:
        """Get summary string.

        Args:
            coords: coordinate format. Defaults to CoordinateFormatEnum.POLAR.
            names: include names. Defaults to False.

        Returns:
            summary string
        """
        s: list[str] = []
        summary = self.summary
        for pmu_key in summary:
            for phasor_key in summary[pmu_key]:
                s.append(
                    f"{pmu_key}.{phasor_key}:{summary[pmu_key][phasor_key].get_summary(coords=coords,names=names)}"
                )
        return ", ".join(s)

    @property
    def summary_str(self) -> str:
        """Get summary string.

        Returns:
            summary string
        """
        return self.get_summary_str()
