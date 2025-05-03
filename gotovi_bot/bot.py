from typing import List
import random
from sentence_transformers import SentenceTransformer
import torch

class Bot:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.responses = [
            "Evo primjera kako to možeš riješiti:",
            "Najbolji pristup bi bio:",
            "Razmotri sljedeće rješenje:",
            "Na osnovu tvog pitanja, predlažem:",
            "Možemo to riješiti ovako:",
        ]
        
        # Osnovni code snippets za demonstraciju
        self.code_examples = {
            "python": [
                "def hello_world():\n    print('Hello World!')",
                "for i in range(10):\n    print(f'Broj: {i}')",
                "try:\n    x = 1/0\nexcept Exception as e:\n    print(f'Error: {e}')"
            ],
            "javascript": [
                "function helloWorld() {\n    console.log('Hello World!');\n}",
                "for(let i = 0; i < 10; i++) {\n    console.log(`Broj: ${i}`);\n}",
                "try {\n    throw new Error('Test');\n} catch(e) {\n    console.error(e);\n}"
            ]
        }
        
    def generate_response(self, message: str) -> str:
        # Embediranje korisničkog upita
        query_embedding = self.model.encode(message, convert_to_tensor=True)
        
        # Dummy logika za odabir odgovora na osnovu upita
        if "python" in message.lower():
            code = random.choice(self.code_examples["python"])
            return f"{random.choice(self.responses)}\n```python\n{code}\n```"
        elif "javascript" in message.lower():
            code = random.choice(self.code_examples["javascript"])
            return f"{random.choice(self.responses)}\n```javascript\n{code}\n```"
        else:
            return f"Razumijem tvoje pitanje o '{message}'. {random.choice(self.responses)}"
        
    def get_code_suggestion(self, code: str) -> str:
        # Dummy code review funkcionalnost
        suggestions = [
            "Dodaj error handling za robustnost.",
            "Razmotri dodavanje dokumentacije.",
            "Možda bi bilo dobro dodati logiranje.",
            "Razmisli o korištenju type hints."
        ]
        return random.choice(suggestions)