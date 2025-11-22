from dados.pessoa import Pessoa

class Paciente(Pessoa):

    '''Classe que representa um paciente'''

    def __init__(self, id_paciente, nome_paciente, data_nascimento, data_inicial, pesquisador, fisioterapeuta,  tipo = "paciente"):
        super().__init__(id_paciente, nome_paciente, tipo)
        self.data_nascimento = data_nascimento
        self.data_inicial = data_inicial
        self.pesquisador_responsavel = pesquisador
        self.fisioterapeuta_responsavel = fisioterapeuta
    
    def __repr__(self):
        return f"Paciente(id={self.id_pessoa}, nome='{self.nome}')"