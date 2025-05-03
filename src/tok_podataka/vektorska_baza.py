"""
Ovaj modul implementira funkcionalnosti za rad s vektorskim bazama podataka.
Koristi se za pohranu, pretragu i upravljanje vektorskim reprezentacijama podataka.
"""

# Import potrebnih biblioteka
import faiss
import numpy as np

class VektorskaBaza:
    """
    Klasa za upravljanje vektorskom bazom podataka koristeći FAISS.
    """

    def __init__(self, dimenzija: int, index_file: str = None):
        """
        Inicijalizacija vektorske baze.

        Args:
            dimenzija (int): Dimenzija vektora.
            index_file (str, optional): Putanja do FAISS indeksa za učitavanje. Ako nije specificirano, kreira se novi indeks.
        """
        self.dimenzija = dimenzija
        if index_file and os.path.exists(index_file):
            print(f"Učitavam FAISS indeks iz: {index_file}")
            self.index = faiss.read_index(index_file)
        else:
            print("Kreiram novi FAISS indeks.")
            self.index = faiss.IndexFlatL2(dimenzija)

    def dodaj_vektore(self, vektori: np.ndarray):
        """
        Dodaje vektore u bazu.

        Args:
            vektori (np.ndarray): Numpy niz vektora dimenzije (broj_vektora, dimenzija).
        """
        if vektori.shape[1] != self.dimenzija:
            raise ValueError(f"Dimenzija vektora mora biti {self.dimenzija}, ali je {vektori.shape[1]}.")
        self.index.add(vektori)
        print(f"Dodano {vektori.shape[0]} vektora u bazu.")

    def pretrazi(self, query_vektori: np.ndarray, top_k: int = 5):
        """
        Pretražuje najbliže vektore u bazi.

        Args:
            query_vektori (np.ndarray): Numpy niz upitnih vektora dimenzije (broj_upita, dimenzija).
            top_k (int): Broj najbližih rezultata za povratak.

        Returns:
            tuple: Dva numpy niza - udaljenosti i indeksi najbližih vektora.
        """
        if query_vektori.shape[1] != self.dimenzija:
            raise ValueError(f"Dimenzija upitnih vektora mora biti {self.dimenzija}, ali je {query_vektori.shape[1]}.")
        distances, indices = self.index.search(query_vektori, top_k)
        return distances, indices

    def sacuvaj_indeks(self, file_path: str):
        """
        Sprema FAISS indeks u datoteku.

        Args:
            file_path (str): Putanja do datoteke za spremanje indeksa.
        """
        faiss.write_index(self.index, file_path)
        print(f"Indeks je sačuvan u: {file_path}")

    def broj_vektora(self) -> int:
        """
        Vraća ukupan broj vektora u bazi.

        Returns:
            int: Broj vektora u bazi.
        """
        return self.index.ntotal

# Primjer korištenja
if __name__ == "__main__":
    dimenzija = 128
    baza = VektorskaBaza(dimenzija)

    # Generisanje slučajnih vektora za dodavanje
    vektori = np.random.random((10, dimenzija)).astype('float32')
    baza.dodaj_vektore(vektori)

    # Generisanje slučajnog upita
    query = np.random.random((1, dimenzija)).astype('float32')
    distances, indices = baza.pretrazi(query)
    print("Najbliži vektori:", indices)
    print("Udaljenosti:", distances)

    # Spremanje indeksa
    baza.sacuvaj_indeks("vektorska_baza.index")