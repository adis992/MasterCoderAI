# Podaci

Ovaj direktorij sadrži sirove i obrađene podatke za projekt MasterCoderAI.

## Sadržaj

- `sirovi/`: Neobrađeni podaci.
- `obradeni/`: Obradjeni podaci.
- `dvc.yaml`: DVC pipeline definicije.

# podaci / Data

Ovaj folder sadrži sve podatke za treniranje i rad AI bota.

## Broj fajlova: 7
- `sirovi/github_sirovi.jsonl`
- `sirovi/bosanski_sirovi.jsonl`
- `sirovi/engleski_sirovi.jsonl`
- `obradeni/github_obradeni.jsonl`
- `obradeni/bosanski_obradeni.jsonl`
- `obradeni/engleski_obradeni.jsonl`
- `dvc.yaml`

## Opis fajlova

1. **sirovi/github_sirovi.jsonl**  
   - **Što radi?** Pohranjuje sirove podatke s GitHub-a (kod i komentari).  
   - **Primjer upotrebe**: Podaci za treniranje modela iz GitHub repozitorija.

2. **sirovi/bosanski_sirovi.jsonl**  
   - **Što radi?** Pohranjuje sirove tekstove na srb-hr-bos jezicima (npr. s foruma, Wikipedije).  
   - **Primjer upotrebe**: Podaci za treniranje modela na srb-hr-bos jezicima.

3. **sirovi/engleski_sirovi.jsonl**  
   - **Što radi?** Pohranjuje sirove tekstove na engleskom (npr. s dokumentacija, Stack Overflow-a).  
   - **Primjer upotrebe**: Podaci za treniranje modela na engleskom jeziku.

4. **obradeni/github_obradeni.jsonl**  
   - **Što radi?** Pohranjuje očišćene GitHub podatke, spremne za treniranje.  
   - **Primjer upotrebe**: Nakon obrade sirovih podataka, koristi se za treniranje.

5. **obradeni/bosanski_obradeni.jsonl**  
   - **Što radi?** Pohranjuje očišćene srb-hr-bos tekstove, spremne za treniranje.  
   - **Primjer upotrebe**: Nakon obrade sirovih podataka, koristi se za treniranje.

6. **obradeni/engleski_obradeni.jsonl**  
   - **Što radi?** Pohranjuje očišćene engleske tekstove, spremne za treniranje.  
   - **Primjer upotrebe**: Nakon obrade sirovih podataka, koristi se za treniranje.

7. **dvc.yaml**  
   - **Što radi?** Definira DVC pipeline za verzioniranje podataka.  
   - **Primjer upotrebe**: Praćenje i upravljanje verzijama podataka.
