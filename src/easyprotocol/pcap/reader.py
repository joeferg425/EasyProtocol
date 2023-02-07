from __future__ import annotations

from pathlib import Path
from typing import Generator

import pyshark

from easyprotocol.base.utils import hex


def tcp_payload_reader(filename: str | Path) -> Generator[bytes, None, None]:
    filename = Path(filename).resolve().absolute()
    fc = pyshark.FileCapture(filename)

    previous: bytes = b""
    for frame in fc:
        if hasattr(frame, "tcp"):
            packet = frame["tcp"]
            if hasattr(packet, "payload"):
                payload = packet.payload
                b = bytes([int(b, 16) for b in payload.split(":")])
                if packet.flags_push == "1":
                    yield previous + b
                    previous = b""
                else:
                    previous += b


def udp_payload_reader(filename: str | Path) -> Generator[bytes, None, None]:
    filename = Path(filename).resolve().absolute()
    fc = pyshark.FileCapture(filename)
    for frame in fc:
        if hasattr(frame, "udp"):
            packet = frame["udp"]
            if hasattr(packet, "payload"):
                payload = packet.payload
                yield bytes([int(b, 16) for b in payload.split(":")])
