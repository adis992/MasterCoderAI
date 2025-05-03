class ZnanjeBaza:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def dodaj_fakt(self, fakt):
        self.facts.add(fakt)

    def dodaj_pravilo(self, pravilo):
        self.rules.append(pravilo)

    def upit(self, fakt):
        return fakt in self.facts

    def ukloni_fakt(self, fakt):
        """
        Uklanja činjenicu iz baze znanja.

        Args:
            fakt (str): Činjenica za uklanjanje.
        """
        self.facts.discard(fakt)

# Primjer korištenja
if __name__ == "__main__": 
    kb = ZnanjeBaza()
    kb.dodaj_fakt("Python je programski jezik.")
    print(kb.upit("Python je programski jezik."))