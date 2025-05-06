import os
import torch
from src.ai_engine.model_loader import ModelLoader

PROCESSED_DATA_PATH = "../data/obradeni/github_obradeni.jsonl"
MODEL_DIR = "../models/moj-bot/"
MODEL_NAME = "bert-base-uncased"

# Učitavanje podataka (dummy primjer)
def ucitaj_podatke(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Nema podataka: {path}")
    # TODO: Prava obrada JSONL podataka
    return ["Primjer ulaza", "Drugi primjer"]

def treniraj():
    print("Pokrećem treniranje modela...")
    loader = ModelLoader(MODEL_DIR)
    tokenizer, model = loader.load_transformer_model(MODEL_NAME)
    podaci = ucitaj_podatke(PROCESSED_DATA_PATH)
    # TODO: Prava petlja treniranja
    print(f"Treniram na {len(podaci)} primjera...")
    # Simulacija treniranja
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, "moj-bot.pt"))
    print("Model sačuvan!")

if __name__ == "__main__":
    treniraj()