"""
Ovaj modul implementira funkcionalnosti za validaciju podataka.
Koristi se za provjeru integriteta, formata i kvaliteta podataka prije obrade ili treniranja modela.
"""

# Import potrebnih biblioteka
from typing import List, Dict, Any
import re

class ValidatorPodataka:
    """
    Klasa za validaciju podataka.
    """

    def __init__(self):
        """
        Inicijalizacija ValidatorPodataka klase.
        """
        pass

    def validiraj_tekst(self, tekst: str) -> bool:
        """
        Provjerava da li je tekst validan (npr. nije prazan, nema zabranjene znakove).

        Args:
            tekst (str): Tekst za validaciju.

        Returns:
            bool: True ako je tekst validan, False inače.
        """
        if not tekst.strip():
            return False
        if re.search(r"[<>\\]", tekst):  # Zabranjeni znakovi
            return False
        return True

    def validiraj_json(self, json_obj: Dict[str, Any], obavezna_polja: List[str]) -> bool:
        """
        Provjerava da li JSON objekt sadrži sva obavezna polja.

        Args:
            json_obj (Dict[str, Any]): JSON objekt za validaciju.
            obavezna_polja (List[str]): Lista obaveznih polja.

        Returns:
            bool: True ako su sva obavezna polja prisutna, False inače.
        """
        for polje in obavezna_polja:
            if polje not in json_obj:
                return False
        return True

    def validiraj_listu(self, lista: List[Any], min_duzina: int = 1) -> bool:
        """
        Provjerava da li lista ispunjava minimalne zahtjeve (npr. minimalna dužina).

        Args:
            lista (List[Any]): Lista za validaciju.
            min_duzina (int): Minimalna dozvoljena dužina liste.

        Returns:
            bool: True ako lista ispunjava zahtjeve, False inače.
        """
        if not isinstance(lista, list):
            return False
        if len(lista) < min_duzina:
            return False
        return True

    def validiraj_duplikate(self, lista: List[Any]) -> bool:
        """
        Provjerava da li lista sadrži duplikate.

        Args:
            lista (List[Any]): Lista za provjeru.

        Returns:
            bool: True ako nema duplikata, False inače.
        """
        return len(lista) == len(set(lista))

# Primjer korištenja
if __name__ == "__main__":
    validator = ValidatorPodataka()

    # Validacija teksta
    tekst = "Ovo je validan tekst."
    print("Validacija teksta:", validator.validiraj_tekst(tekst))

    # Validacija JSON objekta
    json_obj = {"ime": "Test", "godine": 25}
    obavezna_polja = ["ime", "godine"]
    print("Validacija JSON-a:", validator.validiraj_json(json_obj, obavezna_polja))

    # Validacija liste
    lista = [1, 2, 3]
    print("Validacija liste:", validator.validiraj_listu(lista, min_duzina=2))