from dados.pessoa import Pessoa
from dados.sessao import Sessao
<<<<<<< HEAD
=======
from dados.agenda import Agenda
>>>>>>> corrigir classes de dados

class Paciente(Pessoa):

    '''Classe que representa um paciente'''

    def __init__(self, id_paciente, nome_paciente, data_nascimento, data_inicial, pesquisador, fisioterapeuta, tipo = "paciente"):
        super().__init__(id_paciente, nome_paciente, tipo)
        self.data_nascimento = data_nascimento
        self.data_inicial = data_inicial
        self.pesquisador_responsavel = pesquisador
        self.fisioterapeuta_responsavel = fisioterapeuta
<<<<<<< HEAD
        self.sessoes = []

    def adicionarSessao(self, cod, horario):
        self.sessoes.append(Sessao(cod, horario, self.pesquisador_responsavel, self.fisioterapeuta_responsavel, self.nome)) 
=======
        self.sessoes = {}
        self.agenda = Agenda()

    def adicionarSessao(self, sessao):
        self.sessoes.append(sessao) 
>>>>>>> corrigir classes de dados

    def __repr__(self):
        return f"Paciente(id={self.id_pessoa}, nome='{self.nome}')"
