from dados.pessoa import Pessoa

class Pesquisador(Pessoa):
    def __init__(self, id_pesquisador, nome_pesquisador):

        super().__init__(id_pesquisador, nome_pesquisador)

    def __repr__(self):
        return f"Pesquisador(id={self.id_pessoa}, nome='{self.nome}')"
