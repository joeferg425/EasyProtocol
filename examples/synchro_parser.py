"""Example of parsing C37.118 synchrophasor frames from a pcap file."""
from __future__ import annotations

import sys
from pathlib import Path

from easyprotocol.pcap import tcp_payload_reader, udp_payload_reader
from easyprotocol.protocols.synchrophasor import (
    COMMAND,
    CONFIGURATION1,
    CONFIGURATION2,
    DATA,
    HEADER,
    FrameTypeEnum,
)


def demo(filename: str | Path, udp: bool = False) -> None:
    """Run a synchrophasor parsing demo on a pcap file.

    Args:
        filename: path to a pcap file
        udp: set true if synchrophasor packets are using UDP for transport. Defaults to False.
    """
    filename = Path(filename).resolve().absolute()
    func = tcp_payload_reader
    config: CONFIGURATION1 | CONFIGURATION2 | None = None
    if udp:
        func = udp_payload_reader
    for packet in func(filename=filename):
        packet_len = len(packet)
        if packet_len > 2:
            hdr = HEADER(data=packet[:2])
            if hdr.frame_type == FrameTypeEnum.CONFIGURATION1:
                try:
                    config = CONFIGURATION1(data=packet)
                    print(config)
                except Exception as ex:
                    print(ex)
            elif hdr.frame_type == FrameTypeEnum.CONFIGURATION2:
                try:
                    config = CONFIGURATION2(data=packet)
                    print(config)
                except Exception as ex:
                    print(ex)
            elif hdr.frame_type == FrameTypeEnum.COMMAND:
                try:
                    command = COMMAND(data=packet)
                    print(command)
                except Exception as ex:
                    print(ex)
            elif hdr.frame_type == FrameTypeEnum.DATA and config is not None:
                try:
                    data = DATA(
                        data=packet,
                        config=config,
                        phasor_counts=config.phasor_counts,
                        analog_counts=config.analog_counts,
                        digital_counts=config.digital_counts,
                    )
                    print(data.summary_str)
                except Exception as ex:
                    print(ex)
            else:
                print(hdr)


if __name__ == "__main__":
    """Replace sys.argv[1] with your filename or pass a pcap file path as a command line argument."""
    demo(sys.argv[1])
