# Makefile za MasterCoderAI

# Instalacija zavisnosti
install:
	pip install -r requirements.txt

# Pokretanje skripti za prikupljanje podataka
collect-data:
	python backend/scripts/skupljaj_github.py
	python backend/scripts/skupljaj_bos_srb_hr.py
	python backend/scripts/skupljaj_engleski.py

# Obrada podataka
process-data:
	python backend/scripts/obradi_podatke.py

# Treniranje modela
train:
	python backend/scripts/treniraj_model.py

# Pokretanje bota
run-bot:
	python backend/src/bot/bot.py

# Pokretanje API-ja
run-api:
	uvicorn backend/src/api/main:app --host 0.0.0.0 --port 8000

# Testiranje
test:
	pytest backend/tests/ --cov=backend/src

# Lintiranje koda
lint:
	flake8 backend/src

# Dodavanje linting provjere za sigurnosne ranjivosti
security-check:
	bandit -r src/

# Docker login, build, and push
docker-login:
	@echo "Logging into Docker registry..."
	@docker login -u "$$DOCKER_USERNAME" -p "$$DOCKER_TOKEN"

docker-build:
	@echo "Building Docker image..."
	@docker build -t "$$DOCKER_REGISTRY"/mastercoderai:latest .

docker-push:
	@echo "Pushing Docker image..."
	@docker push "$$DOCKER_REGISTRY"/mastercoderai:latest

# Sve je spremno
all: install collect-data process-data train run-bot run-api

.PHONY: run-webui
run-webui:
	cd frontend/webui; npm install; npm start
