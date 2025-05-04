"""
Modul za bazu znanja - sadrži specijalizirana pravila i znanje za domenu programiranja.
Knowledge base module - contains specialized rules and knowledge for the programming domain.
"""

class KnowledgeBase:
    """
    Klasa za upravljanje domenom znanja i pravilima u programerskom kontekstu.
    Class for managing domain knowledge and rules in programming context.
    """
    
    def __init__(self):
        """
        Inicijalizacija baze znanja.
        Initialization of knowledge base.
        """
        # Pravila i znanje za programske jezike
        # Rules and knowledge for programming languages
        self.programming_languages = {
            "python": {
                "extensions": [".py", ".pyi", ".pyd", ".pyc"],
                "version": "3.10+",
                "frameworks": ["Django", "Flask", "FastAPI", "Tornado"],
                "package_manager": "pip",
                "style_guide": "PEP 8"
            },
            "javascript": {
                "extensions": [".js", ".jsx", ".mjs"],
                "version": "ES6+",
                "frameworks": ["React", "Vue", "Angular", "Express"],
                "package_manager": "npm/yarn",
                "style_guide": "Airbnb/Standard"
            },
            # Ostali jezici mogu biti dodani po potrebi
            # Other languages can be added as needed
        }
        
        # Pravila za refaktorisanje koda
        # Rules for code refactoring
        self.refactoring_rules = {
            "rename_variable": "Preimenuj varijablu koristeći smisleno ime koje opisuje njenu svrhu",
            "extract_method": "Izdvoji duplicirani kod u zasebnu metodu",
            "simplify_conditional": "Pojednostavi složene uvjete koristeći pomoćne metode"
        }
        
    def get_language_info(self, language: str) -> dict:
        """
        Vraća informacije o programskom jeziku.
        Returns information about a programming language.
        
        Args:
            language (str): Naziv programskog jezika / Name of programming language
            
        Returns:
            dict: Informacije o jeziku ili prazan dict ako jezik nije poznat
                 Information about the language or empty dict if language is not recognized
        """
        return self.programming_languages.get(language.lower(), {})
        
    def get_refactoring_rule(self, rule_name: str) -> str:
        """
        Vraća specifično pravilo za refaktorisanje.
        Returns a specific refactoring rule.
        
        Args:
            rule_name (str): Naziv pravila / Rule name
            
        Returns:
            str: Opis pravila ili prazan string ako pravilo nije pronađeno
                Description of the rule or empty string if rule is not found
        """
        return self.refactoring_rules.get(rule_name, "")