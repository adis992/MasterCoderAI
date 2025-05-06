# Data Augmentation Module
# Modul za augmentaciju podataka
from typing import List
import random

class DataAugmenter:
    # Klasa za augmentaciju podataka. Class for data augmentation.

    def __init__(self, synonyms: dict):
        # Inicijalizacija DataAugmenter klase. Initializes DataAugmenter class.
        self.synonyms = synonyms

    def replace_synonyms(self, text: str) -> str:
        # Zamjenjuje riječi sinonimima. Replaces words with their synonyms.
        words = text.split()
        augmented_text = [random.choice(self.synonyms.get(word, [word])) for word in words]
        return " ".join(augmented_text)

    def add_noise(self, text: str, noise_ratio: float = 0.1) -> str:
        # Dodaje šum u tekst. Adds random noise to text.
        text_list = list(text)
        num_changes = int(len(text_list) * noise_ratio)

        for _ in range(num_changes):
            index = random.randint(0, len(text_list) - 1)
            text_list[index] = random.choice("abcdefghijklmnopqrstuvwxyz ")

        return "".join(text_list)

    def augment_list(self, texts: List[str], methods: List[str]) -> List[str]:
        # Primjenjuje metode augmentacije. Applies augmentation methods.
        augmented_texts = []

        for text in texts:
            augmented = text
            if "synonyms" in methods:
                augmented = self.replace_synonyms(augmented)
            if "noise" in methods:
                augmented = self.add_noise(augmented)
            augmented_texts.append(augmented)

        return augmented_texts

    def randomize_order(self, texts: List[str]) -> List[str]:
        # Nasumično mijenja redoslijed. Randomizes order of texts.
        random.shuffle(texts)
        return texts

# Primjer korištenja
if __name__ == "__main__":
    synonyms = {
        "brz": ["hitar", "okretan"],
        "auto": ["vozilo", "automobil"],
        "lijep": ["zgodan", "privlačan"]
    }

    augmenter = DataAugmenter(synonyms)

    text = "brz auto je lijep"
    print("Originalni tekst:", text)

    # Zamjena sinonima
    text_synonyms = augmenter.replace_synonyms(text)
    print("Tekst sa sinonimima:", text_synonyms)

    # Dodavanje šuma
    text_noise = augmenter.add_noise(text)
    print("Tekst sa šumom:", text_noise)

    # Augmentacija liste tekstova
    texts = ["brz auto", "lijep dan"]
    methods = ["synonyms", "noise"]
    augmented_texts = augmenter.augment_list(texts, methods)
    print("Augmentirani tekstovi:", augmented_texts)