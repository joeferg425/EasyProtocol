# flake8:noqa
from __future__ import annotations

import pytest

from easyprotocol.protocols.synchrophasor import (
    FrameTypeEnum,
    SynchrophasorCommandFrame,
    SynchrophasorFrame,
)


class TestSynchrophasor:
    def test_synchrophasor_command_frame(self) -> None:
        data = b"\xaa\x41\x00\x12\x00\xf1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xd7\xd0"
        start = 0xAA
        version = 1
        frame_type = FrameTypeEnum.Command.value
        frame_size = 18
        frame = SynchrophasorCommandFrame(data=data)
        assert isinstance(frame, SynchrophasorFrame)
        assert frame.start == start
        assert frame.version == version
        assert frame.frameType == frame_type
        assert frame.frameSize == frame_size
