# Ensure Pytest is installed
# pip install pytest
import pytest

# Dummy test da pytest ne pada
def test_dummy():
    assert True

# Dodavanje testnog scenarija za validaciju duplikata

def test_validiraj_duplikate():
    validator = ValidatorPodataka()
    lista_bez_duplikata = [1, 2, 3]
    lista_sa_duplikatima = [1, 2, 2, 3]

    assert validator.validiraj_duplikate(lista_bez_duplikata) == True
    assert validator.validiraj_duplikate(lista_sa_duplikatima) == False