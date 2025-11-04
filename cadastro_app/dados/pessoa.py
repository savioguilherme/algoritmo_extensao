
class Pessoa():

    '''Classe base para representar uma pessoa'''

    def __init__(self, id_pessoa, nome, tipo):
        self.id_pessoa = id_pessoa
        self.nome = nome
        self.tipo = tipo

    def __repr__(self):
        return f"Pessoa(id={self.id_pessoa}, nome='{self.nome}', tipo='{self.tipo}')"