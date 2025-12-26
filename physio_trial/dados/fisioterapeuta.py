from dados.pessoa import Pessoa
from dados.restricoes_dias_horarios import RestricoesDiasHorarios

class Fisioterapeuta(Pessoa):
    '''Classe que representa um fisioterapeuta'''

    def __init__(self, id_fisioterapeuta, nome_fisioterapeuta, email, data_nascimento, login, senha, status_fisioterapeuta, tipo = "fisioterapeuta"):
        super().__init__(id_fisioterapeuta, nome_fisioterapeuta, email, data_nascimento, tipo, status_fisioterapeuta)
        self.login = login 
        self.senha = senha
        self.restricoes_fisioterapeuta = RestricoesDiasHorarios()

    def restricao_fisioterapeuta(self, horarios, dias):
        pass
    def __repr__(self):
        return f"Fisioterapeuta(id={self.id_pessoa}, nome='{self.nome}')"
