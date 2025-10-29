class Pessoa():
    def __init__(self,id_pessoa,nome):
        self.id_pessoa = id_pessoa
        self.nome = nome
    def __repr__(self):
        return f"Pessoa(id={self.id_pessoa}, nome='{self.nome}')"