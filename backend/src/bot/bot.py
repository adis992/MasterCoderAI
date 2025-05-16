import sys
sys.path.insert(0, '/app')
from src.bot.config import BotConfig  # Preimenovano iz BotKonfiguracija
from src.ai_engine.model_loader import ModelLoader

class MasterCoderBot:
    """
    Glavna klasa bota koja upravlja modelima i odgovara na upite.
    Main bot class responsible for model management and responding to queries.
    """
    def __init__(self, config_path: str):
        """
        Inicijalizacija MasterCoderBot instance.
        Initialization of MasterCoderBot instance.
        
        Args:
            config_path (str): Putanja do konfiguracijske datoteke.
                              Path to the configuration file.
        """
        self.config = BotConfig(config_path)  # Preimenovano iz BotKonfiguracija
        self.model_loader = ModelLoader(self.config.model_dir)
        # Automatski loader prema ekstenziji
        self.tokenizer, self.model = self.model_loader.load_model_auto(self.config.model_name)

    def answer(self, query: str) -> str:  # Preimenovano iz odgovori
        """
        Odgovara na korisnički upit koristeći AI model.
        Responds to a user query using the AI model.
        
        Args:
            query (str): Korisnički upit. / User query.
            
        Returns:
            str: Odgovor bota. / Bot's response.
        """
        # TODO: Integracija sa hibridnim modelom i prompt engineerom
        # TODO: Integration with hybrid model and prompt engineer
        return f"[BOT RESPONSE] {query}"

    def evaluate_response(self, query: str, response: str) -> float:  # Preimenovano iz evaluiraj_odgovor
        """
        Evaluira kvalitet odgovora na osnovu upita.
        Evaluates response quality based on the query.

        Args:
            query (str): Korisnički upit. / User query.
            response (str): Generisani odgovor bota. / Generated bot response.

        Returns:
            float: Ocjena kvaliteta odgovora (0.0 - 1.0). / Response quality score (0.0 - 1.0).
        """
        # TODO: Implementirati evaluaciju koristeći metričke funkcije
        # TODO: Implement evaluation using metric functions
        return 0.85

    def run(self):
        """
        Pokreće interaktivnu sesiju bota u konzoli.
        Runs an interactive bot session in the console.
        """
        print("MasterCoderAI Bot je spreman! (unesi 'exit' za izlaz)")
        print("MasterCoderAI Bot is ready! (type 'exit' to quit)")
        while True:
            query = input("You: ")  # Preimenovano iz Ti/upit
            if query.strip().lower() == 'exit':
                print("Doviđenja! / Goodbye!")
                break
            response = self.answer(query)  # Preimenovano iz odgovori/odgovor
            print(f"Bot: {response}")

if __name__ == "__main__":
    config_path = "src/bot/config.py"  # ili putanja do .yaml/.json
    bot = MasterCoderBot(config_path)
    bot.run()