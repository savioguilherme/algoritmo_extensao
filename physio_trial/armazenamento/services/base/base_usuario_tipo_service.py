from abc import ABC, abstractmethod

from armazenamento.dal.data_access_layer import DataAccessLayer

class BaseUsuarioTipoService(ABC):
    """
    Serviço base para operações relacionadas a códigos de sessão.
    """
    def __init__(self, dal: DataAccessLayer):
        self._dal = dal
    
    # Métodos abstratos para operações específicas podem ser definidos aqui
    @abstractmethod
    def listar_tipos(self) -> list[int]:
        """
        Lista todos os tipos de usuário identificados numericamente pelo ID de cada tipo.
        """
        pass
