"""Easy Parser modbus client."""
from __future__ import annotations

import logging
import socket

from easyprotocol.base.utils import hex
from easyprotocol.protocols.modbus.frames import ModbusTCPFrame
from easyprotocol.protocols.modbus.modbus_transceiver import ModbusTransceiver

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())


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
        if verbose:
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
        LOGGER.debug("Client: TX: %s (%s)", frame, hex(frame.byte_value))
        if self.send_message(frame=frame):
            rx_frame = self.read_message()
            if rx_frame:
                LOGGER.debug("Client: RX: %s (%s)", rx_frame, hex(rx_frame.byte_value))
            return rx_frame
        return None

    @property
    def _buffer_len(self) -> int:
        return len(self._bytes_buffer)
