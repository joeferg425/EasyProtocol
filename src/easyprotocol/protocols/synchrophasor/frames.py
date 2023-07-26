"""Synchrophasor packet classes."""
from __future__ import annotations

from typing import cast

from bitarray import bitarray

from easyprotocol.base import DictField, dataT
from easyprotocol.base.utils import input_to_bytes
from easyprotocol.fields import ArrayField, Float32Field, UInt16Field, UInt32Field
from easyprotocol.fields.unsigned_int import UIntFieldGeneric
from easyprotocol.protocols.synchrophasor.fields import (
    CHK,
    DIGNAMS,
    FORMAT,
    FRAMETYPE,
    PHASOR,
    PHASOR_POLAR_FLOAT,
    PHASOR_POLAR_INT,
    PHASOR_RECTANGULAR_FLOAT,
    PHASOR_RECTANGULAR_INT,
    SYNC,
    CoordinateFormatEnum,
    FrameTypeEnum,
    NumberFormatEnum,
    StringFixedLengthField,
)


class HEADER(DictField):
    """Packet header class for determining what type of frame it is."""

    def __init__(
        self,
        data: dataT = None,
    ) -> None:
        """Create packet header with frame type information.

        Args:
            data: data to parse. Defaults to None.
        """
        super().__init__(
            name="Header",
            default=[
                SYNC(),
            ],
            data=data,
        )

    @property
    def frame_type(self) -> FrameTypeEnum:
        """Get frame type enumeration.

        Returns:
            frame type enumeration
        """
        sync = cast("SYNC", self["SYNC"])
        frame_type = cast("FRAMETYPE", sync["FRAMETYPE"])
        return frame_type.value


class PMU_CONFIGURATION(DictField):
    """PMU configuration object."""

    def __init__(
        self,
        name: str = "PMU_CONFIGURATION",
        default: None = None,
        data: dataT = None,
    ) -> None:
        """Create PMU configuration object.

        Args:
            name: name of field. Defaults to "PMU_CONFIGURATION".
            default: default value. Defaults to None.
            data: data to parse. Defaults to None.
        """
        self._ph_nmr = UInt16Field(name="PHNMR")
        self._an_nmr = UInt16Field(name="ANNMR")
        self._dg_nmr = UInt16Field(name="DGNMR")
        super().__init__(
            name=name,
            data=data,
            default=[
                StringFixedLengthField(name="STN", count=16),
                UInt16Field(name="IDCODE"),
                FORMAT(),
                self._ph_nmr,
                self._an_nmr,
                self._dg_nmr,
                ArrayField(
                    name="PHNAMS",
                    array_item_class=StringFixedLengthField,
                    array_item_default="",
                    count=self._ph_nmr,
                ),
                ArrayField(
                    name="ANNAMS",
                    array_item_class=StringFixedLengthField,
                    array_item_default="",
                    count=self._an_nmr,
                ),
                DIGNAMS(
                    count=self._dg_nmr,
                ),
                ArrayField(
                    name="PHUNIT",
                    array_item_class=Float32Field,
                    array_item_default=0.0,
                    count=self._ph_nmr,
                ),
                ArrayField(
                    name="ANUNIT",
                    array_item_class=Float32Field,
                    array_item_default=0.0,
                    count=self._an_nmr,
                ),
                ArrayField(
                    name="DIGUNIT",
                    array_item_class=UInt32Field,
                    array_item_default=0.0,
                    count=self._dg_nmr,
                ),
                UInt16Field(name="FNOM"),
                UInt16Field(name="CFGCNT"),
            ],
        )

    @property
    def station_name(self) -> str:
        """Get the station name.

        Returns:
            the station name
        """
        return cast("StringFixedLengthField", self["STN"]).value

    @property
    def phasor_names(self) -> list[str]:
        """Get the phasor names.

        Returns:
            the phasor names
        """
        phnams = cast("ArrayField[str]", self["PHNAMS"])
        return [name.value for name in cast(list[StringFixedLengthField], phnams.value)]

    @property
    def analog_names(self) -> list[str]:
        """Get the analog names.

        Returns:
            the analog names
        """
        annams = cast("ArrayField[str]", self["ANNAMS"])
        return [name.value for name in cast(list[StringFixedLengthField], annams.value)]

    @property
    def digital_names(self) -> list[str]:
        """Get the digital names.

        Returns:
            the digital names
        """
        dignams = cast("DIGNAMS", self["DIGNAMS"])
        return [name.value for name in cast(list[StringFixedLengthField], dignams.value)]


class CONFIGURATION1(DictField):
    """Configuration Frame Type 1."""

    def __init__(
        self,
        name: str = "CONFIGURATION1",
        data: dataT = None,
    ) -> None:
        """Create Configuration Frame Type 1.

        Args:
            name: name of field. Defaults to "CONFIGURATION1".
            data: data to be parsed. Defaults to None.
        """
        self._num_pmu = UInt16Field(name="NUM_PMU")
        super().__init__(
            name=name,
            default=[
                SYNC(),
                UInt16Field(name="FRAMESIZE"),
                UInt16Field(name="IDCODE"),
                UInt32Field(name="SOC"),
                UInt32Field(name="FRACSEC"),
                UInt32Field(name="TIME_BASE"),
                self._num_pmu,
                ArrayField[PMU_CONFIGURATION](
                    name="PMU_CONFIGURATIONS",
                    array_item_class=type(PMU_CONFIGURATION),
                    array_item_default=PMU_CONFIGURATION(),
                    count=self._num_pmu,
                ),
                UInt16Field(name="DATA_RATE"),
                CHK(),
            ],
            data=data,
        )

    @property
    def pmu_configs(self) -> list[PMU_CONFIGURATION]:
        """Get pmu configuration list.

        Returns:
            pmu configuration list
        """
        return cast("list[PMU_CONFIGURATION]", self["PMU_CONFIGURATIONS"])

    @property
    def formats(self) -> list[FORMAT]:
        """Get pmu formats.

        Returns:
            pmu formats
        """
        pmu_configs = cast("list[PMU_CONFIGURATION]", self["PMU_CONFIGURATIONS"])
        formats: list[FORMAT] = []
        for pmu_config in pmu_configs:
            fmt = cast("FORMAT", pmu_config["FORMAT"])
            formats.append(fmt)
        return formats

    @property
    def phasor_counts(self) -> list[int]:
        """Get phasor counts.

        Returns:
            phasor counts
        """
        pmu_configs = cast("list[PMU_CONFIGURATION]", self["PMU_CONFIGURATIONS"])
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config["PHNMR"]).value)
        return counts

    @property
    def analog_counts(self) -> list[int]:
        """Get analog counts.

        Returns:
            analog counts
        """
        pmu_configs = cast("list[PMU_CONFIGURATION]", self["PMU_CONFIGURATIONS"])
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config["ANNMR"]).value)
        return counts

    @property
    def digital_counts(self) -> list[int]:
        """Get digital counts.

        Returns:
            digital counts
        """
        pmu_configs = cast("list[PMU_CONFIGURATION]", self["PMU_CONFIGURATIONS"])
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config["DGNMR"]).value)
        return counts


class CONFIGURATION2(CONFIGURATION1):
    """Configuration Frame Type 2."""

    def __init__(
        self,
        name: str = "CONFIGURATION2",
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


class COMMAND(DictField):
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
            name="COMMAND",
            default=[
                SYNC(),
                UInt16Field(name="FRAMESIZE"),
                UInt16Field(name="IDCODE"),
                UInt32Field(name="SOC"),
                UInt32Field(name="FRACSEC"),
                UInt16Field(name="CMD"),
                CHK(),
            ],
            data=data,
        )


class PMU_DATA(DictField):
    """Data field of a Data frame."""

    def __init__(
        self,
        phasor_count: int,
        analog_count: int,
        digital_count: int,
        pmu_format: FORMAT,
        name: str = "PMU_DATA",
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
                self._phasor_class = type(PHASOR_RECTANGULAR_FLOAT)
            else:
                self._phasor_class = type(PHASOR_POLAR_FLOAT)
        else:
            if self._format.coordinates is CoordinateFormatEnum.POLAR:
                self._phasor_class = type(PHASOR_RECTANGULAR_INT)
            else:
                self._phasor_class = type(PHASOR_POLAR_INT)
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
                UInt16Field(name="STAT"),
                ArrayField(
                    name="PHASORS",
                    array_item_class=self._phasor_class,
                    array_item_default=0,
                    count=phasor_count,
                ),
                self._freq_class(name="FREQ"),
                self._freq_class(name="DFREQ"),
                ArrayField(
                    name="ANALOGS",
                    array_item_class=self._analogs_class,
                    array_item_default=0,
                    count=analog_count,
                ),
                ArrayField(
                    name="DIGITALS",
                    array_item_class=UInt16Field,
                    array_item_default=0,
                    count=digital_count,
                ),
            ],
            data=data,
        )

    @property
    def phasors(
        self,
    ) -> list[PHASOR]:
        """Get phasor fields.

        Returns:
            phasor fields
        """
        array = cast("ArrayField[PHASOR]", self["PHASORS"])
        return cast("list[PHASOR]", array.value)


class PMUDataArrayField(ArrayField[PMU_DATA]):
    """PMU data array field."""

    def __init__(
        self,
        name: str,
        phasor_counts: list[int],
        analog_counts: list[int],
        digital_counts: list[int],
        config: CONFIGURATION1 | CONFIGURATION2,
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
            array_item_class=type(PMU_DATA),
            array_item_default=PMU_DATA(phasor_count=0, analog_count=0, digital_count=0, pmu_format=FORMAT()),
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
            f = PMU_DATA(
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


class DATA(DictField):
    """Data parser."""

    def __init__(
        self,
        config: CONFIGURATION1 | CONFIGURATION2,
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
            name="DATA",
            default=[
                SYNC(),
                UInt16Field(name="FRAMESIZE"),
                UInt16Field(name="IDCODE"),
                UInt32Field(name="SOC"),
                UInt32Field(name="FRACSEC"),
                PMUDataArrayField(
                    name="PMU_DATAS",
                    config=self._config,
                    analog_counts=analog_counts,
                    digital_counts=digital_counts,
                    phasor_counts=phasor_counts,
                ),
                CHK(),
            ],
            data=data,
        )

    @property
    def pmus(self) -> list[PMU_DATA]:
        """Get pmus.

        Returns:
            pmus
        """
        pmu_array = cast("PMUDataArrayField", self["PMU_DATAS"])
        return cast("list[PMU_DATA]", pmu_array.value)

    @property
    def summary(self) -> dict[str, dict[str, PHASOR]]:
        """Get summary.

        Returns:
            summary
        """
        summary: dict[str, dict[str, PHASOR]] = {}
        for pmu_idx, pmu_config in enumerate(self._config.pmu_configs):
            pmu_name = pmu_config.station_name
            pmu = self.pmus[pmu_idx]
            summary[pmu_name] = {}
            for phasor_index, phasor_name in enumerate(pmu_config.phasor_names):
                summary[pmu_name][phasor_name] = pmu.phasors[phasor_index]
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
        smry = self.summary
        for pmu_key in smry:
            for phasor_key in smry[pmu_key]:
                s.append(f"{pmu_key}.{phasor_key}:{smry[pmu_key][phasor_key].get_summary(coords=coords,names=names)}")
        return ", ".join(s)

    @property
    def summary_str(self) -> str:
        """Get summary string.

        Returns:
            summary string
        """
        return self.get_summary_str()
