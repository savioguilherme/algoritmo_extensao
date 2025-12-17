from typing import Deque, List
from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador
from dados.sessao import Sessao
from collections import deque

class Agenda():
    '''Classe que recebe todas as sessoes dos pacientes ativos e se relaciona com a heuristica para criar os agendamentos'''

    def __init__(self, pacientes: List[Paciente]):
        self.pacientes: List[Paciente] = pacientes
        self.sessoes_pacientes_ativos: Deque[Sessao] = deque()  # fila com todas as sessoes dos pacientes ativos, menos sessoes agendadas
        self.sessoes_agendadas: Deque[Sessao] = deque() # fila com todas as sessoes dos pacientes ativos agendadas e aguardando
        self.fisioterapeutas_ativos: List[Fisioterapeuta] = []
        self.pesquisadores_ativos: List[Pesquisador] = []
    
    def buscar_pacientes_ativos(self): #essa função pode ser removida caso a classe agenda já receba do banco os pacientes ativos
        return [p for p in self.pacientes if p.status_pessoa == True]

    def buscar_sessoes_pacientes_ativos(self): #vai na lista pacientes e busca as sessoes
        for paciente in self.buscar_pacientes_ativos():
            for sessao in paciente.sessoes_paciente:
                if not sessao.status_agendamento and not sessao.conclusao:
                    self.sessoes_pacientes_ativos.append(sessao)
    
    def agendar_sessao(self): #heurística entra aqui
        pass
    
    def concluir_sessao(self, codigo): # o paciente concluiu essa sessão, ela deixa de existir em agenda e fica salva 
        for sessao in self.sessoes_agendadas:
            if sessao.codigo == codigo:
                sessao.conclusao = True
                self.sessoes_agendadas.remove(sessao)

    def remarcar_sessao(self, codigo): # Essa sessão foi desmarcada, ela volta para a fila sessoes_paci_ativos para ser reagendada
        for sessao in self.sessoes_agendadas:
            if sessao.codigo == codigo:
                sessao.status_agendamento = False
                self.sessoes_pacientes_ativos.append(sessao)
                self.sessoes_agendadas.remove(sessao)

    def buscar_fisioterapeutas_ativos(self):
        pass

    def buscar_pesquisadores_ativos(self):
        pass   