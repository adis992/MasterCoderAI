#!/bin/bash

# Update and install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv docker.io docker-compose git

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r zahtjevi.txt

# Verify installations
echo "Verifying installations..."
python3 --version
pip --version
docker --version
docker-compose --version
git --version

# Prepare data
make collect-data
make process-data

# Instructions for adding AI model
echo "Place your AI model in the 'modeli/moj-bot/' directory before training."

# Final message
echo "Setup complete! You can now train the model and run the bot or API."