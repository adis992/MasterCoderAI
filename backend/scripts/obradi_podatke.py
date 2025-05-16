import json
import os

RAW_PATHS = [
    "../data/sirovi/github_sirovi.jsonl",
    "../data/sirovi/bosanski_sirovi.jsonl",
    "../data/sirovi/engleski_sirovi.jsonl",
]
PROCESSED_PATHS = [
    "../data/obradeni/github_obradeni.jsonl",
    "../data/obradeni/bosanski_obradeni.jsonl",
    "../data/obradeni/engleski_obradeni.jsonl",
]

def clean_text(text):
    # Ukloni nepotrebne znakove, whitespace, itd.
    return text.strip().replace("\n", " ")

def filtriraj_podatke(data, min_duzina=10):
    """
    Filtrira podatke na osnovu minimalne dužine teksta.

    Args:
        data (list): Lista podataka za filtriranje.
        min_duzina (int): Minimalna dozvoljena dužina teksta.

    Returns:
        list: Filtrirani podaci.
    """
    return [item for item in data if len(item.get("text", "")) >= min_duzina]

def process_file(raw_path, processed_path):
    if not os.path.exists(raw_path):
        print(f"Nema fajla: {raw_path}")
        return
    with open(raw_path, "r", encoding="utf-8") as f_in, open(processed_path, "w", encoding="utf-8") as f_out:
        for line in f_in:
            try:
                data = json.loads(line)
                if "text" in data:
                    data["text"] = clean_text(data["text"])
                f_out.write(json.dumps(data, ensure_ascii=False) + "\n")
            except Exception as e:
                print(f"Greska u {raw_path}: {e}")
    print(f"Obrađeni podaci spremljeni u {processed_path}")

def main():
    for raw, processed in zip(RAW_PATHS, PROCESSED_PATHS):
        process_file(raw, processed)

if __name__ == "__main__":
    main()