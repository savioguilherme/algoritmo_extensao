from dados.pessoa import Pessoa

class Fisioterapeuta(Pessoa):
    def __init__(self, id_fisioterapeuta, nome_fisioterapeuta):

        super().__init__(id_fisioterapeuta, nome_fisioterapeuta)

    def __repr__(self):
        return f"Fisioterapeuta(id={self.id_pessoa}, nome='{self.nome}')"