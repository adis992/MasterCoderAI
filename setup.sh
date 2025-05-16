#!/bin/bash
# MasterCoderAI - Setup Script za Ubuntu/Linux
# Instalira sve potrebne zavisnosti i priprema projekat za rad

# Postavi boje za bolji prikaz
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== MasterCoderAI Setup Script =====${NC}"
echo -e "${YELLOW}Ovaj script će instalirati sve potrebne zavisnosti i pripremiti projekat za rad.${NC}"
echo -e "${YELLOW}This script will install all necessary dependencies and prepare the project.${NC}"

# Provjeri Ubuntu/Linux verziju
echo -e "\n${GREEN}Provjeravam Ubuntu verziju...${NC}"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
    echo -e "${YELLOW}Detektovan OS: $OS $VER${NC}"
else
    echo -e "${RED}Nepoznat operativni sistem. Nastavljam, ali neke komande možda neće raditi.${NC}"
fi

# Instaliraj sistemske zavisnosti
echo -e "\n${GREEN}Instaliram sistemske zavisnosti...${NC}"
sudo apt update
sudo apt install -y python3-pip python3-venv build-essential libffi-dev python3-dev

# Kreiraj virtualno okruženje
echo -e "\n${GREEN}Kreiram virtualno okruženje...${NC}"
python3 -m venv venv
source venv/bin/activate

# Nadogradi pip, setuptools i wheel
echo -e "\n${GREEN}Nadograđujem pip, setuptools i wheel...${NC}"
pip install --upgrade pip setuptools wheel

# Instaliraj Python zavisnosti
echo -e "\n${GREEN}Instaliram Python zavisnosti...${NC}"
pip install -r requirements.txt

# Pripremi .env datoteku
echo -e "\n${GREEN}Pripremam .env datoteku...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}Kopiram .env.example u .env${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Molimo vas da uredite .env datoteku i postavite prave vrijednosti.${NC}"
    echo -e "${YELLOW}Please edit the .env file and set the correct values.${NC}"
else
    echo -e "${YELLOW}.env već postoji, preskačem...${NC}"
fi

# Instaliraj Docker ako još nije instaliran
echo -e "\n${GREEN}Provjeravam Docker instalaciju...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker nije pronađen. Instaliram Docker...${NC}"
    sudo apt update
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install -y docker-ce docker-compose
    sudo usermod -aG docker $USER
    echo -e "${YELLOW}Docker je instaliran. Molimo vas da se odjavite i ponovo prijavite da bi promjene imale efekta.${NC}"
    echo -e "${YELLOW}Docker installed. Please log out and log back in for changes to take effect.${NC}"
else
    echo -e "${YELLOW}Docker je već instaliran.${NC}"
fi

# Provjeri da li model postoji u modeli/
echo -e "\n${GREEN}Provjeravam postojanje modela...${NC}"
MODEL_PATH=$(grep MODEL_PATH .env | cut -d '=' -f2)
if [ -z "$MODEL_PATH" ]; then
    MODEL_PATH="modeli/gguf-model.bin"  # default value
fi

if [ ! -f "$MODEL_PATH" ]; then
    echo -e "${RED}GGUF model nije pronađen na putanji: $MODEL_PATH${NC}"
    echo -e "${YELLOW}Postavite MODEL_PATH u .env datoteci na ispravnu putanju do vašeg GGUF modela.${NC}"
    echo -e "${YELLOW}Set MODEL_PATH in the .env file to the correct path to your GGUF model.${NC}"
    mkdir -p "$(dirname "$MODEL_PATH")"
else
    echo -e "${YELLOW}Model pronađen na: $MODEL_PATH${NC}"
fi

# Završi setup
echo -e "\n${GREEN}====== Setup završen! ======${NC}"
echo -e "${YELLOW}Da pokrenete projekat, koristite sljedeće komande:${NC}"
echo -e "${YELLOW}To run the project, use these commands:${NC}"
echo -e "${GREEN}source venv/bin/activate${NC} - Aktivira virtualno okruženje / Activates virtual environment"
echo -e "${GREEN}make test${NC} - Pokreće testove / Runs tests"
echo -e "${GREEN}make run-bot${NC} - Pokreće bota / Runs the bot"
echo -e "${GREEN}make run-api${NC} - Pokreće API server / Runs the API server"
echo -e "${GREEN}make docker-build${NC} - Gradi Docker image / Builds Docker image"
echo -e "${GREEN}docker-compose up${NC} - Pokreće sve servise kroz Docker / Runs all services through Docker"
echo -e "\n${YELLOW}Hvala što koristite MasterCoderAI!${NC}"
echo -e "${YELLOW}Thank you for using MasterCoderAI!${NC}"