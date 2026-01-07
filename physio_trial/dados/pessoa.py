from datetime import date

class Pessoa():
    '''Classe base para representar uma pessoa'''

    def __init__(self, id_pessoa: int, nome: str, email: str, data_nascimento: date, tipo: int, status_pessoa: bool):
        self.id_pessoa = id_pessoa
        self.nome = nome
        self.email = email
        self.data_nascimento = data_nascimento
        self.tipo = tipo
        self.status_pessoa = status_pessoa  #false para uma pessoa que está inativa

    def __repr__(self):
        return f"Pessoa(id={self.id_pessoa}, nome='{self.nome}', email='{self.email}', data_nascimento='{self.data_nascimento}', tipo='{self.tipo}')"
