import datetime
from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador

class Agenda():

    ''' '''

    def __init__(self, fisioterapeuta: Fisioterapeuta, paciente: Paciente, pesquisador: Pesquisador):
        self.agenda_pessoa = []

    def adicionadia(self, dia, mes, ano, hora, minuto, segundo):
        data = datetime.datetime(ano, mes, dia, hora, minuto, segundo)
        self.agenda_pessoa.append(data)

    def removedia(self, dia, mes, ano, hora, minuto, segundo):
        data = datetime.date(ano, mes, dia, hora, minuto, segundo)
        self.agenda_pessoa.remove(data)

    def __repr__(self):
        return f"Agenda({self.agenda_pessoa})"