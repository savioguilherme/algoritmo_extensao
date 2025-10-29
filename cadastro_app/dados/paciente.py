from dados.pessoa import Pessoa

class Paciente(Pessoa):
    def __init__(self, id_paciente, nome_paciente):

        super().__init__(id_paciente, nome_paciente)
    
    def __repr__(self):
        return f"Fisioterapeuta(id={self.id_pessoa}, nome='{self.nome}')"