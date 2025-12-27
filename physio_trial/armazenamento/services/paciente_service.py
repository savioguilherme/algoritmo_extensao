from typing import Any, Dict
import inject

from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.services.base.base_paciente_service import BasePacienteService

class PacienteService(BasePacienteService):
    @inject.autoparams()
    def __init__(self, dal: DataAccessLayer):
        super().__init__(dal)

    def listar_pacientes(self) -> list[Paciente]:
        pass

    def cadastrar_abandono_pesquisa(self, paciente_id: int) -> Dict[str, Any] | None:
        """
        Implementação do método para cadastrar o abandono de pesquisa para um paciente.

        Args:
            paciente_id: ID do paciente.
        """

        return None if self._dal.call_procedure(
            "usp_paciente_alterar_status_abandono",
            paciente_id=paciente_id,
            status_abandono=True
        ) is None else {}
    
    def alterar_pesquisador(self, paciente_id: int, novo_pesquisador_id: int) -> Dict[str, Any] | None:
        """
        Implementação do método para alterar o pesquisador responsável por um paciente.

        Args:
            paciente_id: ID do paciente.
            novo_pesquisador_id: ID do novo pesquisador.
        """

        return None if self._dal.call_procedure(
            "usp_paciente_alterar_pesquisador",
            paciente_id=paciente_id,
            novo_pesquisador_id=novo_pesquisador_id
        ) is None else {}
    
    def alterar_fisioterapeuta(self, paciente_id: int, novo_fisioterapeuta_id: int) -> Dict[str, Any] | None:
        """
        Implementação do método para alterar o fisioterapeuta responsável por um paciente.

        Args:
            paciente_id: ID do paciente.
            novo_fisioterapeuta_id: ID do novo fisioterapeuta.
        """

        return None if self._dal.call_procedure(
            "usp_paciente_alterar_fisioterapeuta",
            paciente_id=paciente_id,
            novo_fisioterapeuta_id=novo_fisioterapeuta_id
        ) is None else {}
