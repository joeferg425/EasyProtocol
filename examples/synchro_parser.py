from __future__ import annotations

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
    filename = Path(filename).resolve().absolute()
    func = tcp_payload_reader
    config: CONFIGURATION1 | CONFIGURATION2 | None = None
    if udp:
        func = udp_payload_reader
    for packet in func(filename=filename):
        if len(packet) > 2:
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
                        formats=config.formats,
                        phasor_counts=config.phasor_counts,
                        analog_counts=config.analog_counts,
                        digital_counts=config.digital_counts,
                    )
                    print(data)
                except Exception as ex:
                    print(ex)
            else:
                print(hdr)


if __name__ == "__main__":
    # demo(r"C:\Users\joe\Downloads\C37.118_1PMU_TCP.pcap")
    demo(r"C:\Users\joe\Downloads\C37.118_1PMU_UDP.pcap", udp=True)
