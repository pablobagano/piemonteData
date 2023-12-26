import re

def nome_valido(nome):
    return nome.isalpha()

def sobrenome_valido(sobrenome):
    return sobrenome.isalpha()

def matricula_valida(matricula):
    pattern = r'^[A-Za-z]{1,2}\d{6,7}$'
    return bool(re.match(pattern,matricula))