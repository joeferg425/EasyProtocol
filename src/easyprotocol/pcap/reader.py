"""A pcap reader for the easy protocol library."""
from __future__ import annotations

from pathlib import Path
from typing import Generator, cast

from pyshark import FileCapture
from pyshark.packet.packet import Packet


def tcp_pcap_reader(filename: str | Path) -> Generator[bytes, None, None]:
    """Read a pcap file and returns each TCP payload for parsing.

    Args:
        filename: pcap file name

    Yields:
        TCP data bytes from each frame
    """
    filename = Path(filename).resolve().absolute()
    fc = FileCapture(filename)
    previous: bytes = b""

    for frame in fc:  # pyright:ignore[reportUnknownVariableType]
        frame = cast("Packet", frame)
        if hasattr(frame, "tcp"):
            packet = cast("Packet", frame["tcp"])
            if hasattr(packet, "payload"):
                payload = cast("str", packet.payload)  # pyright:ignore[reportUnknownMemberType]
                b = bytes([int(b, 16) for b in payload.split(":")])
                push = "0"
                if hasattr(packet, "flags_push"):
                    push = cast("str", packet.flags_push)  # pyright:ignore[reportUnknownMemberType]
                if push == "1":
                    yield previous + b
                    previous = b""
                else:
                    previous += b


def udp_payload_reader(filename: str | Path) -> Generator[bytes, None, None]:
    """Read a pcap file and returns each UDP payload for parsing.

    Args:
        filename: pcap file name

    Yields:
        UDP data bytes from each frame
    """
    filename = Path(filename).resolve().absolute()
    fc = FileCapture(filename)
    for frame in fc:  # pyright:ignore[reportUnknownVariableType]
        frame = cast("Packet", frame)
        if hasattr(frame, "udp"):
            packet = cast("Packet", frame["udp"])
            if hasattr(packet, "payload"):
                payload = cast("str", packet.payload)  # pyright:ignore[reportUnknownMemberType]
                yield bytes([int(b, 16) for b in payload.split(":")])
