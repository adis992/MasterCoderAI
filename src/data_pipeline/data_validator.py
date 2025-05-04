"""
Ovaj modul implementira funkcionalnosti za validaciju podataka.
Koristi se za provjeru integriteta, formata i kvaliteta podataka prije obrade ili treniranja modela.
"""

# Import potrebnih biblioteka
from typing import List, Dict, Any
import re

class DataValidator:
    """
    Klasa za validaciju podataka.
    """

    def __init__(self):
        """
        Inicijalizacija DataValidator klase.
        """
        pass

    def validate_text(self, text: str) -> bool:
        """
        Provjerava da li je tekst validan (npr. nije prazan, nema zabranjene znakove).

        Args:
            text (str): Tekst za validaciju.

        Returns:
            bool: True ako je tekst validan, False inače.
        """
        if not text.strip():
            return False
        if re.search(r"[<>\\]", text):  # Zabranjeni znakovi
            return False
        return True

    def validate_json(self, json_obj: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Provjerava da li JSON objekt sadrži sva obavezna polja.

        Args:
            json_obj (Dict[str, Any]): JSON objekt za validaciju.
            required_fields (List[str]): Lista obaveznih polja.

        Returns:
            bool: True ako su sva obavezna polja prisutna, False inače.
        """
        for field in required_fields:
            if field not in json_obj:
                return False
        return True

    def validate_list(self, lst: List[Any], min_length: int = 1) -> bool:
        """
        Provjerava da li lista ispunjava minimalne zahtjeve (npr. minimalna dužina).

        Args:
            lst (List[Any]): Lista za validaciju.
            min_length (int): Minimalna dozvoljena dužina liste.

        Returns:
            bool: True ako lista ispunjava zahtjeve, False inače.
        """
        if not isinstance(lst, list):
            return False
        if len(lst) < min_length:
            return False
        return True

    def validate_duplicates(self, lst: List[Any]) -> bool:
        """
        Provjerava da li lista sadrži duplikate.

        Args:
            lst (List[Any]): Lista za provjeru.

        Returns:
            bool: True ako nema duplikata, False inače.
        """
        return len(lst) == len(set(lst))

# Primjer korištenja
if __name__ == "__main__":
    validator = DataValidator()

    # Validacija teksta
    tekst = "Ovo je validan tekst."
    print("Validacija teksta:", validator.validate_text(tekst))

    # Validacija JSON objekta
    json_obj = {"ime": "Test", "godine": 25}
    obavezna_polja = ["ime", "godine"]
    print("Validacija JSON-a:", validator.validate_json(json_obj, obavezna_polja))

    # Validacija liste
    lista = [1, 2, 3]
    print("Validacija liste:", validator.validate_list(lista, min_duzina=2))