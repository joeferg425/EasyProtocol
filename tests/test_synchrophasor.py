# flake8:noqa
from __future__ import annotations

from datetime import datetime

import pytest

from easyprotocol.protocols.synchrophasor import (
    CommandEnum,
    FrameTypeEnum,
    SynchrophasorCommandFrame,
    SynchrophasorFrame,
    TimeQualityCodeEnum,
    TimeQualityFlags,
)


class TestSynchrophasor:
    def test_synchrophasor_parse_command_frame(self) -> None:
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

    def test_synchrophasor_create_command_frame(self) -> None:
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

    def test_synchrophasor_assign_command_frame(self) -> None:
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
