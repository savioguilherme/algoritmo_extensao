from abc import ABC, abstractmethod

from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

from armazenamento.dal.data_access_layer import DataAccessLayer

class BaseUsuarioService(ABC):
    """
    Serviço base para operações relacionadas aos usuários.
    """
    def __init__(self, dal: DataAccessLayer):
        self._dal = dal

    @abstractmethod
    def listar_usuarios(self, lista_tipos: list[int]) -> list[Administrador | Fisioterapeuta | Pesquisador]:
        pass

    @abstractmethod
    def consultar_adm(self, id_adm: int) -> Administrador:
        pass

    @abstractmethod
    def inserir_adm(self, adm: Administrador) -> int:
        pass

    @abstractmethod
    def atualizar_adm(self, adm: Administrador) -> None:
        pass

    @abstractmethod
    def consultar_fisioterapeuta(self, id_fisio: int) -> Fisioterapeuta:
        pass

    @abstractmethod
    def inserir_fisioterapeuta(self, fisio: Fisioterapeuta) -> int:
        pass

    @abstractmethod
    def atualizar_fisioterapeuta(self, fisio: Fisioterapeuta) -> None:
        pass

    @abstractmethod
    def consultar_pesquisador(self, id_pesq: int) -> Pesquisador:
        pass

    @abstractmethod
    def inserir_pesquisador(self, pesq: Pesquisador) -> int:
        pass

    @abstractmethod
    def atualizar_pesquisador(self, pesq: Pesquisador) -> None:
        pass

    @abstractmethod
    def deletar_usuario(self, id_usuario: int) -> None:
        pass
