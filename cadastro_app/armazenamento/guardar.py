from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador

class Guardar(): 
    def __init__(self):
        self.guarda_fisioterapeuta = []
        self.guarda_paciente = []
        self.guarda_pesquisador = []
        
    def adiciona_fisioterapeuta(self, id_pessoa, nome):
        fisioterapeuta = Fisioterapeuta(id_pessoa, nome)
        self.guarda_fisioterapeuta.append(fisioterapeuta)
    
    def retorna_fisioterapeuta(self):
        if not self.guarda_fisioterapeuta:
            print("Nenhum fisioterapeuta cadastrado.")
            return
        print("Lista de fisioterapeuta:")
        for p in self.guarda_fisioterapeuta:
            print(p)

    def adiciona_paciente(self, id_pessoa, nome):
        paciente = Paciente(id_pessoa, nome)
        self.guarda_paciente.append(paciente)
    
    def retorna_paciente(self):
        if not self.guarda_paciente:
            print("Nenhum paciente cadastrado.")
            return
        print("Lista de paciente:")
        for p in self.guarda_paciente:
            print(p)

    def adiciona_pesquisador(self, id_pessoa, nome):
        pesquisador = Pesquisador(id_pessoa, nome)
        self.guarda_pesquisador.append(pesquisador)
    
    def retorna_pesquisador(self):
        if not self.guarda_pesquisador:
            print("Nenhum pesquisador cadastrado.")
            return
        print("Lista de Pesquisadores:")
        for p in self.guarda_pesquisador:
            print(p)
