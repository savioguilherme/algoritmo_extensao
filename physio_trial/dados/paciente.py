from dados.pessoa import Pessoa
from dados.sessao import Sessao

class Paciente(Pessoa):
    '''Classe que representa um paciente'''

    CODIGOS_SESSOES = [
        "fisio1", "fisio2", "fisio3", "fisio4", "fisio5",
        "fisio6", "fisio7", "fisio8", "exfinal",
        "retorno1", "retorno2"
    ]

    def __init__(self, id_paciente, nome_paciente, pesquisador, fisioterapeuta, status_paciente, tipo = "paciente"):
        super().__init__(id_paciente, nome_paciente, tipo, status_paciente)

        self.pesquisador_responsavel = pesquisador
        self.fisioterapeuta_responsavel = fisioterapeuta

        self.sessoes_paciente = [
            Sessao(None,cod, None, None, False, False)  #List Comprehension Python 
            for cod in self.CODIGOS_SESSOES
        ]

        self.horarios_restricao = []
        self.dias_restricao = []

        self.conclusao = False
        self.abandono = False

    def restricao_paciente(self, horarios, dias):
        self.horarios_restricao.append(horarios)
        self.dias_restricao.append(dias)
    
    def verificar_conclusao_pesquisa(self):
        for i in self.sessoes_paciente:
            if i.conclusao is False:
                return
            self.conclusao = True
    
    def cadastrar_abandono_pesquisa(self):
        self.abandono = True
        self.desabilitar_paciente()
    
    def desabilitar_paciente(self): 
        self.status_pessoa = False

    def alterar_pesquisador(self, pesquisador): 
        self.pesquisador_responsavel = pesquisador

    def alterar_fisioterapeuta(self, fisioterapeuta): 
        self.fisioterapeuta_responsavel= fisioterapeuta

    def __repr__(self):
        return f"Paciente(id={self.id_pessoa}, nome='{self.nome}')"