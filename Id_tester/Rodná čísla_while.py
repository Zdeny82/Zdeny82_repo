from rc_modul import mesice_ocistene, pohlaví, den_bez_nuly, jméno_měsíce_dle_jeho_čísla, uprava_roku_narozeni_na_letopocet, limit_počtu_dnů_v_měsíci
from colorama import Fore

# validace rodneho cisla
	# nacteni vsuptu -------------------------- ANO
	# tvar bez lomitka -------------------------- ANO
	# 9 nebo 10 znaku - typ int -------------------------- ANO
	# if 10 znaku then delitelne 11 beze zvyšku int -------------------------- ANO
	# if 9 znaku then rok < 1.1.1954 -------------------------- ANO
	# určení datumu narození -------------------------- ANO
	# prvych 6 čísel -> 3 promenne - rok_narozeni, mesic_narozeni, den_narozeni -------------------------- ANO
	# kalkulace celého roku narození -------------------------- ANO
	# mesic_narozeni a zaroven urcime pohlavi -> skusíme odečíst 20, 50, 70; výsledek porovnáme s intervalem <01,12> -------------------------- ANO
	# vypocet prestupni rok -------------------------- ANO
	# den_narozeni -> odvodime od prestupniho roku a mesice -------------------------- ANO

while True:
    rc_raw = input("Zadej své rodné číslo ve tvaru RRMMDDXXXX, o deseti nebo devíti znacích pro starší rodná čísla: ")
    rc_raw = rc_raw.replace("/", "")

    if len(rc_raw) < 9 or len(rc_raw) > 10:
        print(Fore.RED + "PODMÍNKA 1: nesprávný počet znaků, zadej RČ znovu: " + Fore.RESET)
        continue
    else:
        print("PODMÍNKA 1: platné RČ, počet znaků OK")

    DD = rc_raw[4:6]
    MM = rc_raw[2:4]
    RR = rc_raw[0:2]

    DD = int(DD)
    MM = int(MM)
    RR = int(RR)

    MM_0 = mesice_ocistene(MM)
    RRRR = uprava_roku_narozeni_na_letopocet(rc_raw)
    limit_dnů = limit_počtu_dnů_v_měsíci(MM_0, RRRR)
    den_bez_0 = den_bez_nuly(DD)
    jmeno_mesice = jméno_měsíce_dle_jeho_čísla(MM_0)
    pohl = pohlaví(MM)
    rc_raw_int = int(rc_raw)

    if DD > limit_dnů:
        print(Fore.RED + "PODMÍNKA 2:" + Fore.RESET,
                  f"Nezadali jste platné RČ, měsíc {jmeno_mesice} měl v roce {RRRR} maximálně {limit_dnů} dní")
        continue
    else:
        print(f"PODMÍNKA 2: platné RČ, měsíc {jmeno_mesice} má maximálně {limit_dnů} dní")
        rc_raw_int = int(rc_raw)

        if rc_raw_int % 11 != 0:
            print(Fore.RED + "PODMÍNKA 3:" + Fore.RESET, f"Nezadali jste platné RČ, zadané RČ není dělitelné 11")
            continue
        else:
            print(f"PODMÍNKA 3: platné RČ, zadané RČ je dělitelné 11")

            if RRRR > 2025:
                print(Fore.RED + "PODMÍNKA 4:" + Fore.RESET, f"Nezadali jste platné RČ pro rok 2024")
                continue
            else:
                print(f"PODMÍNKA 4: platné RČ pro rok 2024")
                print(" ")
                print(f"Datum narození dle zadaného RČ je: {den_bez_0}. {jmeno_mesice} {RRRR} ")
                print(f"Dle zadaného RC je pohlaví: {pohl}")

                break

# vyzkoušej:
# před rokem 2000 8625359568
# po roce 2000 0512151234
# test pro 18. století 555124440
# narozen 29. února v přestupný rok 2024 2452292198
# narozen 29. února v nepřestupný rok 2023 TZN. FALSE 2352292198


