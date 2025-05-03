import sys
from .konfiguracija import BotKonfiguracija
from src.ai_engine.model_loader import ModelLoader

class MasterCoderBot:
    def __init__(self, config_path: str):
        self.config = BotKonfiguracija(config_path)
        self.model_loader = ModelLoader(self.config.model_dir)
        self.tokenizer, self.model = self.model_loader.load_transformer_model(self.config.model_name)

    def odgovori(self, upit: str) -> str:
        # TODO: Integracija sa hibridnim modelom i prompt engineerom
        return f"[BOT ODGOVOR] {upit}"

    def evaluiraj_odgovor(self, upit: str, odgovor: str) -> float:
        """
        Evaluira kvalitet odgovora na osnovu upita.

        Args:
            upit (str): Korisnički upit.
            odgovor (str): Generisani odgovor bota.

        Returns:
            float: Ocjena kvaliteta odgovora (0.0 - 1.0).
        """
        # TODO: Implementirati evaluaciju koristeći metričke funkcije
        return 0.85

    def run(self):
        print("MasterCoderAI Bot je spreman! (unesi 'exit' za izlaz)")
        while True:
            upit = input("Ti: ")
            if upit.strip().lower() == 'exit':
                print("Doviđenja!")
                break
            odgovor = self.odgovori(upit)
            print(f"Bot: {odgovor}")

if __name__ == "__main__":
    config_path = "src/bot/konfiguracija.py"  # ili putanja do .yaml/.json
    bot = MasterCoderBot(config_path)
    bot.run()