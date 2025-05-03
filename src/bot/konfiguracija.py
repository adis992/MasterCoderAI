import os

class BotKonfiguracija:
    def __init__(self, config_path=None):
        # Hardkodirane vrijednosti za primjer, može se proširiti za YAML/JSON
        self.model_name = os.environ.get("MC_MODEL_NAME", "bert-base-uncased")
        self.model_dir = os.environ.get("MC_MODEL_DIR", "modeli/moj-bot/")
        self.log_level = os.environ.get("MC_LOG_LEVEL", "INFO")
        self.api_timeout = int(os.environ.get("MC_API_TIMEOUT", 30))
        # Dodaj još konfiguracija po potrebi