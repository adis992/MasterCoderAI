"""
Ovaj modul implementira funkcionalnosti za rad s vektorskim bazama podataka.
Koristi se za pohranu, pretragu i upravljanje vektorskim reprezentacijama podataka.
"""

# Import potrebnih biblioteka
import faiss
import numpy as np

class VectorDB:
    # Klasa za upravljanje vektorskom bazom podataka koristeći FAISS. Class for managing vector DB using FAISS.

    def __init__(self, dimension: int, index_file: str = None):
        # Inicijalizacija VectorDB klase. Initializes VectorDB class.
        self.dimension = dimension
        if index_file and os.path.exists(index_file):
            print(f"Učitavam FAISS indeks iz: {index_file}")
            self.index = faiss.read_index(index_file)
        else:
            print("Kreiram novi FAISS indeks.")
            self.index = faiss.IndexFlatL2(dimension)

    def add_vectors(self, vectors: np.ndarray):
        # Dodaje vektore u bazu. Adds vectors to the database.
        if vectors.shape[1] != self.dimension:
            raise ValueError(f"Dimenzija vektora mora biti {self.dimension}, ali je {vectors.shape[1]}.")
        self.index.add(vectors)
        print(f"Dodano {vectors.shape[0]} vektora u bazu.")

    def search(self, query_vectors: np.ndarray, top_k: int = 5):
        # Pretražuje najbliže vektore. Searches nearest vectors.
        if query_vectors.shape[1] != self.dimension:
            raise ValueError(f"Dimenzija upitnih vektora mora biti {self.dimension}, ali je {query_vectors.shape[1]}.")
        distances, indices = self.index.search(query_vectors, top_k)
        return distances, indices

    def save_index(self, file_path: str):
        # Spremanje FAISS indeksa. Saves FAISS index to file.
        faiss.write_index(self.index, file_path)
        print(f"Indeks je sačuvan u: {file_path}")

    def count_vectors(self) -> int:
        # Broj vektora u bazi. Returns total number of vectors in DB.
        return self.index.ntotal

# Primjer korištenja
if __name__ == "__main__":
    dimension = 128
    db = VectorDB(dimension)

    # Generisanje slučajnih vektora za dodavanje
    vectors = np.random.random((10, dimension)).astype('float32')
    db.add_vectors(vectors)

    # Generisanje slučajnog upita
    query = np.random.random((1, dimension)).astype('float32')
    distances, indices = db.search(query)
    print("Najbliži vektori:", indices)
    print("Udaljenosti:", distances)

    # Spremanje indeksa
    db.save_index("vektorska_baza.index")