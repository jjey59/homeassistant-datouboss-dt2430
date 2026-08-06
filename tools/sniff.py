"""
sniff.py

Outil de test de communication pour le DatouBoss DT2430.
Envoie plusieurs commandes et affiche les réponses.
"""

import time
from send import DatouBossSerial
from parser import DatouBossParser


COMMANDS = [
    "QPI",
    "QID",
    "QMOD",
    "QPIGS",
    "QFLAG",
    "QDI",
    "QVFW",
    "QVFW2",
]


def print_header(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main():

    inverter = DatouBossSerial()

    try:

        for cmd in COMMANDS:

            print_header(cmd)

            try:

                response = inverter.send(cmd)

                print("Réponse brute :")
                print(response)

                print()

                print("HEX :")
                print(response.hex(" "))

                print()

                print("ASCII :")
                print(DatouBossParser.clean(response))

                print()

                print("Découpage :")
                print(DatouBossParser.split(response))

            except Exception as e:

                print("Erreur :", e)

            time.sleep(1)

    finally:

        inverter.close()


if __name__ == "__main__":
    main()
