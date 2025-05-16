# MasterCoderAI 🤖

MasterCoderAI is an all-in-one MLOps project designed to streamline AI development, deployment, and monitoring. This repository is organized as a monorepo with modular components for various stages of the MLOps lifecycle.

## Modules
- **architecture/**: System architecture diagrams and specifications.
- **documentation/**: Detailed documentation, including API specs and threat modeling.
- **data/**: Data ETL processes and DVC pipelines.
- **scripts/**: Helper scripts for data collection, cleaning, and training.
- **src/**: Core project code, including AI engine, data pipeline, and API.
- **tests/**: Unit and integration tests.
- **tools/**: Command-line and helper tools.
- **evaluation/**: Benchmark tests and evaluation scenarios.
- **experiments/**: Hyperparameter tuning and ablation studies.
- **models/**: Trained models and MLflow tracking.
- **monitoring/**: Prometheus and Grafana configurations for observability.
- **webui/**: Front-end React application (chat interface & gallery).

## Features

- **Data Collection**: Scripts to scrape and process data from GitHub, Wikipedia, and other sources.

- **Model Training**: Train your own AI model using the provided pipeline.

- **Bot Interaction**: Chat with the bot via API or WebSocket.

- **Monitoring**: Integrated Prometheus and Grafana for performance monitoring.

- **Data Filtering**: Added functionality to filter data based on minimum text length.

- **Vector Database**: Added method to retrieve the total number of vectors in the database.

- **Bot Configuration**: Enhanced configuration options for log level and API timeout.

## 🖥 Na čemu testiramo / Our Testing Environment

Testiramo na sljedećem računaru:

- **CPU**: AMD Ryzen 9 12/24 core

- **RAM**: 32 GB

- **GPU**: NVIDIA RTX 3090 (24 GB VRAM) x2 + NVIDIA GTX 1080Ti (11 GB VRAM)

- **Diskovi**: 120GB/12 TB (SSD/HDD)

- **OS**: Ubuntu (preko WSL-a na Windowsu)

## 📂 Struktura projekta / Project Structure

```
📁 MasterCoderAI
├── 📄 README.md                 # Pregled projekta
├── 📄 LICENSE                   # Licenca (MIT)
├── 📄 .gitignore                # Ignorirane datoteke
├── 📄 Makefile                  # Uobičajeni zadaci (build, test, deploy)
├── 📄 docker-compose.yml        # Konfiguracija servisa
├── 📄 requirements.txt          # Python zavisnosti
├── 📄 setup.sh                  # Setup script za Ubuntu/Linux
├── 📄 cleanup.sh                # Script za čišćenje cache i log fajlova
│
├── 📁 architecture             # Dizajn sistema i tehnički zahtjevi
├── 📁 data                     # Podaci (sirovi i obrađeni)
├── 📁 documentation            # Dokumentacija (API spec, prijetnje)
├── 📁 evaluation               # Evaluacija i benchmark testovi
├── 📁 experiments              # Eksperimenti i optimizacije
├── 📁 models                   # Trenirani modeli i MLflow
├── 📁 monitoring               # Praćenje (Prometheus, Grafana)
├── 📁 scripts                  # Utility skripte (ETL, training)
├── 📁 src                      # Izvorni kod (API, bot, pipeline)
├── 📁 tests                    # Unit i integracijski testovi
├── 📁 tools                    # Pomoćni alati i generičke skripte
└── 📁 webui                    # React web UI (chat + gallery)
```

## Detailed Installation and Setup Instructions

### Clone the Repository

To get started, clone the repository from GitHub:

```bash
# Clone the repository
git clone https://github.com/your-repo/MasterCoderAI.git
cd MasterCoderAI
```

### Install Dependencies on Ubuntu

Ensure you have Python 3.9+, Docker, and Git installed. Then, follow these steps:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Docker and Docker Compose
sudo apt install docker.io docker-compose -y

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r zahtjevi.txt
```

### Install Dependencies on Windows

For Windows users, follow these steps:

1. Install Python 3.9+ from the [official website](https://www.python.org/downloads/).
2. Install Docker Desktop from [Docker's website](https://www.docker.com/products/docker-desktop/).
3. Install Git from [Git's website](https://git-scm.com/).
4. Open PowerShell or Command Prompt and run the following commands:

```powershell
# Set up a virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install Python dependencies
pip install -r zahtjevi.txt

# Prepare data
make collect-data
make process-data
```

5. Place your AI model in the `modeli\moj-bot\` directory.
6. Use `make train`, `make run-bot`, and `make run-api` to train the model and start services.

### Prepare Data

Run the following commands to collect and process data:

```bash
# Collect raw data
make collect-data

# Process the collected data
make process-data
```

### Add AI Model

Place your AI model in the `modeli/moj-bot/` directory. Ensure the model is compatible with the framework used (e.g., PyTorch or TensorFlow).

```bash
# Example structure
modeli/
  moj-bot/
    my_model.pt
```

### Train the Model

Train your AI model using the provided training script:

```bash
make train
```

### Run the Bot and API

Start the bot and API services:

```bash
# Run the bot
make run-bot

# Run the API
make run-api
```

### Docker Build i Deploy

Za izgradnju i deploy Docker container-a:

```bash
# Login na Docker Registry (već konfigurisan u Makefile i CD pipeline)
make docker-login

# Izgradnja Docker image-a
make docker-build

# Push na Docker Registry
make docker-push

# Pokretanje svih servisa pomoću docker-compose
docker-compose up -d
```

Docker credentials su već konfigurisani u CI/CD pipeline-u i Makefile-u. Za prilagođavanje, izmijeni DOCKER_REGISTRY u .env fajlu.

### Functionalities

MasterCoderAI supports the following functionalities:

- **Data Collection**: Scrape data from GitHub, Wikipedia, and other sources.
- **Data Processing**: Clean and prepare data for training.
- **Model Training**: Train AI models using the provided pipeline.
- **Bot Interaction**: Chat with the bot via API or WebSocket.
- **Monitoring**: Use Prometheus and Grafana for performance monitoring.
- **Secure API**: Includes HTTPS, rate limiting, and trusted host protection.

### Deployment

For local deployment, use Docker Compose:

```bash
# Start services locally
docker-compose up
```

For production deployment, configure the CI/CD pipelines in `.github/workflows`.

### Notes

- Ensure all environment variables are properly set (e.g., `MC_MODEL_NAME`, `MC_MODEL_DIR`).
- For production, restrict CORS and trusted hosts to specific domains.
- Regularly monitor logs and metrics for optimal performance.

## Usage

- **Chat with the bot**: Use the `/chat` endpoint to send messages and receive responses.

- **Monitor performance**: Access Grafana dashboards to visualize metrics.

## Deployment

- Use `docker-compose.yml` for local deployment:

  ```bash
  docker-compose up
  ```

- For production, configure the CI/CD pipelines in `.github/workflows`.

## 📋 Zavisnosti / Dependencies

Zavisnosti su navedene u `zahtjevi.txt`:

- `torch`: Mašinsko učenje i GPU optimizacija / Machine learning and GPU optimization.

- `transformers`: Rad s AI modelima / AI model training and inference.

- `fastapi`, `uvicorn`: Web servis za bota / Web server for the bot.

- `requests`, `beautifulsoup4`: Skrejpovanje podataka / Web scraping.

- `langdetect`: Detekcija jezika / Language detection (Srb-hr-bos, English).

- `gitpython`: Kloniranje GitHub repozitorija / GitHub repository cloning.

- `datasets`: Obrada podataka / Data processing.

- `optuna`, `ray[tune]`: Optimizacija hiperparametara / Hyperparameter optimization.

- `prometheus-client`: Praćenje performansi / Performance monitoring.

- `pydantic`: Validacija podataka / Data validation.

- `sqlalchemy`: Upravljanje bazama / Database management.

- `faiss-cpu`: Vektorska pretraga / Vector search for embeddings.

- `mlflow`: Verzioniranje modela / Model versioning.

- `deepspeed`: Distribuirano treniranje / Distributed training.

- `dvc`, `dvc-s3`: Kontrola verzija podataka / Data version control.

- `pytest`: Testiranje koda / Code testing.

## 🚀 Kako pokrenuti / How to Run

1. **Prikupljanje i obrada podataka**

   Pokreni `make collect-data` i `make process-data` za pripremu podataka.

2. **Treniranje modela**

   Pokreni `make train` za treniranje tvog modela (`moj-bot`).

3. **Pokretanje bota**

   Pokreni `make run-bot` za pokretanje bota lokalno.

4. **Pokretanje API-ja**

   Pokreni `make run-api` za pokretanje web servisa (dostupan na `http://localhost:8000`).

5. **Sve odjednom**

   Pokreni `make all` za kompletan proces od instalacije do pokretanja.

## 📦 Deployment

Ako želiš deployati projekt:

- Koristi `docker-compose.yml` za lokalni deployment:

  ```bash
  docker-compose up
  ```

- Za produkciju, koristi CI/CD pipeline definirane u `.github/workflows`.

## Sigurnosne Mjere

- **HTTPS**: Svi podaci između klijenta i servera su šifrirani.
- **Rate Limiting**: Ograničen broj zahtjeva po korisniku kako bi se spriječili DoS napadi.
- **Trusted Hosts**: Zaštita od Host header napada.

## 📜 Licenca / License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📞 Kontakt / Contact

For questions or suggestions, contact the author on GitHub: [adis922](https://github.com/adis922).

# MasterCoderAI

MasterCoderAI je zbirka Python projekata koji uključuju igre, alate, AI/ML, automatizaciju i još mnogo toga. Projekt je organiziran u modularnu strukturu kako bi se olakšalo razumijevanje i proširenje.

## Struktura projekta

1. **arhitektura/**: Dijagrami i tehnički zahtjevi.
2. **dokumentacija/**: API specifikacije i modeli prijetnji.
3. **eksperimenti/**: Optimizacija hiperparametara i studije analize.
4. **evaluacija/**: Benchmarking i test scenariji.
5. **gotovi_bot/**: Bot aplikacija s Docker podrškom.
6. **infrastruktura/**: Kubernetes i Terraform konfiguracije.
7. **modeli/**: Model checkpointovi i MLflow praćenje.
8. **nadzor/**: Prometheus i Grafana za monitoring.
9. **podaci/**: Sirovi i obrađeni podaci.
10. **skripte/**: Utility skripte za obradu podataka i treniranje modela.
11. **src/**: Glavni izvorni kod (AI engine, API, bot, itd.).

## Instalacija

1. Klonirajte repozitorij:

   ```bash
   git clone https://github.com/adis922/MasterCoderAI.git
   cd MasterCoderAI
   ```

2. Instalirajte zavisnosti:

   ```bash
   pip install -r requirements.txt
   ```

## Pokretanje

- Pokrenite skripte ili module prema potrebi, npr.:

   ```bash
   python src/api/main.py
   ```

## Testiranje

- Pokrenite testove koristeći pytest:

   ```bash
   pytest tests/
   ```

## Autor

Ovaj projekt je kreirao i održava [adis922](https://github.com/adis922).