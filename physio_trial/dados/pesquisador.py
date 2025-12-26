from dados.pessoa import Pessoa
from dados.restricoes_dias_horarios import RestricoesDiasHorarios

class Pesquisador(Pessoa):
    '''Classe que representa um pesquisador'''

    def __init__(self, id_pesquisador, nome_pesquisador, email, data_nascimento, login, senha, status_pesquisador, tipo = "pesquisador"):
        super().__init__(id_pesquisador, nome_pesquisador, email, data_nascimento, tipo, status_pesquisador)
        self.login = login
        self.senha = senha
        self.restricoes_pesquisador = RestricoesDiasHorarios()

    def restricao_pesquisador(self, horarios, dias):
        pass

    def __repr__(self):
        return f"Pesquisador(id={self.id_pessoa}, nome='{self.nome}')"
