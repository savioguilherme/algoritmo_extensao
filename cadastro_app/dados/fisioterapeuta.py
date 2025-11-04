from dados.pessoa import Pessoa
from dados.agenda import Agenda

class Fisioterapeuta(Pessoa):

    '''Classe que representa um fisioterapeuta'''

    def __init__(self, id_fisioterapeuta, nome_fisioterapeuta, login, senha, tipo = "fisioterapeuta"):
        super().__init__(id_fisioterapeuta, nome_fisioterapeuta, tipo)
        self.login = login 
        self.senha = senha
        self.agenda_fisioterapeuta = Agenda()

    def __repr__(self):
        return f"Fisioterapeuta(id={self.id_pessoa}, nome='{self.nome}')"