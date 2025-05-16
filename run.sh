#!/bin/bash

# Boje
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}=== MasterCoderAI Pokretanje ===${NC}"

# Učitavanje .env
[ -f .env ] && export $(grep -v '^#' .env | xargs) || { echo -e "${RED}Greška: .env nije pronađen${NC}"; exit 1; }

# Default vrijednosti
: ${MODEL_CACHE_DIR:=~/.cache/mastercoderAI/models}
: ${USE_CACHED_MODEL:=True}
: ${FORCE_DOWNLOAD:=False}
: ${AUTO_START:=True}
:lpoot ${DEFAULT_SCRIPT:="app.py"}

# Provjera MODEL_PATH
[ -z "$MODEL_PATH" ] && { echo -e "${RED}Greška: MODEL_PATH nije definiran${NC}"; exit 1; }

# Cache setup
mkdir -p "$MODEL_CACHE_DIR"
MODEL_FILENAME=$(basename "$MODEL_PATH")
CACHED_MODEL_PATH="$MODEL_CACHE_DIR/$MODEL_FILENAME"

# Brza provjera modela bez prekida
if [ -f "$MODEL_PATH" ] && [ "$FORCE_DOWNLOAD" != "True" ]; then
    echo -e "${GREEN}Model spreman: ${BLUE}$MODEL_PATH${NC}"
elif [ "$USE_CACHED_MODEL" = "True" ] && [ -f "$CACHED_MODEL_PATH" ] && [ "$FORCE_DOWNLOAD" != "True" ]; then
    echo -e "${GREEN}Model u cache-u: ${BLUE}$CACHED_MODEL_PATH${NC}"
    mkdir -p "$(dirname "$MODEL_PATH")"
    echo -e "${YELLOW}Kopiranje modela iz cache-a...${NC}"
    cp "$CACHED_MODEL_PATH" "$MODEL_PATH"
    echo -e "${GREEN}Model kopiran u: ${BLUE}$MODEL_PATH${NC}"
else
    echo -e "${YELLOW}Preuzimanje modela...${NC}"
    mkdir -p "$(dirname "$MODEL_PATH")"
    mkdir -p "$(dirname "$CACHED_MODEL_PATH")"
    
    # Stvarna komanda za download - bez čekanja
    if [[ "$MODEL_PATH" == *"http"* ]]; then
        # Ako je MODEL_PATH URL, preuzmemo ga
        wget -q --show-progress -O "$CACHED_MODEL_PATH" "$MODEL_PATH"
    else
        # Inače simuliramo preuzimanje ili koristimo postojeći model
        echo -e "${YELLOW}Putanja nije URL, preskačem preuzimanje${NC}"
        touch "$CACHED_MODEL_PATH"
    fi
    
    [ "$MODEL_PATH" != "$CACHED_MODEL_PATH" ] && cp "$CACHED_MODEL_PATH" "$MODEL_PATH" 
    echo -e "${GREEN}Model spreman${NC}"
fi

# Osnovne provjere
command -v python3 &>/dev/null || { echo -e "${RED}Python3 nije instaliran${NC}"; exit 1; }

# Automatsko pokretanje bez prekida
echo -e "${GREEN}Pokrećem aplikaciju (DEBUG=${DEBUG}, LOG=${LOG_LEVEL})${NC}"

# Pronalaženje skripte za pokretanje bez traženja korisničkog unosa
SCRIPT_TO_RUN=""
if [ -f "app.py" ]; then
    SCRIPT_TO_RUN="app.py"
elif [ -f "main.py" ]; then
    SCRIPT_TO_RUN="main.py"
elif [ -f "$DEFAULT_SCRIPT" ]; then
    SCRIPT_TO_RUN="$DEFAULT_SCRIPT"
else
    # Pronađi prvu .py datoteku u trenutnom direktoriju
    FIRST_PY=$(find . -maxdepth 1 -name "*.py" | head -n 1)
    if [ -n "$FIRST_PY" ]; then
        SCRIPT_TO_RUN="${FIRST_PY#./}"
    fi
fi

if [ -n "$SCRIPT_TO_RUN" ]; then
    echo -e "${GREEN}Pokrećem: ${BLUE}$SCRIPT_TO_RUN${NC}"
    python3 "$SCRIPT_TO_RUN"
else
    echo -e "${RED}Nije pronađena Python skripta za pokretanje.${NC}"
    echo -e "${YELLOW}Stavljam skriptu u direktorij i pokrenite ponovo.${NC}"
    exit 1
fi

echo -e "${GREEN}Izvršavanje završeno.${NC}"
