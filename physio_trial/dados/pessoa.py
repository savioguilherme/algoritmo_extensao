
class Pessoa():

    '''Classe base para representar uma pessoa'''

    def __init__(self, id_pessoa, nome, tipo, status_pessoa):
        self.id_pessoa = id_pessoa
        self.nome = nome
        self.tipo = tipo
        self.status_pessoa = status_pessoa  #false para uma pessoa que está inativa

    def __repr__(self):
        return f"Pessoa(id={self.id_pessoa}, nome='{self.nome}', tipo='{self.tipo}')"