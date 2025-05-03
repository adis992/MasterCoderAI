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
	pytest evaluacija/testovi

# Lintiranje koda
lint:
	flake8 src

# Dodavanje linting provjere za sigurnosne ranjivosti
security-check:
	bandit -r src/

# Sve je spremno
all: install collect-data process-data train run-bot run-api
