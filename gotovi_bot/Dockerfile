FROM python:3.9-slim

WORKDIR /app

# Instaliraj potrebne sistemske pakete
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Kopiraj requirements.txt i instaliraj zavisnosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj source kod
COPY . .

# Izloži port za FastAPI
EXPOSE 8000

# Pokreni FastAPI aplikaciju
CMD ["python", "main.py"]