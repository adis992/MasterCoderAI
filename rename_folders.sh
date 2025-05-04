#!/bin/bash
# MasterCoderAI - Rename Script
# Preimenovanje foldera iz bosanskog/hrvatskog/srpskog u engleski

echo "===== Preimenovanje foldera iz bosanskog/hrvatskog/srpskog u engleski ====="

# Brisanje nepotrebnih foldera
if [ -d "gotovi_bot" ]; then
  echo "Brišem 'gotovi_bot' folder..."
  rm -rf gotovi_bot
fi

# Preimenovanje foldera
if [ -d "podaci" ]; then
  echo "Preimenujem 'podaci' u 'data'..."
  mv podaci data
fi

if [ -d "script" ]; then
  echo "Preimenujem 'script' u 'scripts'..."
  mv script scripts
fi

if [ -d "eksperimenti" ]; then
  echo "Preimenujem 'eksperimenti' u 'experiments'..."
  mv eksperimenti experiments
fi

if [ -d "evaluacija" ]; then
  echo "Preimenujem 'evaluacija' u 'evaluation'..."
  mv evaluacija evaluation
fi

if [ -d "src/tok_podataka" ]; then
  echo "Preimenujem 'src/tok_podataka' u 'src/data_pipeline'..."
  mv src/tok_podataka src/data_pipeline
fi

if [ -d "src/graf_znanja" ]; then
  echo "Preimenujem 'src/graf_znanja' u 'src/knowledge_graph'..."
  mv src/graf_znanja src/knowledge_graph
fi

if [ -f "src/bot/konfiguracija.py" ]; then
  echo "Preimenujem 'src/bot/konfiguracija.py' u 'src/bot/config.py'..."
  mv src/bot/konfiguracija.py src/bot/config.py
fi

# Brisanje __pycache__ foldera
echo "Brišem sve __pycache__ foldere..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "===== Preimenovanje i čišćenje završeno ====="