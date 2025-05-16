"""
Ovaj modul služi za učitavanje i upravljanje različitim AI modelima.
Možete koristiti ovaj fajl za dinamičko učitavanje modela, provjeru kompatibilnosti,
i inicijalizaciju modela za različite zadatke.

This module is used for loading and managing various AI models.
You can use this file for dynamic model loading, compatibility checking,
and model initialization for different tasks.
"""

# Import potrebnih biblioteka / Import of required libraries
import torch
from transformers import AutoModel, AutoTokenizer
import os

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False

class ModelLoader:
    """
    Klasa za učitavanje i upravljanje AI modelima.
    Class for loading and managing AI models.
    """

    def __init__(self, model_directory: str):
        """
        Inicijalizacija ModelLoader klase.
        Initialization of the ModelLoader class.

        Args:
            model_directory (str): Putanja do direktorija gdje su modeli pohranjeni.
                                   Path to the directory where models are stored.
        """
        self.model_directory = model_directory

    def load_transformer_model(self, model_name: str):
        """
        Učitava pretrenirani transformers model i njegov tokenizator.
        Loads a pretrained transformers model and its tokenizer.

        Args:
            model_name (str): Ime ili putanja do transformers modela.
                             Name or path to the transformers model.

        Returns:
            tuple: Tokenizator i model. / Tokenizer and model.
        """
        print(f"Učitavam transformers model: {model_name}")
        print(f"Loading transformers model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        return tokenizer, model

    def load_custom_model(self, model_file: str):
        """
        Učitava prilagođeni PyTorch model iz datoteke.
        Loads a custom PyTorch model from a file.

        Args:
            model_file (str): Ime datoteke modela. / Model filename.

        Returns:
            torch.nn.Module: Učitani model. / Loaded model.
        """
        model_path = os.path.join(self.model_directory, model_file)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model datoteka nije pronađena: {model_path}")
            # Model file not found: {model_path}

        print(f"Učitavam prilagođeni model iz: {model_path}")
        print(f"Loading custom model from: {model_path}")
        model = torch.load(model_path)
        model.eval()  # Postavlja model u eval mod / Sets model to eval mode
        return model

    def list_available_models(self):
        """
        Vraća listu svih dostupnih modela u direktoriju.
        Returns a list of all available models in the directory.

        Returns:
            list: Lista imena modela. / List of model names.
        """
        if not os.path.exists(self.model_directory):
            raise FileNotFoundError(f"Direktorij modela nije pronađen: {self.model_directory}")
            # Model directory not found: {self.model_directory}

        print(f"Pregledavam dostupne modele u direktoriju: {self.model_directory}")
        print(f"Listing available models in directory: {self.model_directory}")
        return [f for f in os.listdir(self.model_directory) if f.endswith('.pt') or f.endswith('.bin') or f.endswith('.gguf')]

    def load_model_auto(self, model_file: str):
        """
        Automatski bira loader na osnovu ekstenzije modela.
        Automatically selects loader based on model file extension.
        """
        ext = os.path.splitext(model_file)[1].lower()
        if ext == '.gguf':
            if not LLAMA_CPP_AVAILABLE:
                raise ImportError("llama-cpp-python nije instaliran! Instaliraj s 'pip install llama-cpp-python'.")
            model_path = os.path.join(self.model_directory, model_file)
            print(f"Učitavam GGUF model preko llama.cpp: {model_path}")
            return None, Llama(model_path=model_path)
        elif ext in ['.pt', '.bin']:
            return None, self.load_custom_model(model_file)
        else:
            # Pretpostavi transformers
            return self.load_transformer_model(model_file)

# Primjer korištenja / Example usage
if __name__ == "__main__":
    # Zamijenjeno sa stvarnom putanjom direktorija modela
    # Replaced with actual model directory path
    model_dir = "modeli/moj-bot/"

    loader = ModelLoader(model_dir)

    # Prikaz dostupnih modela / Display available models
    dostupni_modeli = loader.list_available_models()
    print("Dostupni modeli / Available models:", dostupni_modeli)

    # Učitavanje transformers modela / Load transformers model
    transformer_model_name = "bert-base-uncased"
    tokenizer, model = loader.load_transformer_model(transformer_model_name)
    print(f"Uspješno učitan transformers model: {transformer_model_name}")
    print(f"Successfully loaded transformers model: {transformer_model_name}")

    # Učitavanje prilagođenog modela / Load custom model
    if dostupni_modeli:
        custom_model = loader.load_custom_model(dostupni_modeli[0])
        print(f"Uspješno učitan prilagođeni model: {dostupni_modeli[0]}")
        print(f"Successfully loaded custom model: {dostupni_modeli[0]}")