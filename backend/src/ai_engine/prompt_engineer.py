"""
Ovaj modul implementira funkcionalnosti za inženjering promptova.
Koristi se za generisanje, evaluaciju i optimizaciju promptova za AI modele.
"""

# Import potrebnih biblioteka
from typing import List, Dict

class PromptEngineer:
    """
    Klasa za upravljanje promptovima i njihovu optimizaciju.
    """

    def __init__(self, default_prompt: str):
        """
        Inicijalizacija PromptEngineer klase.

        Args:
            default_prompt (str): Zadani prompt koji se koristi ako nije specificiran drugi.
        """
        self.default_prompt = default_prompt

    def generate_prompt(self, context: str, question: str) -> str:
        """
        Generiše prompt na osnovu konteksta i pitanja.

        Args:
            context (str): Kontekstualni tekst.
            question (str): Pitanje koje treba odgovoriti.

        Returns:
            str: Generisani prompt.
        """
        prompt = f"{self.default_prompt}\nKontekst: {context}\nPitanje: {question}\nOdgovor:"
        return prompt

    def evaluate_prompt(self, prompt: str, model_output: str, expected_output: str) -> Dict[str, float]:
        """
        Evaluira prompt na osnovu izlaza modela i očekivanog izlaza.

        Args:
            prompt (str): Prompt koji je korišten.
            model_output (str): Izlaz modela.
            expected_output (str): Očekivani izlaz.

        Returns:
            Dict[str, float]: Metričke vrijednosti evaluacije (npr. tačnost, sličnost).
        """
        # TODO: Implementirati evaluaciju koristeći metričke funkcije (npr. BLEU, ROUGE)
        accuracy = 1.0 if model_output.strip() == expected_output.strip() else 0.0
        return {"accuracy": accuracy}

    def optimize_prompt(self, context: str, question: str, expected_output: str, iterations: int = 10) -> str:
        """
        Optimizira prompt iterativnim poboljšanjem.

        Args:
            context (str): Kontekstualni tekst.
            question (str): Pitanje koje treba odgovoriti.
            expected_output (str): Očekivani izlaz.
            iterations (int): Broj iteracija za optimizaciju.

        Returns:
            str: Optimizirani prompt.
        """
        best_prompt = self.generate_prompt(context, question)
        best_score = 0.0

        for i in range(iterations):
            # TODO: Generisati varijacije prompta i evaluirati ih
            current_prompt = f"{best_prompt} (Iteracija {i+1})"
            model_output = ""  # TODO: Dobiti izlaz modela za trenutni prompt
            evaluation = self.evaluate_prompt(current_prompt, model_output, expected_output)

            if evaluation["accuracy"] > best_score:
                best_score = evaluation["accuracy"]
                best_prompt = current_prompt

        return best_prompt

    def generisi_varijacije(self, osnovni_prompt: str, broj_varijacija: int = 5) -> List[str]:
        """
        Generiše varijacije osnovnog prompta za eksperimentisanje.

        Args:
            osnovni_prompt (str): Osnovni prompt za generisanje varijacija.
            broj_varijacija (int): Broj varijacija koje treba generisati.

        Returns:
            List[str]: Lista generisanih varijacija prompta.
        """
        varijacije = [f"{osnovni_prompt} - Varijacija {i+1}" for i in range(broj_varijacija)]
        return varijacije

# Primjer korištenja
if __name__ == "__main__":
    default_prompt = "Odgovori na sljedeće pitanje koristeći dostavljeni kontekst."
    prompt_engineer = PromptEngineer(default_prompt)

    context = "AI modeli su korisni za automatizaciju zadataka."
    question = "Kako AI modeli pomažu u automatizaciji?"
    expected_output = "AI modeli pomažu u automatizaciji analizom podataka i donošenjem odluka."

    # Generisanje prompta
    prompt = prompt_engineer.generate_prompt(context, question)
    print("Generisani prompt:", prompt)

    # Optimizacija prompta
    optimized_prompt = prompt_engineer.optimize_prompt(context, question, expected_output)
    print("Optimizirani prompt:", optimized_prompt)