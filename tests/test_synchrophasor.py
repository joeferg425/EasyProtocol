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
        assert frame.start == start
        assert frame.version == version
        assert frame.frameType == frame_type
        assert frame.syncBit == sync_bit
        assert frame.frameSize == frame_size
        assert frame.idCode == id_code
        assert frame.soc.value == datetime.utcfromtimestamp(0)
        assert frame.timeQualityFlags == time_quality_flags
        assert frame.timeQualityCode == time_quality_code
        assert frame.fractionalSeconds == fractional_seconds
        assert frame.command == command
        assert frame.checksum == checksum

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
        assert frame.start == start
        assert frame.version == version
        assert frame.frameType == frame_type
        assert frame.syncBit == sync_bit
        assert frame.frameSize == frame_size
        assert frame.idCode == id_code
        assert frame.soc.value == datetime.utcfromtimestamp(0)
        assert frame.timeQualityFlags == time_quality_flags
        assert frame.timeQualityCode == time_quality_code
        assert frame.fractionalSeconds == fractional_seconds
        assert frame.command == command
        assert frame.checksum == checksum
