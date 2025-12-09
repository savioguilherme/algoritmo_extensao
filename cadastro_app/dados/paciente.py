from dados.pessoa import Pessoa
from dados.sessao import Sessao
from dados.agenda import Agenda

class Paciente(Pessoa):

    '''Classe que representa um paciente'''

    CODIGOS_SESSOES = [
        "fisio1", "fisio2", "fisio3", "fisio4", "fisio5",
        "fisio6", "fisio7", "fisio8", "exfinal",
        "retorno1", "retorno2"
    ]

    def __init__(self, id_paciente, nome_paciente, pesquisador, fisioterapeuta, tipo = "paciente"):
        super().__init__(id_paciente, nome_paciente, tipo)
        self.pesquisador_responsavel = pesquisador
        self.fisioterapeuta_responsavel = fisioterapeuta
        self.sessoes_paciente = [
            Sessao(cod, None, None, False)
            for cod in self.CODIGOS_SESSOES
        ]
        self.agenda = Agenda()

    def __repr__(self):
        return f"Paciente(id={self.id_pessoa}, nome='{self.nome}')"