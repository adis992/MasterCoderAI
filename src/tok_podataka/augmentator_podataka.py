"""
Ovaj modul implementira funkcionalnosti za augmentaciju podataka.
Koristi se za generisanje dodatnih podataka kako bi se poboljšala raznolikost i robusnost modela.
"""

# Import potrebnih biblioteka
from typing import List
import random

class AugmentatorPodataka:
    """
    Klasa za augmentaciju podataka.
    """

    def __init__(self, sinonimi: dict):
        """
        Inicijalizacija AugmentatorPodataka klase.

        Args:
            sinonimi (dict): Rječnik sinonima za zamjenu riječi.
        """
        self.sinonimi = sinonimi

    def zamijeni_sinonime(self, tekst: str) -> str:
        """
        Zamjenjuje riječi u tekstu njihovim sinonimima ako su dostupni.

        Args:
            tekst (str): Ulazni tekst za augmentaciju.

        Returns:
            str: Tekst sa zamijenjenim sinonimima.
        """
        rijeci = tekst.split()
        augmentirani_tekst = [random.choice(self.sinonimi.get(rijec, [rijec])) for rijec in rijeci]
        return " ".join(augmentirani_tekst)

    def dodaj_sumi(self, tekst: str, suma_procenat: float = 0.1) -> str:
        """
        Dodaje slučajnu šum u tekst zamjenom ili dodavanjem znakova.

        Args:
            tekst (str): Ulazni tekst za augmentaciju.
            suma_procenat (float): Procenat znakova koji će biti izmijenjeni.

        Returns:
            str: Tekst sa dodanom šumom.
        """
        tekst_lista = list(tekst)
        broj_izmjena = int(len(tekst_lista) * suma_procenat)

        for _ in range(broj_izmjena):
            indeks = random.randint(0, len(tekst_lista) - 1)
            tekst_lista[indeks] = random.choice("abcdefghijklmnopqrstuvwxyz ")

        return "".join(tekst_lista)

    def augmentiraj_listu(self, tekstovi: List[str], metode: List[str]) -> List[str]:
        """
        Primjenjuje odabrane metode augmentacije na listu tekstova.

        Args:
            tekstovi (List[str]): Lista tekstova za augmentaciju.
            metode (List[str]): Lista metoda augmentacije (npr. "sinonimi", "suma").

        Returns:
            List[str]: Lista augmentiranih tekstova.
        """
        augmentirani_tekstovi = []

        for tekst in tekstovi:
            augmentirani = tekst
            if "sinonimi" in metode:
                augmentirani = self.zamijeni_sinonime(augmentirani)
            if "suma" in metode:
                augmentirani = self.dodaj_sumi(augmentirani)
            augmentirani_tekstovi.append(augmentirani)

        return augmentirani_tekstovi

    def randomiziraj_redoslijed(self, tekstovi: List[str]) -> List[str]:
        """
        Nasumično mijenja redoslijed tekstova u listi.

        Args:
            tekstovi (List[str]): Lista tekstova za randomizaciju.

        Returns:
            List[str]: Lista tekstova u nasumičnom redoslijedu.
        """
        random.shuffle(tekstovi)
        return tekstovi

# Primjer korištenja
if __name__ == "__main__":
    sinonimi = {
        "brz": ["hitar", "okretan"],
        "auto": ["vozilo", "automobil"],
        "lijep": ["zgodan", "privlačan"]
    }

    augmentator = AugmentatorPodataka(sinonimi)

    tekst = "brz auto je lijep"
    print("Originalni tekst:", tekst)

    # Zamjena sinonima
    tekst_sinonimi = augmentator.zamijeni_sinonime(tekst)
    print("Tekst sa sinonimima:", tekst_sinonimi)

    # Dodavanje šuma
    tekst_suma = augmentator.dodaj_sumi(tekst)
    print("Tekst sa šumom:", tekst_suma)

    # Augmentacija liste tekstova
    tekstovi = ["brz auto", "lijep dan"]
    metode = ["sinonimi", "suma"]
    augmentirani_tekstovi = augmentator.augmentiraj_listu(tekstovi, metode)
    print("Augmentirani tekstovi:", augmentirani_tekstovi)