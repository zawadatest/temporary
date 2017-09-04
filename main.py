#zakladamy ze na sprzecie jest bootloader i dzialajaca wersja softu ktora mozna aktualizowac do najnowszej
import unittest
import rpdIp
import netsnmp
from general import General
from power import Power
from upgrade import Upgrade


if __name__ == "__main__":
	rpdIp.init()
	unittest.main(verbosity=2)
