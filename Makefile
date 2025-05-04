# Makefile za MasterCoderAI

# Instalacija zavisnosti
install:
	pip install -r zahtjevi.txt

# Pokretanje skripti za prikupljanje podataka
collect-data:
	python skripte/skupljaj_github.py
	python skripte/skupljaj_bos_srb_hr.py
	python skripte/skupljaj_engleski.py

# Obrada podataka
process-data:
	python skripte/obradi_podatke.py

# Treniranje modela
train:
	python skripte/treniraj_model.py

# Pokretanje bota
run-bot:
	python src/bot/bot.py

# Pokretanje API-ja
run-api:
	uvicorn src/api/main:app --host 0.0.0.0 --port 8000

# Testiranje
test:
	pytest tests/ --cov=src

# Lintiranje koda
lint:
	flake8 src

# Dodavanje linting provjere za sigurnosne ranjivosti
security-check:
	bandit -r src/

# Docker login, build, and push
docker-login:
	@echo "Logging into Docker registry..."
	@echo "dckr_pat_hRWZ0euTClOA7MUwC8gcB6xdMU4" | docker login -u "adis1992" --password-stdin

docker-build:
	@echo "Building Docker image..."
	@docker build -t "$$DOCKER_REGISTRY"/mastercoderai:latest .

docker-push:
	@echo "Pushing Docker image..."
	@docker push "$$DOCKER_REGISTRY"/mastercoderai:latest

# Sve je spremno
all: install collect-data process-data train run-bot run-api
