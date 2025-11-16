from datetime import date
from bisect import bisect_left
class Planner():
    def __init__(self, codigo_dos_horarios : list[str], dias : list[date]):
        self.codigo_dos_horarios = codigo_dos_horarios #horarios ordenados
        self.dias_uteis = dias
        self.dias_uteis.sort()
    #adiciona dia, mantendo a lista de dias ordenada
    def adicionar_dia(self, dia : date):
        index = bisect_left(self.dias_uteis, date)
        self.dias_uteis.insert(index, dia)

    def remover_dia(self, dia : date):
        index = bisect_left(self.dias_uteis, dia)
        if index == len(self.dias_uteis) or self.dias_uteis[index] != dia: return
        del self.dias_uteis[index]
    
