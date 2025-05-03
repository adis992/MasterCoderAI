# Gotovi Bot

Ovaj direktorij sadrži implementaciju gotovog bota s Docker podrškom.

## Sadržaj

- `bot.py`: Glavna skripta za bota.
- `Dockerfile`: Konfiguracija za Docker image.
- `docker-compose.yml`: Konfiguracija za pokretanje bota u Docker okruženju.

- **main.py**: Ulazna tačka za aplikaciju bota.
- **requirements.txt**: Lista Python zavisnosti potrebnih za bota.

## Kako koristiti

1. **Pokretanje lokalno**:
   ```bash
   python main.py
   ```

2. **Pokretanje koristeći Docker**:
   ```bash
   docker-compose up
   ```

## Napomene

- Provjerite da su sve zavisnosti instalirane prije pokretanja.
- Docker verzija zahtijeva pravilno konfigurisan Docker i Docker Compose.