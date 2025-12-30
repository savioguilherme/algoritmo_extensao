from psycopg.types.json import Jsonb

from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.services.base.base_sessao_service import BaseSessaoService
from armazenamento.decorators.auth_class import auth_class

from datetime import datetime

@auth_class
class SessaoService(BaseSessaoService):
    """
    Serviço base para operações relacionadas a sessoes.
    """
    def __init__(self, dal: DataAccessLayer):
        self._dal = dal

    def agendar_dia_horario(self, id_sessao: int, novo_dia_horario: datetime) -> None:
        """
        Agenda o dia e horário de uma sessao, atualizando também o status de agendamento.

        Args:
            id_sessao: ID da sessao.
            novo_dia_horario: objeto datetime representando o novo dia e horário da sessão.
        """
        pass

    def cadastrar_conclusao(self, id_sessao: int) -> None:
        """
        Marca uma sessão como concluida.

        Args:
            id_sessao: ID da sessao.
        """
        pass

    def atualizar_sessoes_agendadas(self, sessoes_atualizadas: list[dict[str, int | datetime]]) -> bool:
        """
        Atualiza múltiplas sessões agendadas.

        Args:
            sessoes_atualizadas: Lista de dicionários contendo 'id_sessao' e 'dia_horario'.
        """
        
        _ = self._dal.call_procedure(
            "usp_sessoes_alterar_em_massa",
            p_lista_sessoes=Jsonb(sessoes_atualizadas)
        )

        return True
