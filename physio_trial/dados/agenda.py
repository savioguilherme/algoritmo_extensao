from collections import deque
from dados.paciente import Paciente

class Agenda():
    '''Classe que recebe todos os pacientes ativos e suas sessoes, e se relaciona com a heuristica'''

    def __init__(self, pacientes: Paciente):
        self.pacientes = [pacientes]
        self.sessoes_pacientes_ativos_nao_agendadas = deque() 
        self.sessoes_agendadas = deque()
        self.id_fisioterapeutas_ativos = []
        self.id_pesquisadores_ativos = []
    
    def buscar_pacientes_ativos(self):
        return [p for p in self.pacientes if p.status_pessoa == True]

    def buscar_sessoes_pacientes_ativos(self):
        sessoes = []
        for paciente in self.buscar_pacientes_ativos():
            for sessao in paciente.sessoes_paciente:
                if not sessao.status_agendamento and not sessao.conclusao:
                    sessoes.append(sessao)
        return sessoes
    
    def buscar_sessoes_nao_agendadas_paciente(self, paciente):
        return [
            sessao for sessao in paciente.sessoes_paciente
            if not sessao.status_agendamento and not sessao.conclusao
        ]

    def buscar_sessoes_pacientes_ativos(self):
        self.sessoes_pacientes_ativos_nao_agendadas.clear()
        pacientes_ativos = self.buscar_pacientes_ativos()
        for paciente in pacientes_ativos:
            sessoes_nao_agendadas = self.buscar_sessoes_nao_agendadas_paciente(paciente)

        for sessao in sessoes_nao_agendadas:
            self.sessoes_pacientes_ativos_nao_agendadas.append(sessao)

    def buscar_fisioterapeutas_ativos(self):
        pass

    def buscar_pesquisadores_ativos(self):
        pass

    def agendar_sessao(self):
        pass
    
    def concluir_sessao(self):
        pass

    def remarcar_sessao(self): 
        pass