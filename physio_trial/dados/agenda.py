from collections import deque
from dados.paciente import Paciente

class Agenda():
    '''Classe que recebe todos os pacientes ativos e suas sessoes, e se relaciona com a heuristica'''

    def __init__(self):
        self.sessoes_pacientes_ativos_nao_agendadas = deque([]) 
        self.sessoes_agendadas = deque([])

        self.id_fisioterapeutas_ativos = []
        self.id_pesquisadores_ativos = []
    
    def buscar_sessoes_pacientes_ativos(self):
        pass

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