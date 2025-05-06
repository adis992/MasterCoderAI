# Model Prijetnji (Threat Modeling)

## Identifikacija prijetnji

- **Neovlašteni pristup API-ju**: Implementirati autentifikaciju i autorizaciju.

- **SQL injekcije**: Validirati sve ulazne podatke.

- **DoS napadi**: Ograničiti broj zahtjeva po korisniku.

## Mitigacija

- Koristiti HTTPS za šifriranje podataka.

- Implementirati rate limiting.

- Redovno ažurirati zavisnosti kako bi se izbjegle poznate ranjivosti.