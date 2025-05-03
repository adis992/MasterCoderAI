"""
Ovaj modul služi za učitavanje i upravljanje različitim AI modelima.
Možete koristiti ovaj fajl za dinamičko učitavanje modela, provjeru kompatibilnosti,
i inicijalizaciju modela za različite zadatke.
"""

# Import potrebnih biblioteka
import torch
from transformers import AutoModel, AutoTokenizer
import os

class ModelLoader:
    """
    Klasa za učitavanje i upravljanje AI modelima.
    """

    def __init__(self, model_directory: str):
        """
        Inicijalizacija ModelLoader klase.

        Args:
            model_directory (str): Putanja do direktorija gdje su modeli pohranjeni.
        """
        self.model_directory = model_directory

    def load_transformer_model(self, model_name: str):
        """
        Učitava pretrenirani transformers model i njegov tokenizator.

        Args:
            model_name (str): Ime ili putanja do transformers modela.

        Returns:
            tuple: Tokenizator i model.
        """
        print(f"Učitavam transformers model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        return tokenizer, model

    def load_custom_model(self, model_file: str):
        """
        Učitava prilagođeni PyTorch model iz datoteke.

        Args:
            model_file (str): Ime datoteke modela.

        Returns:
            torch.nn.Module: Učitani model.
        """
        model_path = os.path.join(self.model_directory, model_file)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model datoteka nije pronađena: {model_path}")

        print(f"Učitavam prilagođeni model iz: {model_path}")
        model = torch.load(model_path)
        model.eval()  # Postavlja model u eval mod
        return model

    def list_available_models(self):
        """
        Vraća listu svih dostupnih modela u direktoriju.

        Returns:
            list: Lista imena modela.
        """
        if not os.path.exists(self.model_directory):
            raise FileNotFoundError(f"Direktorij modela nije pronađen: {self.model_directory}")

        print(f"Pregledavam dostupne modele u direktoriju: {self.model_directory}")
        return [f for f in os.listdir(self.model_directory) if f.endswith('.pt') or f.endswith('.bin')]

# Primjer korištenja
if __name__ == "__main__":
    # Zamijenjeno sa stvarnom putanjom direktorija modela
    model_dir = "modeli/moj-bot/"

    loader = ModelLoader(model_dir)

    # Prikaz dostupnih modela
    dostupni_modeli = loader.list_available_models()
    print("Dostupni modeli:", dostupni_modeli)

    # Učitavanje transformers modela
    transformer_model_name = "bert-base-uncased"
    tokenizer, model = loader.load_transformer_model(transformer_model_name)
    print(f"Uspješno učitan transformers model: {transformer_model_name}")

    # Učitavanje prilagođenog modela
    if dostupni_modeli:
        custom_model = loader.load_custom_model(dostupni_modeli[0])
        print(f"Uspješno učitan prilagođeni model: {dostupni_modeli[0]}")