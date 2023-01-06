"""Easy Parser modbus server."""
from __future__ import annotations

import logging
import socket

from easyprotocol.protocols.modbus.fields import ModbusFunctionEnum
from easyprotocol.protocols.modbus.frames import (
    ModbusTCPFrame,
    ModbusTCPReadCoilsRequest,
    ModbusTCPReadDiscreteInputsRequest,
)


class ModbusTransceiver:
    """Base class for handling sockets and message send/receive."""

    def __init__(self, logger: logging.Logger) -> None:
        """Create base class for handling sockets and message send/receive.

        Args:
            logger: logger for base class
        """
        self.logger = logger
        self._modbus_socket: socket.socket | None = None
        self._bytes_buffer = b""
        self._error_counter = 0
        self._inited = False

    def start(
        self,
        ip: str | None = None,
        port: int | None = None,
        timeout: float = 0.5,
        connection_timeout: float = 0.1,
    ) -> None:
        """Start socket things.

        Args:
            ip: ip address to use. Defaults to None.
            port: port number to use. Defaults to None.
            timeout: socket timeout. Defaults to 0.5.
            connection_timeout: socket timeout for making connections. Defaults to 0.1.

        Raises:
            NotImplementedError: until implemented
        """
        raise NotImplementedError()

    def read_message(self) -> ModbusTCPFrame | None:
        """Read a message from the socket.

        Returns:
            the parsed message or None
        """
        msg = None
        if self._modbus_socket is not None:
            frame_byte_count = 8
            try:
                if self._buffer_len < frame_byte_count:
                    self._bytes_buffer += self._modbus_socket.recv(frame_byte_count - self._buffer_len)
            except TimeoutError:
                pass
            except OSError:
                pass
            if self._buffer_len >= frame_byte_count:
                header = ModbusTCPFrame(data=self._bytes_buffer[:frame_byte_count])
                if header.functionCode.value == ModbusFunctionEnum.ReadCoils:
                    frame_byte_count = 14
                    try:
                        if self._buffer_len < frame_byte_count:
                            self._bytes_buffer += self._modbus_socket.recv(frame_byte_count - self._buffer_len)
                    except TimeoutError:
                        pass
                    except OSError:
                        pass
                    try:
                        msg = ModbusTCPReadCoilsRequest(data=self._bytes_buffer)
                        self._bytes_buffer = self._bytes_buffer[len(msg.byte_value) :]
                    except Exception as ex:
                        self.logger.debug("Failed to parse %s: %s", ModbusFunctionEnum.ReadCoils, ex)
                if header.functionCode.value == ModbusFunctionEnum.ReadDiscreteInputs:
                    frame_byte_count = 14
                    try:
                        if self._buffer_len < frame_byte_count:
                            self._bytes_buffer += self._modbus_socket.recv(frame_byte_count - self._buffer_len)
                    except TimeoutError:
                        pass
                    except OSError:
                        pass
                    try:
                        msg = ModbusTCPReadDiscreteInputsRequest(data=self._bytes_buffer)
                        self._bytes_buffer = self._bytes_buffer[len(msg.byte_value) :]
                    except Exception as ex:
                        self.logger.debug("Failed to parse %s: %s", ModbusFunctionEnum.ReadDiscreteInputs, ex)
        return msg

    def send_message(self, frame: ModbusTCPFrame) -> bool:
        """Send socket message.

        Args:
            frame: modbus frame to send

        Returns:
            true if send succeeded
        """
        if self._modbus_socket is None:
            self.start()
        frame_bytes = frame.byte_value
        frame_length = len(frame_bytes)
        sent_count = 0
        try:
            if self._modbus_socket is not None:
                sent_count = self._modbus_socket.send(frame_bytes)
        except TimeoutError as ex:
            self.logger.error("Failed to send message: %s", ex)
        except OSError as ex:
            self.logger.error("Failed to send message: %s", ex)
            self._modbus_socket = None
        return sent_count == frame_length

    @property
    def _buffer_len(self) -> int:
        return len(self._bytes_buffer)
