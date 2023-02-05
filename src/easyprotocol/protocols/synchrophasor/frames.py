"Synchrophasor packet classes."
from __future__ import annotations

from typing import Sequence, cast

from bitarray import bitarray

from easyprotocol.base import ParseFieldDict, dataT
from easyprotocol.base.parse_base import ParseBase
from easyprotocol.base.parse_field_dict import K, T, parseGenericT
from easyprotocol.base.utils import input_to_bytes
from easyprotocol.fields import (
    ArrayField,
    BoolField,
    ChecksumField,
    Float32Field,
    StringField,
    UInt8EnumField,
    UInt8Field,
    UInt16Field,
    UInt32Field,
    UIntField,
)
from easyprotocol.fields.unsigned_int import UIntFieldGeneric
from easyprotocol.protocols.synchrophasor.fields import (
    CHK,
    CHNAMS,
    FORMAT,
    FRAMETYPE,
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


class HEADER(ParseFieldDict):
    def __init__(
        self,
        data: dataT = None,
    ) -> None:
        super().__init__(
            name="Header",
            default=[
                SYNC(),
            ],
            data=data,
        )

    @property
    def frame_type(self) -> FrameTypeEnum:
        sync = cast("SYNC", self["SYNC"])
        frame_type = cast("FRAMETYPE", sync["FRAMETYPE"])
        return frame_type.value


class _CONFIGURATION(ParseFieldDict):
    def __init__(
        self,
        name: str = "PMUConfiguration",
        default: None = None,
        data: dataT = None,
    ) -> None:
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
                CHNAMS(
                    phasor_count=self._ph_nmr,
                    analog_count=self._an_nmr,
                    digital_count=self._dg_nmr,
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


class CONFIGURATION1(ParseFieldDict):
    def __init__(
        self,
        name: str = "CONFIGURATION1",
        data: dataT = None,
    ) -> None:
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
                ArrayField(
                    name="PMUConfigurations",
                    array_item_class=_CONFIGURATION,
                    array_item_default="",
                    count=self._num_pmu,
                ),
                UInt16Field(name="DATA_RATE"),
                CHK(),
            ],
            data=data,
        )

    @property
    def formats(self) -> list[FORMAT]:
        pmu_configs = cast("list[_CONFIGURATION]", self["PMUConfigurations"])
        formats: list[FORMAT] = []
        for pmu_config in pmu_configs:
            fmt = cast("FORMAT", pmu_config["FORMAT"])
            formats.append(fmt)
        return formats

    @property
    def phasor_counts(self) -> list[int]:
        pmu_configs = cast("list[_CONFIGURATION]", self["PMUConfigurations"])
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config["PHNMR"]).value)
        return counts

    @property
    def analog_counts(self) -> list[int]:
        pmu_configs = cast("list[_CONFIGURATION]", self["PMUConfigurations"])
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config["ANNMR"]).value)
        return counts

    @property
    def digital_counts(self) -> list[int]:
        pmu_configs = cast("list[_CONFIGURATION]", self["PMUConfigurations"])
        counts: list[int] = []
        for pmu_config in pmu_configs:
            counts.append(cast("UInt16Field", pmu_config["DGNMR"]).value)
        return counts


class CONFIGURATION2(CONFIGURATION1):
    def __init__(
        self,
        name: str = "CONFIGURATION2",
        data: dataT = None,
    ) -> None:
        super().__init__(
            name=name,
            data=data,
        )


class COMMAND(ParseFieldDict):
    def __init__(
        self,
        data: dataT = None,
    ) -> None:
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


class _PMU_DATA(ParseFieldDict):
    def __init__(
        self,
        phasor_count: int,
        analog_count: int,
        digital_count: int,
        format: FORMAT,
        name: str = "PMU_DATA",
        default: None = None,
        data: dataT = None,
    ) -> None:
        self._format = format
        if self._format.phasors is NumberFormatEnum.FLOAT:
            if self._format.coordinates is CoordinateFormatEnum.POLAR:
                self._phasor_class = PHASOR_RECTANGULAR_FLOAT
            else:
                self._phasor_class = PHASOR_POLAR_FLOAT
        else:
            if self._format.coordinates is CoordinateFormatEnum.POLAR:
                self._phasor_class = PHASOR_RECTANGULAR_INT
            else:
                self._phasor_class = PHASOR_POLAR_INT
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
                CHK(),
            ],
            data=data,
        )


class PMUArrayField(ArrayField[_PMU_DATA]):
    def __init__(
        self,
        name: str,
        phasor_counts: list[int],
        analog_counts: list[int],
        digital_counts: list[int],
        formats: list[FORMAT],
        data: dataT | None = None,
    ) -> None:
        self._phasor_counts = phasor_counts
        self._analog_counts = analog_counts
        self._digital_counts = digital_counts
        self._formats = formats
        super().__init__(
            name,
            count=len(formats),
            array_item_class=_PMU_DATA,
            array_item_default=_PMU_DATA(phasor_count=0, analog_count=0, digital_count=0, format=FORMAT()),
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
        if count is not None:
            for i in range(count):
                f = _PMU_DATA(
                    name=f"#{i}",
                    default=self._array_item_default,
                    phasor_count=self._phasor_counts[i],
                    analog_count=self._analog_counts[i],
                    digital_count=self._digital_counts[i],
                    format=self._formats[i],
                )
                bit_data = f.parse(data=bit_data)
                self._children[f.name] = f
        return bit_data


class DATA(ParseFieldDict):
    def __init__(
        self,
        formats: list[FORMAT],
        phasor_counts: list[int],
        analog_counts: list[int],
        digital_counts: list[int],
        data: dataT = None,
    ) -> None:
        super().__init__(
            name="DATA",
            default=[
                SYNC(),
                UInt16Field(name="FRAMESIZE"),
                UInt16Field(name="IDCODE"),
                UInt32Field(name="SOC"),
                UInt32Field(name="FRACSEC"),
                PMUArrayField(
                    name="PMU_DATA",
                    formats=formats,
                    analog_counts=analog_counts,
                    digital_counts=digital_counts,
                    phasor_counts=phasor_counts,
                ),
                CHK(),
            ],
            data=data,
        )


class DATA_POLAR_FLOAT(ParseFieldDict):
    def __init__(
        self,
        pmu_count: int,
        phasor_counts: list[int],
        analog_counts: list[int],
        digital_counts: list[int],
        data: dataT = None,
    ) -> None:
        super().__init__(
            name="DATA",
            default=[
                SYNC(),
                UInt16Field(name="FRAMESIZE"),
                UInt16Field(name="IDCODE"),
                UInt32Field(name="SOC"),
                UInt32Field(name="FRACSEC"),
                PMUArrayField(
                    name="PMU_DATA",
                    array_item_class=_PMU_DATA_POLAR_FLOAT,
                    array_item_default=None,
                    count=pmu_count,
                    analog_counts=analog_counts,
                    digital_counts=digital_counts,
                    phasor_counts=phasor_counts,
                ),
                CHK(),
            ],
            data=data,
        )


class DATA_RECTANGULAR_INT(ParseFieldDict):
    def __init__(
        self,
        pmu_count: int,
        phasor_counts: list[int],
        analog_counts: list[int],
        digital_counts: list[int],
        data: dataT = None,
    ) -> None:
        super().__init__(
            name="DATA",
            default=[
                SYNC(),
                UInt16Field(name="FRAMESIZE"),
                UInt16Field(name="IDCODE"),
                UInt32Field(name="SOC"),
                UInt32Field(name="FRACSEC"),
                PMUArrayField(
                    name="PMU_DATA",
                    array_item_class=_PMU_DATA_RECTANGULAR_INT,
                    array_item_default=None,
                    count=pmu_count,
                    analog_counts=analog_counts,
                    digital_counts=digital_counts,
                    phasor_counts=phasor_counts,
                ),
                CHK(),
            ],
            data=data,
        )


class DATA_POLAR_INT(ParseFieldDict):
    def __init__(
        self,
        pmu_count: int,
        phasor_counts: list[int],
        analog_counts: list[int],
        digital_counts: list[int],
        data: dataT = None,
    ) -> None:
        super().__init__(
            name="DATA",
            default=[
                SYNC(),
                UInt16Field(name="FRAMESIZE"),
                UInt16Field(name="IDCODE"),
                UInt32Field(name="SOC"),
                UInt32Field(name="FRACSEC"),
                PMUArrayField(
                    name="PMU_DATA",
                    array_item_class=_PMU_DATA_POLAR_INT,
                    array_item_default=None,
                    count=pmu_count,
                    analog_counts=analog_counts,
                    digital_counts=digital_counts,
                    phasor_counts=phasor_counts,
                ),
                CHK(),
            ],
            data=data,
        )
