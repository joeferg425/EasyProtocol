from __future__ import annotations

from pathlib import Path
from typing import Generator

import pyshark

from easyprotocol.base.utils import hex


def tcp_payload_reader(filename: str | Path) -> Generator[bytes, None, None]:
    filename = Path(filename).resolve().absolute()
    fc = pyshark.FileCapture(filename)

    for frame in fc:
        if hasattr(frame, "tcp"):
            packet = frame["tcp"]
            if hasattr(packet, "payload"):
                payload = packet.payload
                yield bytes([int(b, 16) for b in payload.split(":")])


def udp_payload_reader(filename: str | Path) -> Generator[bytes, None, None]:
    filename = Path(filename).resolve().absolute()
    fc = pyshark.FileCapture(filename)
    for frame in fc:
        if hasattr(frame, "udp"):
            packet = frame["udp"]
            if hasattr(packet, "payload"):
                payload = packet.payload
                yield bytes([int(b, 16) for b in payload.split(":")])
