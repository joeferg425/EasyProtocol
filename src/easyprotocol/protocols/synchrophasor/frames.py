"""Synchrophasor packet classes."""
from __future__ import annotations

from typing import Union, cast

from bitarray import bitarray

from easyprotocol.base import DictField, dataT
from easyprotocol.base.base import BaseField
from easyprotocol.base.utils import input_to_bytes
from easyprotocol.fields import (
    ArrayFieldGeneric,
    Float32Field,
    UInt16Field,
    UInt32Field,
)
from easyprotocol.fields.unsigned_int import UIntFieldGeneric
from easyprotocol.protocols.synchrophasor.fields import (
    Checksum,
    CoordinateFormatEnum,
    FieldNameEnum,
    FixedLengthStringArray,
    Format,
    FrameTypeEnum,
    FrameTypeNameEnum,
    NumberFormatEnum,
    Phasor,
    PhasorPolarFloat,
    PhasorPolarInt,
    PhasorRectangularFloat,
    PhasorRectangularInt,
    StringFixedLengthField,
    Sync,
)


class SynchrophasorFrame(DictField):
    """Packet header class for determining what type of frame it is."""

    def __init__(
        self,
        name: str = FrameTypeNameEnum.Frame.value,
        data: dataT = None,
        default: list[BaseField] | None = None,
    ) -> None:
        """Create packet header with frame type information.

        Args:
            name: name of frame
            data: data to parse. Defaults to None.
            default: default child fields
        """
        if default is None:
            default = []
        super().__init__(
            name=name,
            default=[
                Sync(),
            ]
            + default,
            data=data,
        )

    @property
    def start(self) -> int:
        """Get start value integer.

        Returns:
            start value
        """
        return cast("Sync", self[FieldNameEnum.Sync.value]).start

    @property
    def version(self) -> int:
        """Get version integer.

        Returns:
            version value
        """
        return cast("Sync", self[FieldNameEnum.Sync.value]).version

    @property
    def frameType(self) -> FrameTypeEnum:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("Sync", self[FieldNameEnum.Sync.value]).frameType

    @property
    def syncBit(self) -> bool:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("Sync", self[FieldNameEnum.Sync.value]).syncBit


class SynchrophasorConfigurationFrame(SynchrophasorFrame):
    """PMU configuration object."""

    def __init__(
        self,
        name: str = FieldNameEnum.PMUConfiguration.value,
        default: list[BaseField] | None = None,
        data: dataT = None,
    ) -> None:
        """Create PMU configuration object.

        Args:
            name: name of field. Defaults to "PMU_CONFIGURATION".
            default: default value. Defaults to None.
            data: data to parse. Defaults to None.
        """
        self._ph_nmr = UInt16Field(name=FieldNameEnum.PhasorCount.value)
        self._an_nmr = UInt16Field(name=FieldNameEnum.AnalogCount.value)
        self._dg_nmr = UInt16Field(name=FieldNameEnum.DigitalCount.value)
        super().__init__(
            name=name,
            data=data,
            default=[
                StringFixedLengthField(name=FieldNameEnum.StationName.value, count=16),
                UInt16Field(name=FieldNameEnum.IDCode.value),
                Format(),
                self._ph_nmr,
                self._an_nmr,
                self._dg_nmr,
                FixedLengthStringArray(
                    name=FieldNameEnum.PhasorNames.value,
                    count=self._ph_nmr,
                ),
                FixedLengthStringArray(
                    name=FieldNameEnum.AnalogNames.value,
                    count=self._an_nmr,
                ),
                FixedLengthStringArray(
                    name=FieldNameEnum.DigitalNames.value,
                    count=self._dg_nmr,
                ),
                ArrayFieldGeneric(
                    name=FieldNameEnum.PhasorUnit.value,
                    array_item_class=Float32Field,
                    array_item_default=0.0,
                    count=self._ph_nmr,
                ),
                ArrayFieldGeneric(
                    name=FieldNameEnum.AnalogUnit.value,
                    array_item_class=Float32Field,
                    array_item_default=0.0,
                    count=self._an_nmr,
                ),
                ArrayFieldGeneric(
                    name=FieldNameEnum.DigitalUnit.value,
                    array_item_class=UInt32Field,
                    array_item_default=0.0,
                    count=self._dg_nmr,
                ),
                UInt16Field(name=FieldNameEnum.NominalFrequency.value),
                UInt16Field(name=FieldNameEnum.ConfigurationCount.value),
            ],
        )

    @property
    def station_name(self) -> str:
        """Get the station name.

        Returns:
            the station name
        """
        return cast("StringFixedLengthField", self[FieldNameEnum.StationName.value]).value_as_string

    @property
    def phasor_names(self) -> list[str]:
        """Get the phasor names.

        Returns:
            the phasor names
        """
        return cast("FixedLengthStringArray", self[FieldNameEnum.PhasorNames.value]).value_list

    @property
    def analog_names(self) -> list[str]:
        """Get the analog names.

        Returns:
            the analog names
        """
        return cast("FixedLengthStringArray", self[FieldNameEnum.AnalogNames.value]).value_list

    @property
    def digital_names(self) -> list[str]:
        """Get the digital names.

        Returns:
            the digital names
        """
        return cast("FixedLengthStringArray", self[FieldNameEnum.DigitalNames.value]).value_list


class SynchrophasorConfiguration1Frame(SynchrophasorConfigurationFrame):
    """Configuration Frame Type 1."""

    def __init__(
        self,
        name: str = FrameTypeNameEnum.Configuration1.value,
        data: dataT = None,
    ) -> None:
        """Create Configuration Frame Type 1.

        Args:
            name: name of field. Defaults to "CONFIGURATION1".
            data: data to be parsed. Defaults to None.
        """
        self._num_pmu = UInt16Field(name=FieldNameEnum.PMUCount.value)
        super().__init__(
            name=name,
            default=[
                Sync(),
                UInt16Field(name=FieldNameEnum.FrameSize.value),
                UInt16Field(name=FieldNameEnum.IDCode.value),
                UInt32Field(name=FieldNameEnum.SecondsOfCentury.value),
                UInt32Field(name=FieldNameEnum.FractionalSeconds.value),
                UInt32Field(name=FieldNameEnum.TimeBase.value),
                self._num_pmu,
                ArrayFieldGeneric[SynchrophasorConfigurationFrame](
                    name=FieldNameEnum.PMUConfigurations.value,
                    array_item_class=type(SynchrophasorConfigurationFrame),
                    array_item_default=SynchrophasorConfigurationFrame(),
                    count=self._num_pmu,
                ),
                UInt16Field(name=FieldNameEnum.DataRate.value),
                Checksum(),
            ],
            data=data,
        )

    @property
    def pmu_configs(self) -> list[SynchrophasorConfigurationFrame]:
        """Get pmu configuration list.

        Returns:
            pmu configuration list
        """
        return cast(
            "ArrayFieldGeneric[SynchrophasorConfigurationFrame]", self[FieldNameEnum.PMUConfigurations.value]
        ).value_list

    @property
    def formats(self) -> list[Format]:
        """Get pmu formats.

        Returns:
            pmu formats
        """
        pmu_configs = cast(
            "ArrayFieldGeneric[SynchrophasorConfigurationFrame]", self[FieldNameEnum.PMUConfiguration.value]
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
            "ArrayFieldGeneric[SynchrophasorConfigurationFrame]", self[FieldNameEnum.PMUConfigurations.value]
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
            "ArrayFieldGeneric[SynchrophasorConfigurationFrame]", self[FieldNameEnum.PMUConfiguration.value]
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
            "ArrayFieldGeneric[SynchrophasorConfigurationFrame]", self[FieldNameEnum.PMUConfiguration.value]
        ).value_list
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config[FieldNameEnum.DigitalCount.value]).value)
        return counts


class SynchrophasorConfiguration2Frame(SynchrophasorConfiguration1Frame):
    """Configuration Frame Type 2."""

    def __init__(
        self,
        name: str = FrameTypeNameEnum.Configuration2.value,
        data: dataT = None,
    ) -> None:
        """Create Configuration Frame Type 2.

        Args:
            name: name of frame. Defaults to "CONFIGURATION2".
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=name,
            data=data,
        )


class SynchrophasorCommandFrame(SynchrophasorFrame):
    """Command frame."""

    def __init__(
        self,
        data: dataT = None,
    ) -> None:
        """Create Command frame.

        Args:
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name=FrameTypeNameEnum.Command.value,
            default=[
                UInt16Field(name=FieldNameEnum.FrameSize.value),
                UInt16Field(name=FieldNameEnum.IDCode.value),
                UInt32Field(name=FieldNameEnum.SecondsOfCentury.value),
                UInt32Field(name=FieldNameEnum.FractionalSeconds.value),
                UInt16Field(name=FieldNameEnum.Command.value),
                Checksum(),
            ],
            data=data,
        )

    @property
    def frameSize(self) -> int:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        return cast("UInt16Field", self[FieldNameEnum.FrameSize.value]).value


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
            count=len(self._config.pmu_configs),
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
        bit_data = input_to_bytes(data=data)
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
                UInt32Field(name=FieldNameEnum.SecondsOfCentury.value),
                UInt32Field(name=FieldNameEnum.FractionalSeconds.value),
                PMUDataArray(
                    name=FieldNameEnum.PMUData.value,
                    config=self._config,
                    analog_counts=analog_counts,
                    digital_counts=digital_counts,
                    phasor_counts=phasor_counts,
                ),
                Checksum(),
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
        for pmu_idx, pmu_config in enumerate(self._config.pmu_configs):
            pmu_name = pmu_config.station_name
            pmu = self.pmu_list[pmu_idx]
            summary[pmu_name] = {}
            for phasor_index, phasor_name in enumerate(pmu_config.phasor_names):
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
