from dados.pessoa import Pessoa
from dados.agenda import Agenda

class Pesquisador(Pessoa):

    '''Classe que representa um pesquisador'''

    def __init__(self, id_pesquisador, nome_pesquisador, login, senha, tipo = "pesquisador"):
        super().__init__(id_pesquisador, nome_pesquisador, tipo)
        self.login = login 
        self.senha = senha
        self.agenda_pesquisador = Agenda()
        self.pacientes = []

    def __repr__(self):
        return f"Pesquisador(id={self.id_pessoa}, nome='{self.nome}')"