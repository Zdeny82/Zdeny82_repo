import unittest

api_key = "0b7fb2318e6d5a9470a60a58b919fb2b"
latitude = 49.11 #zeměpisná šířka
longitude = 16.36 #zeměpisná délka

class TestWeatherProgram(unittest.TestCase):
    def test_Počasí_instance(self):
        pocasi = Počasí(latitude, longitude, api_key)
        self.assertIsInstance(pocasi, Počasí)

    def test_Teplota_instance(self):
        teplota = Teplota(49.11, 16.36, "api_key")
        self.assertIsInstance(teplota, Teplota)

    def test_Oblačnost_instance(self):
        oblacnost = Oblačnost(49.11, 16.36, "jasno")
        self.assertIsInstance(oblacnost, Oblačnost)

    def test_Vítr_instance(self):
        vitr = Vítr(49.11, 16.36, 10, 180)
        self.assertIsInstance(vitr, Vítr)

    def test_Slunce_instance(self):
        slunce = Slunce(49.11, 16.36, 1620206100, 1620256800)
        self.assertIsInstance(slunce, Slunce)

if __name__ == "__main__":
    unittest.main()

import pytest
from pocasi_modul import Počasí, Teplota, Oblačnost, Vítr, Slunce

# Definujeme testovací scénáře pomocí parametrize
@pytest.mark.parametrize("latitude, longitude, api_key, ocekavany_vystup", [
    (49.11, 16.36, "0b7fb2318e6d5a9470a60a58b919fb2b", "OK"),
    (100, 100, "0b7fb2318e6d5a9470a60a58b919fb2b", "ze serveru se nepodařilo načíst data"),
])
def test_ziskej_data_o_pocasi(latitude, longitude, api_key, ocekavany_vystup):
    # Voláme testovanou funkci s daným vstupem
    vysledek = Počasí.ziskej_data_o_pocasi(latitude, longitude, api_key)

    # Porovnáváme výsledek s očekávaným výstupem
    if ocekavany_vystup == "OK":
        assert vysledek is not None
    else:
        assert vysledek is None
