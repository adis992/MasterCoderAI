# Gotovi Bot / Ready Bot

Ovaj folder sadrži gotovog bota spremnog za pokretanje i integraciju.

## Sadržaj

- **bot.py**: Glavna skripta za pokretanje bota.
- **docker-compose.yml**: Konfiguracija za pokretanje bota koristeći Docker.
- **Dockerfile**: Definicija Docker imidža za bota.
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