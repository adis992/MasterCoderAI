import git
import json
import os
from langdetect import detect

OUTPUT_PATH = "../data/sirovi/github_sirovi.jsonl"
REPOS = [
    "https://github.com/huggingface/transformers.git",
    # Dodaj još repozitorija po želji
]

def extract_code_and_comments(repo_path):
    # Dummy: Vrati primjer podataka
    return [{"file": "example.py", "code": "print('Hello')", "comments": ["Hello"]}]

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
        for repo_url in REPOS:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            local_path = f"tmp/{repo_name}"
            if not os.path.exists(local_path):
                print(f"Kloniram {repo_url}...")
                git.Repo.clone_from(repo_url, local_path)
            data = extract_code_and_comments(local_path)
            for entry in data:
                entry["lang"] = detect(entry["code"])
                f_out.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Podaci spremljeni u {OUTPUT_PATH}")

if __name__ == "__main__":
    main()