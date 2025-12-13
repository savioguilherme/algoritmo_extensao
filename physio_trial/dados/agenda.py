from collections import deque

class Agenda():

    ''''''

    def __init__(self):
        self.sessoes_pacientes_ativos_nao_agendadas = deque([])
        self.sessoes_agendadas = deque([])
    
    def buscar_sessoes_pacientes_ativos(self):
        pass
    
    def agendar_sessao(self):
        pass
    
    '''def __init__(self):
        self.disponibilidade_semanal = [set() for _ in range(7)]
        self.restricoes = set()
    
    def adicionar_disponibilidade(self, dia_semana, horario):
        self.disponibilidade_semanal[dia_semana%7].add(horario)

    def remover_disponibilidade(self, dia_semana, horario):
        self.disponibilidade_semanal[dia_semana%7].discard(horario)

    def adicionar_restricao(self, dia_horario):
        self.restricoes.add(dia_horario)

    def remover_restricao(self, dia_horario):
        self.restricoes.discard(dia_horario)

    def esta_disponivel(self, dia_horario):
        dia_semana = dia_horario.weekday()
        horario = dia_horario.time()
        return horario in self.disponibilidade_semanal[dia_semana] and not dia_horario in self.restricoes

    def get_lista_disponibilidade_semanal(self):
        return [list(disponibilidade) for disponibilidade in self.disponibilidade_semanal]

    def get_lista_restricoes(self):
        return list(self.restricoes)
    
    def get_horarios(self):
        return set.union(*[horarios for horarios in self.disponibilidade_semanal])'''
