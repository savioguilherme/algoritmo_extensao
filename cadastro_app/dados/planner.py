from datetime import date, time
from agenda import Agenda
from bisect import bisect_left
class Planner():
    def __init__(self, codigo_dos_horarios : dict[time, str], dias : list[date]):
        self.codigo_dos_horarios = codigo_dos_horarios 
        self.dias_uteis = dias
        self.dias_uteis.sort()
    #adiciona dia, mantendo a lista de dias ordenada
    def adicionar_dia(self, dia : date):
        index = bisect_left(self.dias_uteis, dia)
        self.dias_uteis.insert(index, dia)

    def remover_dia(self, dia : date):
        index = bisect_left(self.dias_uteis, dia)
        if index == len(self.dias_uteis) or self.dias_uteis[index] != dia: return
        del self.dias_uteis[index]
    def calcular_disponibilidade(self, pessoa : Agenda):
        #inicializa a tabela de disponibilidade
        disponibilidade = {}
        for dia in self.dias_uteis:
            for horario in self.codigo_dos_horarios.values():
                disponibilidade[dia][horario] = True
        #atualiza conforme os horarios marcados na agenda pessoal
        for data in pessoa.agenda_pessoa:
            codigo = self.codigo_dos_horarios[data.TimeOfDay]
            disponibilidade[dia][codigo] = False
        return disponibilidade
        

            
    
