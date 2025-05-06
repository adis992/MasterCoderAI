# === DEV Dockerfile (brzi build, bez torch/transformers) ===
FROM python:3.9-slim
WORKDIR /app

# Build argument to select requirements file (default=dev)
ARG REQUIREMENTS=requirements.dev.txt
COPY ${REQUIREMENTS} /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir torch

ENV PYTHONPATH=/app

COPY backend/ /app/

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# === PRODUKCIJA Dockerfile za Ubuntu/Linux s GPU podrškom ===
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
WORKDIR /app

# Instaliraj osnovne dependencyje
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3.10-venv python3-pip git && \
    rm -rf /var/lib/apt/lists/*

# Kopiraj requirements.txt i instaliraj Python dependencyje
ARG REQUIREMENTS=requirements.txt
COPY ${REQUIREMENTS} /app/requirements.txt
RUN python3.10 -m pip install --upgrade pip && \
    python3.10 -m pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app

COPY backend/ /app/

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Ovaj Dockerfile koristi CUDA, cuDNN i torch za GPU na Ubuntu. Nema Windows dependencyja.