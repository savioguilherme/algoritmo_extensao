from dados.pessoa import Pessoa
from dados.agenda import Agenda

class Fisioterapeuta(Pessoa):

    '''Classe que representa um fisioterapeuta'''

    def __init__(self, id_fisioterapeuta, nome_fisioterapeuta, login, senha, status_fisioterapeuta, tipo = "fisioterapeuta"):
        super().__init__(id_fisioterapeuta, nome_fisioterapeuta, tipo, status_fisioterapeuta)
        self.login = login 
        self.senha = senha
        self.horarios_restricao = []
        self.dias_restricao = []

    def restricao_fisioterapeuta(self, horarios, dias):
        self.horarios_restricao.append(horarios)
        self.dias_restricao.append(dias)

    def __repr__(self):
        return f"Fisioterapeuta(id={self.id_pessoa}, nome='{self.nome}')"
