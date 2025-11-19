class AgendaPesquisador():

    ''' '''

    def __init__(self, data_inicial):
        self.data_inicial = data_inicial
        self.data = None
        self.horario = None
        self.profissional = None
        self.secao = []
        self.agenda = []

    def cadastrar_secao(self): 
        self.secao.append(self.data, self.horario, self.profissional)
    
    def cadastrar_agenda(self):
        for 1 in range(12):
            self.agenda.append(self.cadastrar_secao())