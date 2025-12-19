
from abc import ABC, abstractmethod

import inject

from armazenamento.dal.data_access_layer import DataAccessLayer

class BaseCodigoSessaoService(ABC):
    """
    Serviço base para operações relacionadas a códigos de sessão.
    """
    def __init__(self, dal: DataAccessLayer):
        self._dal = dal
    
    # Métodos abstratos para operações específicas podem ser definidos aqui
    @abstractmethod
    def listar_codigos_sessoes(self) -> list[str]:
        """
        Lista todos os códigos de sessão disponíveis.
        """
        pass
