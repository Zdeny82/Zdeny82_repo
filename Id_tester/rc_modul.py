# MODUL METOD PRO VÝPOČTY Z RODNÉHO ČÍSLA
def mesice_ocistene(MM):  # očištěné od přičtených čísel 50 a 70 pro ženy, předává dál i číslo měsíce 13 a vyšší
    # předá dál čísla měsíců bez identifikátoru ženského pohlaví
    # implicitní funkce, pomocná
    if 62 >= MM >= 51:
        return MM - 50
    elif 82 >= MM >= 71:
        return MM - 70
    else:
        return MM  # tady předávám dál i číslo měsíce 13 a vyšší


def pohlaví(MM):
    # zohlední identifikátor ženského pohlaví, jinak předá pohlaví mužské
    # explicitiní funkce, pro print
    if 51 <= MM <= 62:
        return "žena"
    elif 71 <= MM <= 82:
        return "žena"
    else:
        return "muž"


def den_bez_nuly(DD):
    # pokud dvojčíslí DD začíná nulou, předá dál číslo bez nuly
    # explicitiní funkce, pro print
    den_narozeni_string = str(DD)
    if den_narozeni_string[0] == "0":
        den_narozeni_bez_nuly_na_zacatku = DD[1]
        return int(den_narozeni_bez_nuly_na_zacatku)
    else:
        return DD


def jméno_měsíce_dle_jeho_čísla(číslo_měsíce):
    # vstup je výstupem funkce mesice_ocistene. Fce předá místo čísla jméno měsíce, pokud je vstup větší než 12, předá číslo
    # explicitiní funkce, pro print
    tupple_měsíců = (
        "leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen", "září", "říjen", "listopad",
        "prosinec")
    slovník_měsíců = {i + 1: tupple_měsíců[i] for i in range(0, len(tupple_měsíců))}
    if 1 <= číslo_měsíce <= 12:
        název_měsíce = slovník_měsíců.get(číslo_měsíce)
        return název_měsíce
    else:
        return False  # jak bude argument číslo měsíce větší než 12, vyhodí False


def uprava_roku_narozeni_na_letopocet(RRMMDDXXXX):
    # při zadání RC vezme první dvě čísla a přičte k ním zbytek letopočtu a předá jako číslo ve tvaru RRRR
    # explicitiní funkce, pro print
    RR = RRMMDDXXXX[0:2]
    RR = int(RR)

    if len(RRMMDDXXXX) == 10:
        if RR < 25:  # vybíráme z intervalu desetiletí 00 - 20. léta 21.st. (if první_rc_číslo >=0 and první_rc_číslo <= 2:)
            rok_narozeni = RR + 2000
            return rok_narozeni
        elif 54 <= RR <= 99:  # vybíráme z intervalu desetiletí 50 - 90. léta 20.st.
            rok_narozeni = RR + 1900
            return rok_narozeni
        else:
            rok_narozeni = RR + 2000
        return rok_narozeni
    elif len(RRMMDDXXXX) == 9:  # není RC o devítí číslech po roce 1954
        if RR < 53:
            rok_narozeni = RR + 1900
            return rok_narozeni
        else:  # to je pouze hypotéza, že jsou pro lidi narozené v 19. století RC tvořena stejnou logikou
            rok_narozeni = RR + 1800
            return rok_narozeni
    else:
        rok_narozeni = RR + 2000
        return rok_narozeni


def limit_počtu_dnů_v_měsíci(č_měsíce: int, RRRR: int) -> int:
    # argumentem bude vystup fce mesice_ocistene() jako výstup fce výše a fce uprava_roku_narozeni_na_letopocet(),
    # předá limitu počtu dní v daném měsíci
    # implicitní funkce, pomocná

    dlouhé_měsíce = [1, 3, 5, 7, 8, 10, 12]
    krátké_měsíce = [4, 6, 9, 11]
    měsíc_únor = [2]
    if č_měsíce in dlouhé_měsíce:
        return 31  # dní v měsíci
    elif č_měsíce in krátké_měsíce:
        return 30  # dní v měsíci
    elif č_měsíce in měsíc_únor:
        # PODMÍNKA přestupný rok zde může zůstat protože není vylučovací, je to buď a nebo a vždy předá hodnotnu.
        if RRRR % 4 == 0 or (
                RRRR % 100 == 0 and RRRR % 400 == 0):  # PODMÍNKA přetupný rok = je dělitelný 4 a není dělitelný 100, což ho činí přestupným.
            return 29  # dní v měsíci
        else:
            return 28  # dní v měsíci
    else:
        return 31  # pokud argumentem bude číslo větší než 12, rovněž vyhodí False
