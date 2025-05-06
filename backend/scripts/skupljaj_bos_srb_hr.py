import requests
import json
import os
from bs4 import BeautifulSoup
from langdetect import detect

OUTPUT_PATH = "../data/sirovi/bosanski_sirovi.jsonl"
URLS = [
    "https://bs.wikipedia.org/wiki/Vje%C5%A1ta%C4%8Dka_inteligencija",
    # Dodaj još URL-ova po želji
]

def fetch_text(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    return "\n".join(paragraphs)

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
        for url in URLS:
            print(f"Skrejpujem {url}...")
            text = fetch_text(url)
            lang = detect(text)
            if lang in ["bs", "hr", "sr"]:
                f_out.write(json.dumps({"url": url, "text": text, "lang": lang}, ensure_ascii=False) + "\n")
    print(f"Podaci spremljeni u {OUTPUT_PATH}")

if __name__ == "__main__":
    main()