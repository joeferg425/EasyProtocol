# flake8:noqa
from __future__ import annotations

from datetime import datetime

import pytest

from easyprotocol.protocols.synchrophasor import (
    CommandEnum,
    CoordinateFormatEnum,
    FrameTypeEnum,
    NominalFrequencyEnum,
    NumberFormatEnum,
    SynchrophasorCommandFrame,
    SynchrophasorConfiguration2Frame,
    SynchrophasorFrame,
    TimeQualityCodeEnum,
    TimeQualityFlags,
)


class TestSynchrophasor:
    def test_synchrophasor_parse_command_frame_send_config2(self) -> None:
        data = b"\xaa\x41\x00\x12\x00\xf1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xd7\xd0"
        start = 0xAA
        version = 1
        frame_type = FrameTypeEnum.Command.value
        sync_bit = False
        frame_size = 18
        id_code = 241
        frame = SynchrophasorCommandFrame(data=data)
        time_quality_flags = TimeQualityFlags(0)
        time_quality_code = TimeQualityCodeEnum.ClockLocked
        fractional_seconds = 0
        command = CommandEnum.SendConfiguration2
        checksum = 0xD7D0
        assert isinstance(frame, SynchrophasorFrame)
        assert frame.start.value == start
        assert frame.version.value == version
        assert frame.frameType.value == frame_type
        assert frame.syncBit.value == sync_bit
        assert frame.frameSize.value == frame_size
        assert frame.idCode.value == id_code
        assert frame.soc.value == datetime.utcfromtimestamp(0)
        assert frame.timeQualityFlags.value == time_quality_flags
        assert frame.timeQualityCode.value == time_quality_code
        assert frame.fractionalSeconds.value == fractional_seconds
        assert frame.command.value == command
        assert frame.checksum.value == checksum

    def test_synchrophasor_create_command_frame_send_config2(self) -> None:
        start = 0xAA
        version = 1
        frame_type = FrameTypeEnum.Command
        sync_bit = False
        frame_size = 18
        id_code = 241
        time_quality_flags = TimeQualityFlags(0)
        time_quality_code = TimeQualityCodeEnum.ClockLocked
        fractional_seconds = 0
        command = CommandEnum.SendConfiguration2
        checksum = 0xD7D0
        frame = SynchrophasorCommandFrame(
            start=start,
            version=version,
            frame_type=frame_type,
            sync_bit=sync_bit,
            frame_size=frame_size,
            id_code=id_code,
            time_stamp=datetime.utcfromtimestamp(0),
            time_quality_flags=time_quality_flags,
            time_quality_code=time_quality_code,
            fractional_seconds=fractional_seconds,
            command=command,
            update_checksum=True,
        )
        assert isinstance(frame, SynchrophasorFrame)
        assert frame.start.value == start
        assert frame.version.value == version
        assert frame.frameType.value == frame_type
        assert frame.syncBit.value == sync_bit
        assert frame.frameSize.value == frame_size
        assert frame.idCode.value == id_code
        assert frame.soc.value == datetime.utcfromtimestamp(0)
        assert frame.timeQualityFlags.value == time_quality_flags
        assert frame.timeQualityCode.value == time_quality_code
        assert frame.fractionalSeconds.value == fractional_seconds
        assert frame.command.value == command
        assert frame.checksum.value == checksum

    def test_synchrophasor_assign_command_frame_send_config2(self) -> None:
        start = 0xAA
        version = 1
        frame_type = FrameTypeEnum.Command
        sync_bit = False
        frame_size = 18
        id_code = 241
        time_quality_flags = TimeQualityFlags(0)
        time_quality_code = TimeQualityCodeEnum.ClockLocked
        fractional_seconds = 0
        command = CommandEnum.SendConfiguration2
        checksum = 0xD7D0
        frame = SynchrophasorCommandFrame(
            start=0,
            version=2,
            frame_type=FrameTypeEnum.Data,
            sync_bit=True,
            frame_size=2,
            id_code=6,
            time_stamp=datetime.utcfromtimestamp(1234),
            time_quality_flags=TimeQualityFlags.LeapSecondAdd,
            time_quality_code=TimeQualityCodeEnum.One,
            fractional_seconds=3,
            command=CommandEnum.DataTransmissionOff,
        )
        assert frame.start != start
        assert frame.version != version
        assert frame.frameType != frame_type
        assert frame.syncBit != sync_bit
        assert frame.frameSize != frame_size
        assert frame.idCode != id_code
        assert frame.soc.value != datetime.utcfromtimestamp(0)
        assert frame.timeQualityFlags != time_quality_flags
        assert frame.timeQualityCode != time_quality_code
        assert frame.fractionalSeconds != fractional_seconds
        assert frame.command != command
        assert frame.checksum != checksum

        frame.start.value = start
        frame.version.value = version
        frame.frameType.value = frame_type
        frame.syncBit.value = sync_bit
        frame.frameSize.value = frame_size
        frame.idCode.value = id_code
        frame.soc.value = datetime.utcfromtimestamp(0)
        frame.timeQualityFlags.value = time_quality_flags
        frame.timeQualityCode.value = time_quality_code
        frame.fractionalSeconds.value = fractional_seconds
        frame.command.value = command
        frame.update_checksum()

        assert isinstance(frame, SynchrophasorFrame)
        assert frame.start.value == start
        assert frame.version.value == version
        assert frame.frameType.value == frame_type
        assert frame.syncBit.value == sync_bit
        assert frame.frameSize.value == frame_size
        assert frame.idCode.value == id_code
        assert frame.soc.value == datetime.utcfromtimestamp(0)
        assert frame.timeQualityFlags.value == time_quality_flags
        assert frame.timeQualityCode.value == time_quality_code
        assert frame.fractionalSeconds.value == fractional_seconds
        assert frame.command.value == command
        assert frame.checksum.value == checksum

    def test_synchrophasor_parse_config2_frame_send_config2(self) -> None:
        data = (
            b"\xaa\x31\x00\x86\x00\xf1\x48\x93\x34\x4a\x00\x19\x99\x9a\x00\xff"
            b"\xff\xff\x00\x01\x42\x6c\x75\x65\x20\x50\x4d\x55\x20\x20\x20\x20"
            b"\x20\x20\x20\x20\x00\xf1\x00\x06\x00\x04\x00\x00\x00\x00\x56\x31"
            b"\x4c\x50\x4d\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x56\x41"
            b"\x4c\x50\x4d\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x56\x42"
            b"\x4c\x50\x4d\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x56\x43"
            b"\x4c\x50\x4d\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x00\x00"
            b"\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x01"
            b"\x00\x59\x00\x32\xc1\xe2"
        )
        start = 0xAA
        version = 1
        frame_type = FrameTypeEnum.Configuration2.value
        sync_bit = False
        frame_size = 134
        id_code = 241
        frame = SynchrophasorConfiguration2Frame(data=data)
        timestamp = datetime(2008, 8, 1, 16, 5, 30)
        time_quality_flags = TimeQualityFlags(0)
        time_quality_code = TimeQualityCodeEnum.ClockLocked
        fractional_seconds = 1677722
        pmu_count = 1
        station_name = "Blue PMU"
        frequency_format = NumberFormatEnum.INT
        phasor_format = NumberFormatEnum.FLOAT
        analog_format = NumberFormatEnum.FLOAT
        coordinate_format = CoordinateFormatEnum.POLAR
        phasor_count = 4
        analog_count = 0
        digital_count = 0
        phasor_name1 = "V1LPM"
        phasor_name2 = "VALPM"
        phasor_name3 = "VBLPM"
        phasor_name4 = "VCLPM"
        phasor_convert1 = 1 * (10**-5)
        phasor_convert2 = 1 * (10**-5)
        phasor_convert3 = 1 * (10**-5)
        phasor_convert4 = 1 * (10**-5)
        nominal_frequency = NominalFrequencyEnum.FiftyHertz
        config_count = 89
        data_rate = 50
        checksum = 0xC1E2
        assert frame.start.value == start
        assert frame.version.value == version
        assert frame.frameType.value == frame_type
        assert frame.syncBit.value == sync_bit
        assert frame.frameSize.value == frame_size
        assert frame.idCode.value == id_code
        assert frame.soc.value == timestamp
        assert frame.soc.value == timestamp
        assert frame.timeQualityFlags.value == time_quality_flags
        assert frame.timeQualityCode.value == time_quality_code
        assert frame.fractionalSeconds.value == fractional_seconds
        assert frame.pmuCount == pmu_count
        assert len(frame.pmuConfigs) == pmu_count
        pmu_config = frame.pmuConfigs[0]
        assert pmu_config.stationName.value_as_string == station_name
        assert pmu_config.idCode.value == id_code
        assert pmu_config.formats.frequencies.value == frequency_format
        assert pmu_config.formats.phasors.value == phasor_format
        assert pmu_config.formats.analogs.value == analog_format
        assert pmu_config.formats.coordinates.value == coordinate_format
        assert pmu_config.phasorCount.value == phasor_count
        assert pmu_config.analogCount.value == analog_count
        assert pmu_config.digitalCount.value == digital_count
        phname1 = pmu_config.phasorNames[0]
        phname2 = pmu_config.phasorNames[1]
        phname3 = pmu_config.phasorNames[2]
        phname4 = pmu_config.phasorNames[3]
        assert phname1 == phasor_name1
        assert phname2 == phasor_name2
        assert phname3 == phasor_name3
        assert phname4 == phasor_name4
        phcvrt1 = pmu_config.phasorUnits[0]
        phcvrt2 = pmu_config.phasorUnits[1]
        phcvrt3 = pmu_config.phasorUnits[2]
        phcvrt4 = pmu_config.phasorUnits[3]
        assert phcvrt1 == phasor_convert1
        assert phcvrt2 == phasor_convert2
        assert phcvrt3 == phasor_convert3
        assert phcvrt4 == phasor_convert4
        assert not pmu_config.analogUnits
        assert not pmu_config.digitalUnits
        assert pmu_config.nominalFrequency.value == nominal_frequency
        assert pmu_config.configurationCount.value == config_count
        assert frame.dataRate.value == data_rate
        assert frame.checksum.value == checksum
