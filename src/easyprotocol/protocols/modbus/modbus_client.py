"""Easy Parser modbus client."""
from __future__ import annotations

import logging
import socket
import sys

from easyprotocol.base.utils import hex
from easyprotocol.protocols.modbus.frames import (
    ModbusTCPFrame,
    ModbusTCPReadCoilsRequest,
)
from easyprotocol.protocols.modbus.modbus_transceiver import ModbusTransceiver

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


class ModbusClient(ModbusTransceiver):
    """Modbus client definition."""

    def __init__(
        self,
        ip: str = "127.0.0.1",
        port: int = 502,
        verbose: bool = False,
    ) -> None:
        """Create Modbus client.

        Args:
            ip: address of client. Defaults to "127.0.0.1".
            port: port number of client. Defaults to 502.
            verbose: logging verbosity. Defaults to False.
        """
        super().__init__(logger=LOGGER)
        if verbose is True:
            LOGGER.setLevel(logging.DEBUG)
        self._ip = ip
        self._port = port
        self._bytes_buffer = b""

    def start(
        self,
        ip: str | None = None,
        port: int | None = None,
        timeout: float = 0.5,
        connection_timeout: float = 0.1,
    ) -> None:
        """Start the client.

        Args:
            ip: address of client. Defaults to None.
            port: port number of client. Defaults to None.
            timeout: socket timeout of client. Defaults to 0.5.
            connection_timeout: new socket connection timeout. Defaults to 0.1.
        """
        if not self._inited:
            LOGGER.info("Starting client on socket %s:%s", self._ip, self._port)
            self._inited = True
        self.stop()
        if ip is not None:
            self._ip = ip
        if port is not None:
            self._port = port
        try:
            self._modbus_socket = socket.socket()
            self._modbus_socket.settimeout(connection_timeout)
            self._modbus_socket.connect((self._ip, self._port))
            self._error_counter = 0
            LOGGER.info("Connected to server at %s:%s", self._ip, self._port)
            self._modbus_socket.settimeout(timeout)
        except socket.timeout as ex:
            if self._error_counter == 0:
                LOGGER.error("Failed to connect to socket %s:%s: %s", self._ip, self._port, ex)
            self._error_counter += 1
            self._modbus_socket = None
        except TimeoutError as ex:
            if self._error_counter == 0:
                LOGGER.error("Failed to connect to socket %s:%s: %s", self._ip, self._port, ex)
            self._error_counter += 1
            self._modbus_socket = None
        except OSError as ex:
            if self._error_counter == 0:
                LOGGER.error("Failed to connect to socket %s:%s: %s", self._ip, self._port, ex)
            self._error_counter += 1
            self._modbus_socket = None

    def stop(self) -> None:
        """Stop the modbus client."""
        if self._modbus_socket is not None:
            try:
                self._modbus_socket.shutdown(socket.SHUT_WR)
            except OSError as ex:
                LOGGER.error("Failed to shutdown socket %s:%s: %s", self._ip, self._port, ex)
            try:
                self._modbus_socket.close()
            except OSError as ex:
                LOGGER.error("Failed to close socket %s:%s: %s", self._ip, self._port, ex)
            self._modbus_socket = None

    def send_receive_frame(self, frame: ModbusTCPFrame) -> ModbusTCPFrame | None:
        """Send and receive frames.

        Args:
            frame: frame to send

        Returns:
            response frame or none
        """
        LOGGER.debug("Client: TX: %s (%s)", frame, hex(frame.value_as_bytes))
        if self.send_message(frame=frame):
            rx_frame = self.read_message()
            if rx_frame:
                LOGGER.debug("Client: RX: %s (%s)", rx_frame, hex(rx_frame.value_as_bytes))
            return rx_frame
        return None

    @property
    def _buffer_len(self) -> int:
        return len(self._bytes_buffer)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address", nargs="?", default="127.0.0.1", help="The IP Address of the Modbus server.")
    parser.add_argument("-p", "--port", type=int, default=502, help="The TCP port of the server.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Set flag to see debugging messages.")
    args = parser.parse_args()

    client = ModbusClient(ip=args.ip_address, port=args.port, verbose=args.verbose)
    client.start()
    read_coils = ModbusTCPReadCoilsRequest()
    LOGGER.info(read_coils)
    LOGGER.info(client.send_receive_frame(read_coils))
    client.stop()
