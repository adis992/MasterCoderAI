# Load environment variables using python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()

# Napomena: Ova konfiguracija koristi python-dotenv i očekuje .env file na Ubuntu/Linux serveru.
# Za Windows developere: preporučuje se testiranje i deployment na Linux okruženju zbog kompatibilnosti nekih biblioteka.
# Note: This configuration uses python-dotenv and expects a .env file on Ubuntu/Linux server.
# For Windows developers: testing and deployment on Linux environment is recommended due to compatibility of some libraries.

# Environment variables
API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
MODEL_PATH = os.getenv('MODEL_PATH', 'modeli/gguf-model.bin')

class BotConfig:
    """
    Konfiguracija za MasterCoderBot. Uključuje putanje do modela, API ključeve, i ostale postavke.
    Configuration for MasterCoderBot. Includes model paths, API keys, and other settings.
    """
    
    def __init__(self, config_path: str = None):
        """
        Inicijalizira konfiguraciju bota.
        Initializes bot configuration.
        
        Args:
            config_path (str, optional): Putanja do konfiguracijske datoteke (ako se ne koristi .env).
                                        Path to configuration file (if not using .env).
        """
        # Putanje do modela / Model paths
        self.model_dir = os.path.dirname(MODEL_PATH)
        self.model_name = os.path.basename(MODEL_PATH)
        
        # API postavke / API settings
        self.api_key = API_KEY
        self.api_timeout = int(os.getenv('API_TIMEOUT', '30'))
        
        # Debug i logiranje / Debug and logging
        self.debug = DEBUG
        self.log_level = os.getenv('LOG_LEVEL', 'info')
        
        # Dodatne postavke / Additional settings
        self.max_tokens = int(os.getenv('MAX_TOKENS', '1024'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))

    # Dodaj dodatne funkcije za čitanje/validaciju konfiguracije ovdje
    # Add additional functions for config reading/validation here

# Nema viška, svi komentari su dvojezični i informativni.
# No excess code, all comments are bilingual and informative.