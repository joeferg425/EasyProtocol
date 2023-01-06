"""Easy Parser modbus server."""
from __future__ import annotations

import logging
import math
import socket
from typing import Generator, cast

from easyprotocol.base.utils import hex
from easyprotocol.protocols.modbus.fields import ModbusFunctionEnum
from easyprotocol.protocols.modbus.frames import (
    ModbusTCPFrame,
    ModbusTCPReadCoilsRequest,
    ModbusTCPReadCoilsResponse,
    ModbusTCPReadDiscreteInputsRequest,
    ModbusTCPReadDiscreteInputsResponse,
)
from easyprotocol.protocols.modbus.modbus_transceiver import ModbusTransceiver

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())


class ModbusServer(ModbusTransceiver):
    """Modbus server definition."""

    def __init__(
        self,
        ip: str = "127.0.0.1",
        port: int = 502,
        verbose: bool = False,
    ) -> None:
        """Create modbus server.

        Args:
            ip: address of server. Defaults to "127.0.0.1".
            port: port number of server. Defaults to 502.
            verbose: logging verbosity. Defaults to False.
        """
        super().__init__(logger=LOGGER)
        if verbose:
            LOGGER.setLevel(logging.DEBUG)
        self._server_ip = ip
        self._server_port = port
        self._client_ip = ""
        self._client_port = 0
        self._server_socket: socket.socket | None = None
        self._bytes_buffer = b""
        self._map: dict[ModbusFunctionEnum, dict[int, dict[int, bool] | dict[int, int] | dict[int, int | bool]]] = {}
        if verbose:
            LOGGER.setLevel(logging.DEBUG)

    def add_mapping(
        self,
        function: ModbusFunctionEnum,
        address: int,
        values: dict[int, bool] | dict[int, int] | dict[int, int | bool],
    ) -> None:
        """Add data to modbus map.

        Args:
            function: function code to add data to
            address: address of server (device) to add data to
            values: data dictionary in the form of {register: data}
        """
        if function not in self._map:
            self._map[function] = {}
        if address not in self._map[function]:
            self._map[function][address] = values
        else:
            self._map[function][address].update(values)  # pyright:ignore[reportGeneralTypeIssues] - this is fine...

    def start(
        self,
        ip: str | None = None,
        port: int | None = None,
        timeout: float = 0.5,
        connection_timeout: float = 0.1,
    ) -> None:
        """Start the modbus server.

        Args:
            ip: address of server. Defaults to None.
            port: port number of server. Defaults to None.
            timeout: socket timeout. Defaults to 0.5.
            connection_timeout: new socket connection timeout. Defaults to 0.1.
        """
        if not self._inited:
            LOGGER.info("Starting server on socket %s:%s", self._server_ip, self._server_port)
            self._inited = True
        if ip is not None:
            self._server_ip = ip
        if port is not None:
            self._server_port = port
        if self._server_socket is None:
            try:
                self._server_socket = socket.socket()
                self._server_socket.bind((self._server_ip, self._server_port))
                self._server_socket.listen()
                LOGGER.info("Server running at %s:%s", self._server_ip, self._server_port)
            except OSError as ex:
                LOGGER.error("Failed to bind server to %s:%s: %s", self._server_ip, self._server_port, ex)
                self._server_socket = None
        if self._server_socket is not None and self._modbus_socket is None:
            try:
                self._server_socket.settimeout(connection_timeout)
                self._modbus_socket, (self._client_ip, self._client_port) = self._server_socket.accept()
                LOGGER.info("Client connected from %s:%s", self._client_ip, self._client_port)
                self._error_counter = 0
                self._modbus_socket.settimeout(timeout)
            except TimeoutError as ex:
                if self._error_counter == 0:
                    LOGGER.error("No client connected to server %s:%s: %s", self._server_ip, self._server_port, ex)
                self._error_counter += 1
            except OSError as ex:
                if self._error_counter == 0:
                    LOGGER.error("No client connected to server %s:%s: %s", self._server_ip, self._server_port, ex)
                self._error_counter += 1

    def stop(
        self,
    ) -> None:
        """Close the server socket (if it is open)."""
        if self._modbus_socket is not None:
            try:
                self._modbus_socket.shutdown(socket.SHUT_WR)
            except OSError as ex:
                LOGGER.error("Failed to close client socket %s:%s: %s", self._client_ip, self._client_port, ex)
            try:
                self._modbus_socket.close()
            except OSError as ex:
                LOGGER.error("Failed to close server socket %s:%s: %s", self._client_ip, self._client_port, ex)
        if self._server_socket is not None:
            try:
                self._server_socket.shutdown(socket.SHUT_WR)
            except OSError as ex:
                LOGGER.error("Failed to close server socket %s:%s: %s", self._server_ip, self._server_port, ex)
            try:
                self._server_socket.close()
            except OSError as ex:
                LOGGER.error("Failed to close server socket %s:%s: %s", self._server_ip, self._server_port, ex)
        self._client_ip = ""
        self._client_port = 0
        self._server_socket = None

    def run(self) -> Generator[tuple[ModbusTCPFrame | None, ModbusTCPFrame | None], None, None]:
        """Run the server forever as a generator.

        Yields:
            tuples of rx/tx pairs. rx or tx can be None
        """
        while True:
            self.start()
            if self._modbus_socket is not None:
                rx_msg, tx_msg = self.receive_and_send()
                if rx_msg is not None:
                    LOGGER.debug("Server: RX: %s (%s)", rx_msg, hex(rx_msg.byte_value))
                if tx_msg is not None:
                    LOGGER.debug("Server: TX: %s (%s)", str(tx_msg), hex(tx_msg.byte_value))
                if rx_msg is not None:
                    yield rx_msg, tx_msg

    def receive_and_send(self) -> tuple[ModbusTCPFrame | None, ModbusTCPFrame | None]:
        """Receive a message and send a reply.

        Returns:
            an rx/tx pair. rx or tx can be None
        """
        msg = self.read_message()
        if msg:
            function = msg.functionCode.value
            if function in self._map:
                if isinstance(msg, ModbusTCPReadCoilsRequest):
                    rc = cast("ModbusTCPReadCoilsRequest", msg)  # pyright:ignore[reportUnnecessaryCast]
                    address = rc.address.value
                    register = rc.register.value
                    count = rc.count.value
                    registers = list(range(register, register + count))
                    if all(reg in self._map[function][address] for reg in registers):
                        values = [bool(self._map[function][address][reg]) for reg in registers]
                        tx = ModbusTCPReadCoilsResponse(
                            address=address,
                            byte_count=math.ceil(count / 8),
                            coil_array=values,
                        )
                        if self.send_message(tx):
                            return msg, tx
                        else:
                            return msg, None
                elif isinstance(msg, ModbusTCPReadDiscreteInputsRequest):
                    rc = cast("ModbusTCPReadDiscreteInputsRequest", msg)  # pyright:ignore[reportUnnecessaryCast]
                    address = rc.address.value
                    register = rc.register.value
                    count = rc.count.value
                    registers = list(range(register, register + count))
                    if all(reg in self._map[function][address] for reg in registers):
                        values = [bool(self._map[function][address][reg]) for reg in registers]
                        tx = ModbusTCPReadDiscreteInputsResponse(
                            address=address,
                            byte_count=math.ceil(count / 8),
                            discrete_input_array=values,
                        )
                        if self.send_message(tx):
                            return msg, tx
                        else:
                            return msg, None
        return None, None

    @property
    def _buffer_len(self) -> int:
        return len(self._bytes_buffer)

    @property
    def server_ip(self) -> str:
        """Get the server ip address.

        Returns:
            the server ip address
        """
        return self._server_ip

    @property
    def server_port(self) -> int:
        """Get the server port number.

        Returns:
            the server port number
        """
        return self._server_port

    @property
    def client_ip(self) -> str | None:
        """Get the client ip address (or None if the client is not connected).

        Returns:
            the client ip address (or None if the client is not connected)
        """
        if self._modbus_socket is not None:
            return self._client_ip
        else:
            return None

    @property
    def client_port(self) -> int | None:
        """Get the client port number (or None if the client is not connected).

        Returns:
            the client port number (or None if the client is not connected)
        """
        if self._modbus_socket is not None:
            return self._client_port
        else:
            return None
