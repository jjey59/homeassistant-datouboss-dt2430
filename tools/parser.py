"""
Parser des réponses du DatouBoss DT2430.
"""

from typing import Dict, List


class DatouBossParser:

    @staticmethod
    def clean(raw: bytes) -> str:
        """
        Transforme une réponse brute en texte.
        """

        if raw is None:
            return ""

        text = raw.decode(errors="ignore")

        return text.strip()

    @staticmethod
    def split(raw: bytes) -> List[str]:
        """
        Découpe une réponse en champs séparés par des espaces.
        """

        return DatouBossParser.clean(raw).split()

    @staticmethod
    def parse_qpi(raw: bytes) -> Dict:
        """
        Exemple :
            PI30
        """

        return {
            "protocol": DatouBossParser.clean(raw)
        }

    @staticmethod
    def parse_qmod(raw: bytes) -> Dict:
        """
        Décode le mode de fonctionnement.
        """

        value = DatouBossParser.clean(raw)

        modes = {
            "P": "Power On",
            "S": "Standby",
            "L": "Line",
            "B": "Battery",
            "F": "Fault",
            "H": "Power Saving"
        }

        return {
            "mode_code": value,
            "mode": modes.get(value, "Unknown")
        }

    @staticmethod
    def parse_qid(raw: bytes) -> Dict:

        return {
            "serial_number": DatouBossParser.clean(raw)
        }

    @staticmethod
    def parse_qpigs(raw: bytes) -> Dict:
        """
        Parser générique.

        Pour le moment on retourne simplement
        tous les champs reçus.
        """

        values = DatouBossParser.split(raw)

        return {
            "raw": DatouBossParser.clean(raw),
            "fields": values
        }
