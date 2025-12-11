from dados.pessoa import Pessoa
from dados.agenda import Agenda

class Pesquisador(Pessoa):

    '''Classe que representa um pesquisador'''

    def __init__(self, id_pesquisador, nome_pesquisador, login, senha, status_pesquisador, tipo = "pesquisador"):
        super().__init__(id_pesquisador, nome_pesquisador, tipo, status_pesquisador)
        self.login = login 
        self.senha = senha
        self.horarios_restricao = []
        self.dias_restricao = []
        self.agenda = Agenda()

    def restricao_pesquisador(self, horarios, dias):
        self.horarios_restricao.append(horarios)
        self.dias_restricao.append(dias)

    def __repr__(self):
        return f"Pesquisador(id={self.id_pessoa}, nome='{self.nome}')"
