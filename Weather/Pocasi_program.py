# Uprav svůj projekt tak, že použiješ zásady OOP a znalosti z 2. pol kurzu
#-----------------------------------------------------------------------------
# vytvoř třídy -- ANO --
# vhodě použij atibuty místo proměných -- ANO --
# nahraď funkce metodami -- ANO --
# použij iterátory -- ANO --
# implementuj čtení - zapisování z do souboru -- ANO --
# importuj další moduly a knihovny -- ANO --
# napiš testy pros svůj kód -- ANO --
# vhodně použij try/except -- ANO --


from pocasi_modul import Počasí, Teplota, Oblačnost, Vítr, Slunce
from colorama import Fore

print(Fore.LIGHTBLUE_EX + "Tento program ti dá aktuální informace o počasí" + Fore.RESET)
api_key = "0b7fb2318e6d5a9470a60a58b919fb2b"

#PROGRAM --------------
latitude = None
longitude = None
api_key = None


while True:

    # Try/Except --------------------------
        try:
            if latitude is None or longitude is None: #dopracovat rozcestník
                latitude = float(input("Zadej zěměpisnou šířku ve formátu float na dvě desetiná čísla od -90.00 do 90.00: "))
                longitude = float(input("Zadej zěměpisnou délku ve formátu float na dvě desetiná čísla od -180.00 do 180.00: "))
                api_key = "0b7fb2318e6d5a9470a60a58b919fb2b"


            else:
                if 90.00 < latitude or -90.00 > latitude:
                    print(Fore.RED + "takové místo na zemi neexistuje, zadej hodnoty znovu nebo zadej: 'konec': " + Fore.RESET)
                    continue
                elif 180.00 < longitude or -180.00 > longitude:
                    print(Fore.RED + "takové místo na zemi neexistuje, zadej hodnoty znovu zadej: 'konec': " + Fore.RESET)
                    continue

            # Provede se program
                volba_2 = input("zadej číslici pro zobrazení informací o počasí: \n \n 1. Teplota \n 2. Oblačnost \n 3. Rychlost větru \n 4. Východ a západ Slunce \n \n 5. Konec programu \n 6. Nové zadání ")
                pocasi_data = Počasí.ziskej_data_o_pocasi(latitude, longitude, api_key) #PRVNÍ A POSLEDNÍ ZAVOLÁNÍ METODY ziskej_data_o_pocasi()
                name = pocasi_data.get('name', 'bez dostupného názvu') #PRO MÍSTO, KTERÉ MÁ NEBO NEMÁ NÁZEV

    # Teplota --------------------------
                if volba_2 == str(1):
                    print("\n", Fore.BLUE + "Teplota: " + Fore.RESET)

                    # Načtení rychlosti větru a směru větru z pocasi_data
                    teplota_v_místě = pocasi_data['main']['temp']

                    # Výstup na obrazovku
                    print(f"Aktuální teplota v místě:, {pocasi_data['name']}, je: {pocasi_data['main']['temp']} °C, "
                          f"Pocitová teplota je, {pocasi_data['main']['feels_like']} °C")
                    volba_2_1 = input("zadej číslici pro zobrazení detailnějších informací o teplotách: "
                                      "\n \n 1. Tisk grafu teplot \n 2. Zaznamenaná maxima ")


        # graf --------------------------
                    if volba_2_1 == str(1):
                        # Výstup na obrazovku
                        #print(Teplota.metoda_pro_jedinecne_teploty)
                        Teplota.tisk_grafu_teplot()

        # maximální teplota --------------------------
                    elif volba_2_1 == str(2):
                        # Výstup na obrazovku
                        print("\n", Fore.GREEN + "Maximální teplota: " + Fore.RESET)
                        print("\n"f" maximální zaznamenaná teplota v databázi je {max(Teplota.metoda_pro_jedinecne_teploty())}")

                        jedinecne_teploty = Teplota.maximální_teplota()

                        # Vyfiltrování pozice v záznamech z data.csv
                        teploty = [(float(x.split(',')[2].strip())) for x in jedinecne_teploty[0]]

                        # Seřazení teplot dle hodnoty
                        seřazené_teploty = sorted(teploty)
                        pozice = seřazené_teploty.index(teplota_v_místě)

                        # Výstup na obrazovku
                        print(f" pozice záznamu aktuální teploty ze všech dat o měření je: {pozice + 1}. pozice "
                              f"z {len(seřazené_teploty)} naměřených teplot")

                    else:
                        # Výstup na obrazovku
                        print("\n" "tato volba není podporovaná")
                        continue

    # Oblačnost --------------------------
                elif volba_2 == str(2):
                    print("\n", Fore.BLUE + "Oblačnost: " + Fore.RESET)

                    # Načtení rychlosti větru a směru větru z pocasi_data
                    description = pocasi_data["weather"][0]["description"]
                    oblačnost_inst = Oblačnost(latitude, longitude, description)

                    # Výstup na obrazovku
                    print(f"Aktuálně v místě: {pocasi_data['name']} je: {oblačnost_inst.description} {oblačnost_inst.slunicko_nebo_mracek_print()}")

    # Rychlost větru --------------------------
                elif volba_2 == str(3):
                    print("\n", Fore.BLUE + "Rychlost větru: " + Fore.RESET)

                    # Načtení rychlosti větru a směru větru z pocasi_data
                    rychlost_vetru = pocasi_data['wind']['speed']
                    smer_vetru = pocasi_data['wind']['deg']
                    vitr_inst = Vítr(latitude, longitude, rychlost_vetru, smer_vetru)

                    # Výstup na obrazovku
                    print(f"Aktuální rychlost větru v místě: {pocasi_data['name']} je: {vitr_inst.rychlost_vetru} km/h , směr větru: {vitr_inst.zobrazeni_smeru_vetru()}")

    # Západ Slunce --------------------------
                elif volba_2 == str(4):
                    print("\n", Fore.BLUE + "Západ Slunce: " + Fore.RESET)

                    # Načtení rychlosti větru a směru větru z pocasi_data
                    čas_východu = pocasi_data['sys']['sunrise']
                    čas_západu = pocasi_data['sys']['sunset']
                    slunce_inst = Slunce(latitude, longitude, čas_východu, čas_západu)

                    čas_východu_čitelný, čas_západu_čitelný = slunce_inst.převod_údajů_na_čitelný_čast()
                    čas_do_západu_sec, čas_od_východu_sec = slunce_inst.za_jakou_dobu_zapadne_Slunce()

                    # Výstup na obrazovku
                    print(f"Slunce v místě: {pocasi_data['name']} vyšlo v {čas_východu_čitelný} a zapadne v {čas_západu_čitelný} místního času")
                    print(f"Slunce zapadne za: {round(čas_do_západu_sec / 3600)} hod. a {round(((čas_do_západu_sec) % 3600) / 60)} min. \U0001F305")
                    print(f"Slunce vyšlo před: {round(čas_od_východu_sec / 3600)} hod. a {round(((čas_od_východu_sec) % 3600) / 60)} min. \U0001F307")

                elif volba_2 == str(5):
                    print(Fore.RED + "program počasí ukončen " + Fore.RESET)
                    break

                elif volba_2 == str(6):
                    print(Fore.RED + "\n""zadej nové hodnoty" + Fore.RESET)
                    latitude = None
                    longitude = None
                    continue

                else:
                    continue

        except ValueError as e:
            print("Chyba při zadávání vstupu:", e)
            continue


#latitude = 49.11 #zeměpisná šířka Brno
#longitude = 16.36 #zeměpisná délka Brno

exit()





