from abc import ABC, abstractmethod

from armazenamento.dal.data_access_layer import DataAccessLayer

from datetime import datetime

class BaseSessaoService(ABC):
    """
    Serviço base para operações relacionadas a sessoes.
    """
    def __init__(self, dal: DataAccessLayer):
        self._dal = dal

    @abstractmethod
    def agendar_dia_horario(self, id_sessao: int, novo_dia_horario: datetime) -> None:
        """
        Agenda o dia e horário de uma sessao, atualizando também o status de agendamento.

        Args:
            id_sessao: ID da sessao.
            novo_dia_horario: objeto datetime representando o novo dia e horário da sessão.
        """
        pass

    @abstractmethod
    def cadastrar_conclusao(self, id_sessao: int) -> None:
        """
        Marca uma sessão como concluida.

        Args:
            id_sessao: ID da sessao.
        """
        pass
