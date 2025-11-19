import holidays
from datetime import *

class Agenda():

    '''Classe Agenda recebe todas as outras agendas e organiza todo o sistema de agendamento'''

    def __init__(self):
        
        self.agenda_geral = []

        self.dia_inicial_calendario = date(2025,11,1)

        # dicionario com os 5 slots mostrando os horários inicias de cada um
        self.slots = {'primeira': time(8), 'segunda': time(10), 'terceira': time(13), 'quarta':time(15), 'quinta':time(17)} 

    def criarcalendario(self):
        pass

    def verificaferiado(self, diarecebido):
        feriados_brasil = holidays.country_holidays("BR") #recebe todos os feriados do Brasil (em teoria, preciso confirmar)
        if diarecebido in feriados_brasil:
            return True #se o dia for um feriado retorna true
        
    def verificafinalsemana(self, diarecebido): 
        diarecebido = date.weekday() #recebe todos os dias e sua posição na semana como um número (seg = 0)
        if diarecebido == 5 or diarecebido == 6: 
            return True #se for 5 (sáb) ou 6 (dom) returna true

    def adicionadia(self, dia, mes, ano, hora, minuto, segundo):
        data = datetime.datetime(ano, mes, dia, hora, minuto, segundo)
        self.agenda_pessoa.append(data)

    def removedia(self, dia, mes, ano, hora, minuto, segundo):
        data = datetime.date(ano, mes, dia, hora, minuto, segundo)
        self.agenda_pessoa.remove(data)