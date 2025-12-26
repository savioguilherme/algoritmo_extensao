from dados.pessoa import Pessoa

class Administrador(Pessoa):
    '''Classe que representa um administrador do sistema'''

    def __init__(self, id_administrador, nome_administrador, email, data_nascimento, login, senha, status_administrador, tipo="administrador"):
        super().__init__(id_administrador, nome_administrador, email, data_nascimento, tipo, status_administrador)
        self.login = login 
        self.senha = senha

    def __repr__(self):
        return f"Administrador(id={self.id_pessoa}, nome='{self.nome}')"
