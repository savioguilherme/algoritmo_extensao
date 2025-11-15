import datetime

class AgendaPaciente():

    ''' '''

    def __init__(self, data_inicial):
        self.data_inicial = data_inicial
        self.horario = None
        self.profissional = None
        self.tratamento = []

    def agenda(self): 
        self.tratamento.append(self.data_inicial, self.horario, self.profissional)
        