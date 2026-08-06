"""
CRC-CCITT (XMODEM) pour les onduleurs DatouBoss / Voltronic.

Ce module permet :
- de calculer le CRC d'une commande
- d'ajouter le CRC à une commande
- d'obtenir une trame prête à être envoyée
"""

from typing import Union


POLYNOMIAL = 0x1021


def crc16(data: Union[str, bytes]) -> int:
    """
    Calcule le CRC16-CCITT (XMODEM).
    """

    if isinstance(data, str):
        data = data.encode("ascii")

    crc = 0

    for byte in data:
        crc ^= (byte << 8)

        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ POLYNOMIAL) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF

    return crc


def crc_bytes(data: Union[str, bytes]) -> bytes:
    """
    Retourne le CRC sous forme de deux octets.
    """

    value = crc16(data)

    return bytes([
        (value >> 8) & 0xFF,
        value & 0xFF
    ])


def build_command(command: str) -> bytes:
    """
    Construit une commande complète :

        COMMANDE + CRC + CR

    Exemple :

        b"QPI\\xbe\\xac\\r"
    """

    command = command.strip()

    frame = command.encode("ascii")
    frame += crc_bytes(command)
    frame += b"\r"

    return frame


if __name__ == "__main__":

    tests = [
        "QPI",
        "QMOD",
        "QPIGS",
        "QID",
    ]

    for cmd in tests:
        packet = build_command(cmd)

        print("--------------------------------")
        print("Commande :", cmd)
        print("CRC :", crc16(cmd))
        print("Trame :", packet.hex(" "))
