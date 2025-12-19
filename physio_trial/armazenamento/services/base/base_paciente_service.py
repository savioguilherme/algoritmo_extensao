from abc import ABC, abstractmethod
from typing import Any, Dict

from armazenamento.dal.data_access_layer import DataAccessLayer

class BasePacienteService(ABC):
    """
    Serviço base para operações relacionadas a pacientes.
    """
    def __init__(self, dal: DataAccessLayer):
        self._dal = dal

    # Métodos abstratos para operações específicas podem ser definidos aqui
    @abstractmethod
    def cadastrar_abandono_pesquisa(self, paciente_id: int) -> Dict[str, Any] | None:
        """
        Cadastra o abandono de pesquisa para um paciente.

        Args:
            paciente_id: ID do paciente.
        """
        pass

    @abstractmethod
    def alterar_pesquisador(self, paciente_id: int, novo_pesquisador_id: int) -> Dict[str, Any] | None:
        """
        Altera o pesquisador responsável por um paciente.

        Args:
            paciente_id: ID do paciente.
            novo_pesquisador_id: ID do novo pesquisador.
        """
        pass

    @abstractmethod
    def alterar_fisioterapeuta(self, paciente_id: int, novo_fisioterapeuta_id: int) -> Dict[str, Any] | None:
        """
        Altera o fisioterapeuta responsável por um paciente.

        Args:
            paciente_id: ID do paciente.
            novo_fisioterapeuta_id: ID do novo fisioterapeuta.
        """
        pass
