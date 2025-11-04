from dados.pessoa import Pessoa
from dados.agenda import Agenda

class Paciente(Pessoa):

    '''Classe que representa um paciente'''

    def __init__(self, id_paciente, nome_paciente, tipo = "paciente"):
        super().__init__(id_paciente, nome_paciente, tipo)
        self.agenda_paciente = Agenda()
        self.pesquisador_responsavel = None
        self.fisioterapeuta_responsavel = None

    def __repr__(self):
        return f"Paciente(id={self.id_pessoa}, nome='{self.nome}')"