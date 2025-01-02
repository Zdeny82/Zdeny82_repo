
import requests
import csv
import time
import datetime
import matplotlib.pyplot as plt

class Počasí:

    def __init__(self, latitude, longitude, api_key):
        self.latitude = latitude
        self.longitude = longitude
        self.api_key = api_key

    @classmethod
    def ziskej_data_o_pocasi(cls, latitude, longitude, api_key):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&lang=cz&units=metric"
        response = requests.get(url)

        if response.status_code == 200: #response "OK"
            data = response.json() #Funkce json() metody response objektu zpracovává příchozí JSON odpověď a
                # vrací ji jako slovník Pythonu. Takže data proměnná obsahuje slovník s informacemi o počasí.
            teplota = data['main']['temp']

            # Uložení dat do CSV souboru
            with open('data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([latitude, longitude, teplota])
            return data
        else:
            print("ze serveru se nepodařilo načíst data")
            return None

class Teplota(Počasí):

    def __init__(self, latitude, longitude, hodnota):
        super().__init__(latitude, longitude, api_key = None)
        self.hodnota = hodnota
    @classmethod
    def metoda_pro_jedinecne_teploty(cls):
        with open('data.csv', mode='r', newline='') as file_to_read:
            obsah = file_to_read.readlines()

        # Vytvoření prázdné množiny pro jedinečné teploty
        jedinecne_teploty = set()

        # Získání teplot z načtených dat
        for x in obsah:
            hodnoty = x.strip().split(',')
            teplota = float(hodnoty[2])
            jedinecne_teploty.add(teplota)  # Přidání teploty do množiny

        # Konverze množiny na seznam pro další použití
        jedinecne_teploty = list(jedinecne_teploty)
        return jedinecne_teploty

    @classmethod
    def tisk_grafu_teplot(cls):
        teploty = cls.metoda_pro_jedinecne_teploty()

        plt.bar(range(len(teploty)), teploty, color="blue", edgecolor="skyblue") #vytiskne počet prvků a jejich hodnoty
        plt.xlim(-0.5, len(teploty)) #vycentruje osu x, kde zřejmě default šířka sloupce přesahuje hodnotu o 0,5 na obě strany
        plt.ylim(min(teploty) - 25, max(teploty) + 5) #zvýší zobrazovanou škálu osy y o 5
        plt.axhline(0, color="red", linestyle="solid", linewidth=1) #nastavení teploty 0

        # Nastavení označení osy x jako celých čísel
        plt.xticks(range(len(teploty)), range(len(teploty)))

        # Nastavení popisků os
        plt.xlabel("Počet záznamů jedinečných teplot")
        plt.ylabel("Teplota °C")
        plt.title("Graf zaznamenaných teplot programem")

        # Přidání popisků k jednotlivým sloupcům
        for i in range(len(teploty)):
            plt.text(range(len(teploty))[i], teploty[i] + 1, str(teploty[i]), ha='center',color='red')

        # Zobrazení grafu
        plt.show()

    @classmethod
    def maximální_teplota(cls):
        with open('data.csv', mode='r', newline='') as file_to_read:
            obsah = file_to_read.readlines()
            jedinecne_teploty = set(obsah)
            jedinecne_teploty = list(jedinecne_teploty)
            maximální_teplota = max(jedinecne_teploty)
            return jedinecne_teploty, maximální_teplota

class Oblačnost(Počasí):

    def __init__(self, latitude, longitude, description):
        super().__init__(latitude, longitude, api_key=None)
        self.description = description

    def slunicko_nebo_mracek_print(self):
        cloud = "☁"
        sun = "☀"
        if self.description in ["zataženo", "oblačno"]: #stejné jako použití x == y or x == z
            return f"\033[37m{cloud}\033[0m"
        elif self.description == "jasno":
            return f"\033[33m{sun}\033[0m"
        else:
            return f"\033[37m{cloud}\033[0m" + f"\033[33m{sun}\033[0m"

class Vítr(Počasí):

    def __init__(self, latitude, longitude, rychlost_vetru, smer_vetru):
        super().__init__(latitude, longitude, api_key=None)
        self.rychlost_vetru = rychlost_vetru
        self.smer_vetru = smer_vetru

    def zobrazeni_smeru_vetru(self):
        if self.smer_vetru <= 90:
            return f"{self.smer_vetru}° severního směru \033[91m\u2191\033[0m"
        elif self.smer_vetru <= 180:
            smer_vetru = self.smer_vetru - 90
            return f"{smer_vetru}° východního směru \033[94m\u2192\033[0m"
        elif self.smer_vetru <= 270:
            smer_vetru = self.smer_vetru - 180
            return f"{smer_vetru}° jižního směru \033[92m\u2193\033[0m"
        else:
            smer_vetru = self.smer_vetru - 270
            return f"{smer_vetru}° západního směru \033[93m\u2190\033[0m"

class Slunce(Počasí):

    def __init__(self, latitude, longitude, čas_východu, čas_západu):
        super().__init__(latitude, longitude, api_key=None)
        self.čas_východu = čas_východu
        self.čas_západu = čas_západu

    def převod_údajů_na_čitelný_čast(self):
        čas_východu_čitelný = datetime.datetime.fromtimestamp(self.čas_východu).strftime("%H:%M:%S")
        čas_západu_čitelný = datetime.datetime.fromtimestamp(self.čas_západu).strftime("%H:%M:%S")
        return čas_východu_čitelný, čas_západu_čitelný

    def za_jakou_dobu_zapadne_Slunce(self):
        čas_do_západu_sec = self.čas_západu - time.time()
        čas_od_východu_sec = time.time() - self.čas_východu

        return čas_do_západu_sec, čas_od_východu_sec