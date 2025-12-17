from dados.pessoa import Pessoa
from dados.sessao import Sessao
from dados.restricoes_dias_horarios import RestricoesDiasHorarios
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

class Paciente(Pessoa):
    '''Classe que representa um paciente'''

    CODIGOS_SESSOES = [
        "fisio1", "fisio2", "fisio3", "fisio4", "fisio5",
        "fisio6", "fisio7", "fisio8", "exfinal",
        "retorno1", "retorno2"
    ]

    def __init__(self, id_paciente, nome_paciente, pesquisador: Pesquisador, fisioterapeuta: Fisioterapeuta, status_paciente, tipo = "paciente"):
        super().__init__(id_paciente, nome_paciente, tipo, status_paciente)

        self.pesquisador_responsavel = pesquisador
        self.fisioterapeuta_responsavel = fisioterapeuta
        self.restricoes_paciente = RestricoesDiasHorarios()

        self.sessoes_paciente = [
            Sessao(
                id_sessao=None,
                codigo=cod,
                paciente=self,
                dia=None,
                horario=None,
                status_agendamento=False,
                conclusao=False
            )  
            for cod in self.CODIGOS_SESSOES #List Comprehension Python 
        ]
        self.conclusao_pesquisa = False
        self.abandono_pesquisa = False
    
    def restricao_paciente(self, horarios, dias):
        pass

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

    def alterar_pesquisador(self, pesquisador: Pesquisador): 
        self.pesquisador_responsavel = pesquisador

    def alterar_fisioterapeuta(self, fisioterapeuta: Fisioterapeuta): 
        self.fisioterapeuta_responsavel= fisioterapeuta

    def __repr__(self):
        return f"Paciente(id={self.id_pessoa}, nome='{self.nome}')"