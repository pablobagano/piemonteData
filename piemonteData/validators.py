import re

def nome_valido(nome):
    return all(part.isalpha() for part in nome.split())

def sobrenome_valido(sobrenome):
    return all(part.isalpha() for part in sobrenome.split())

def matricula_valida(matricula):
    pattern = r'^[A-Za-z]{1,2}\d{6,7}$'
    return bool(re.match(pattern,matricula))