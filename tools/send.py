"""
Envoi de commandes série vers un onduleur DatouBoss DT2430.
"""

import serial

from crc import build_command


class DatouBossSerial:

    def __init__(
        self,
        port="/dev/ttyUSB0",
        baudrate=2400,
        timeout=2
    ):

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=self.timeout,
        )

    def send(self, command):

        packet = build_command(command)

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.ser.write(packet)
        self.ser.flush()

        answer = self.ser.readline()

        return answer

    def close(self):

        if self.ser.is_open:
            self.ser.close()


if __name__ == "__main__":

    inverter = DatouBossSerial()

    commands = [
        "QPI",
        "QMOD",
        "QPIGS",
        "QID"
    ]

    for cmd in commands:

        print("----------------------------------")
        print("Commande :", cmd)

        try:
            response = inverter.send(cmd)

            print("Réponse brute :", response)
            print("HEX :", response.hex(" "))

        except Exception as e:

            print("Erreur :", e)

    inverter.close()
