"""
Gestionnaire de communication série DatouBoss.

Ce module encapsule pySerial et fournit une interface simple
pour envoyer des commandes et recevoir les réponses.
"""

from __future__ import annotations

import logging
from typing import Optional

import serial


_LOGGER = logging.getLogger(__name__)


class SerialError(Exception):
    """Erreur de communication série."""


class SerialPort:
    """
    Gestionnaire du port série.
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 2400,
        timeout: float = 2.0,
    ):

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self._serial: Optional[serial.Serial] = None

    def open(self):

        if self._serial and self._serial.is_open:
            return

        _LOGGER.info("Ouverture du port %s", self.port)

        self._serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=self.timeout,
        )

    def close(self):

        if self._serial:

            _LOGGER.info("Fermeture du port")

            self._serial.close()

            self._serial = None

    @property
    def connected(self):

        return (
            self._serial is not None
            and self._serial.is_open
        )

    def write(self, data: bytes):

        if not self.connected:
            raise SerialError("Port non ouvert")

        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()

        self._serial.write(data)
        self._serial.flush()

    def read(self) -> bytes:

        if not self.connected:
            raise SerialError("Port non ouvert")

        return self._serial.readline()

    def query(self, data: bytes) -> bytes:

        self.write(data)

        return self.read()
