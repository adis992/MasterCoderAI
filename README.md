# MasterCoderAI 🤖

MasterCoderAI is a professional AI bot designed to assist with programming tasks, supporting multiple languages including Serbian, Croatian, and Bosnian. It combines industry best practices to enable local model creation from scratch or integration with pre-trained models.

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

- **CPU**: AMD Ryzen 9

- **RAM**: 32 GB

- **GPU**: NVIDIA RTX 3090 (24 GB VRAM) + NVIDIA GTX 1080Ti (11 GB VRAM)

- **Diskovi**: 168 TB (SSD/HDD)

- **OS**: Ubuntu (preko WSL-a na Windowsu)

## 📂 Struktura projekta / Project Structure

Struktura projekta je modularna, s jasnim folderima za svaki dio. Svaki folder ima svoj `README.md` koji objašnjava čemu služi i što sadrži.

📁 **MasterCoderAI**  
├── 📄 **README.md**                           # Ovaj fajl – pregled projekta / Project overview  
├── 📄 **LICENSE**                            # Licenca / Open-source license (e.g., MIT)  
├── 📄 **.gitignore**                         # Ignorira env, logove, podatke / Excludes env, logs, data  
├── 📄 **Makefile**                           # Uobičajeni zadaci / Common tasks (build, test, deploy)  
├── 📄 **zahtjevi.txt / requirements.txt**    # Python zavisnosti / Python dependencies  
├── 📄 **docker-compose.yml**                 # Lokalna okruženja / Local dev and integration environments  
├── 📁 **.github**  
│   └── 📁 **workflows**  
│       ├── 📄 **ci.yml**                     # CI: lint, test, build  
│       └── 📄 **cd.yml**                     # CD: deploy to staging/production  
├── 📁 **arhitektura / architecture**  
│   ├── 📄 **sistem_dijagram.drawio**         # Vizuelni plan / Visual blueprint  
│   └── 📄 **tehnicki_zahtjevi.md**           # Nefunkcionalni zahtjevi / Non-functional requirements  
├── 📁 **podaci / data**  
│   ├── 📁 **sirovi / raw**                   # Neobrađeni podaci / Immutable source data  
│   │   ├── 📄 **github_sirovi.jsonl**        # GitHub kod i komentari / GitHub code and comments  
│   │   ├── 📄 **bosanski_sirovi.jsonl**      # Srb-hr-bos tekstovi / Srb-hr-bos texts  
│   │   └── 📄 **engleski_sirovi.jsonl**      # Engleski tekstovi / English texts  
│   ├── 📁 **obrađeni / processed**           # Očišćeni podaci / Cleaned and versioned outputs  
│   │   ├── 📄 **github_obrađeni.jsonl**      # Očišćeni GitHub podaci / Cleaned GitHub data  
│   │   ├── 📄 **bosanski_obrađeni.jsonl**    # Očišćeni srb-hr-bos podaci / Cleaned Srb-hr-bos data  
│   │   └── 📄 **engleski_obrađeni.jsonl**    # Očišćeni engleski podaci / Cleaned English data  
│   └── 📄 **dvc.yaml**                       # DVC definicije / DVC pipeline definitions  
├── 📁 **src**                                # Sav izvorni kod / All source code  
│   ├── 📁 **ai_motor / ai_engine**           # Učitavanje i logika modela / Model loading, inference  
│   │   ├── 📄 **model_loader.py**            # Dinamičko učitavanje / Dynamic model loading  
│   │   ├── 📄 **prompt_engineer.py**         # Kreiranje promptova / Prompt templating  
│   │   └── 📄 **hibridni_model.py**          # Kombinacija modela / Ensemble models  
│   ├── 📁 **tok_podataka / data_pipeline**   # Obrada podataka / ETL, validation, augmentation  
│   │   ├── 📄 **validator_podataka.py**      # Provjera kvaliteta / Data quality checks  
│   │   ├── 📄 **augmentator_podataka.py**    # Generisanje podataka / Synthetic data generation  
│   │   └── 📄 **vektorska_baza.py**          # Upravljanje embedinzima / Embedding management  
│   ├── 📁 **graf_znanja / knowledge_graph**  # Sistem znanja / Domain knowledge and reasoning  
│   │   └── 📄 **znanje_baza.py**             # Ekspertni sistem / Knowledge base  
│   ├── 📁 **api**                            # FastAPI aplikacija / FastAPI application  
│   │   ├── 📄 **main.py**                    # Glavni API / Main API  
│   │   ├── 📄 **middleware.py**              # Sigurnost / Security and rate limiting  
│   │   └── 📄 **ws_endpoints.py**            # WebSocket podrška / WebSocket support  
│   └── 📁 **bot**                            # Orkiestracija bota / Bot orchestration  
│       ├── 📄 **bot.py**                     # Glavna skripta bota / Main bot script  
│       └── 📄 **konfiguracija.py**           # Postavke / Configuration  
├── 📁 **modeli / models**                    # Trenirani modeli / Trained model artifacts  
│   ├── 📁 **moj-bot / my-bot**               # Tvoj lokalni model / Your local model  
│   ├── 📁 **mlruns**                         # MLflow praćenje / MLflow tracking server data  
│   └── 📄 **registry.yaml**                  # Registar modela / Model registry pointers  
├── 📁 **eksperimenti / experiments**         # Testiranje i optimizacija / Hyperparameter sweeps, ablations  
│   ├── 📁 **optimizacija_hiperparametara / hyperparameter_tuning**  
│   │   ├── 📄 **optuna_tuning.py**           # Optimizacija / Parameter tuning  
│   └── 📁 **studije_analize / ablation_studies**  
│       ├── 📄 **ablation_test.py**           # Analiza modela / Component impact analysis  
├── 📁 **evaluacija / evaluation**            # Testiranje performansi / Benchmark and test reporting  
│   ├── 📁 **benchmark**                      # Skripte za testiranje / Benchmark scripts & data  
│   │   ├── 📄 **benchmark.py**               # Usporedni testovi / Comparative tests  
│   └── 📁 **testovi / test_suites**  
│       ├── 📄 **scenariji_testiranja.py**    # Testiranje scenarija / Scenario-based testing  
├── 📁 **infrastruktura / infra**             # Infrastruktura kao kod / Infrastructure as code  
│   ├── 📁 **terraform**                      # Definicije resursa / Cloud resource definitions  
│   └── 📁 **kubernetes**                     # Helm chartovi / Helm charts & manifests  
├── 📁 **nadzor / monitoring**                # Praćenje / Observability setups  
│   ├── 📁 **prometheus**                     # Konfiguracija / Prometheus configs  
│   │   ├── 📄 **prometheus_conf.yaml**       # Metrike / Metrics  
│   └── 📁 **grafana**                        # Definicije / Dashboard definitions  
│       ├── 📄 **grafana_dashboards**         # Vizualizacija / Visualization  
└── 📁 **skripte / scripts**                  # Utility skripte / Utility and maintenance scripts  
    ├── 📄 **skupljaj_github.py**             # Prikupljanje podataka / Data ingestion  
    ├── 📄 **skupljaj_bosanski.py**           # Srb-hr-bos podaci / Srb-hr-bos data collection  
    ├── 📄 **skupljaj_engleski.py**           # Engleski podaci / English data collection  
    ├── 📄 **obradi_podatke.py**              # Čišćenje podataka / Data cleaning pipeline  
    └── 📄 **treniraj_model.py**              # Treniranje / Entrypoint for training  

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

For questions or suggestions, contact the author on GitHub: [your-username](https://github.com/your-username).

# MasterCoderAI

MasterCoderAI je zbirka Python projekata koji uključuju igre, alate, AI/ML, automatizaciju i još mnogo toga. Projekt je organiziran u modularnu strukturu kako bi se olakšalo razumijevanje i proširenje.

## Struktura projekta

- **arhitektura/**: Dijagrami i tehnički zahtjevi.
- **dokumentacija/**: API specifikacije i modeli prijetnji.
- **eksperimenti/**: Optimizacija hiperparametara i studije analize.
- **evaluacija/**: Benchmarking i test scenariji.
- **gotovi_bot/**: Bot aplikacija s Docker podrškom.
- **infrastruktura/**: Kubernetes i Terraform konfiguracije.
- **modeli/**: Model checkpointovi i MLflow praćenje.
- **nadzor/**: Prometheus i Grafana za monitoring.
- **podaci/**: Sirovi i obrađeni podaci.
- **skripte/**: Utility skripte za obradu podataka i treniranje modela.
- **src/**: Glavni izvorni kod (AI engine, API, bot, itd.).

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