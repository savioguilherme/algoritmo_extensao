from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, TYPE_CHECKING

from armazenamento.dal.data_access_layer import DataAccessLayer

if TYPE_CHECKING:
    from dados.paciente import Paciente

class BasePacienteService(ABC):
    """
    Serviço base para operações relacionadas a pacientes.
    """
    def __init__(self, dal: DataAccessLayer):
        self._dal = dal

    # Métodos abstratos para operações específicas podem ser definidos aqui
    @abstractmethod
    def consultar(self, id: int) -> Paciente:
        """
        Consulta um paciente pelo ID.

        Args:
            id: ID do paciente.
        """
        pass

    @abstractmethod
    def listar_pacientes(self, apenas_ativos: bool) -> list[Paciente]:
        """
        Lista todos os pacientes cadastrados

        Args:
        """
        pass

    @abstractmethod
    def atualizar_acompanhamentos(self, lista_acompanhamentos: List[Dict[str, int]]) -> bool:
        """
        Atualiza os acompanhamentos (pesquisador e fisioterapeuta) de múltiplos pacientes.

        Args:
            acompanhamentos: Lista de dicionários contendo 'id_paciente', 'id_pesquisador' e 'id_fisioterapeuta'.
        """
        pass

    @abstractmethod
    def cadastrar_abandono_pesquisa(self, id_paciente: int) -> Dict[str, Any] | None:
        """
        Cadastra o abandono de pesquisa para um paciente.

        Args:
            id_paciente: ID do paciente.
        """
        pass

    @abstractmethod
    def alterar_pesquisador(self, id_paciente: int, novo_pesquisador_id: int) -> Dict[str, Any] | None:
        """
        Altera o pesquisador responsável por um paciente.

        Args:
            id_paciente: ID do paciente.
            novo_pesquisador_id: ID do novo pesquisador.
        """
        pass

    @abstractmethod
    def alterar_fisioterapeuta(self, id_paciente: int, novo_fisioterapeuta_id: int) -> Dict[str, Any] | None:
        """
        Altera o fisioterapeuta responsável por um paciente.

        Args:
            id_paciente: ID do paciente.
            novo_fisioterapeuta_id: ID do novo fisioterapeuta.
        """
        pass
