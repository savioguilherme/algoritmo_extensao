from dados.sessao import Sessao

from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.services.base.base_sessao_service import BaseSessaoService

from datetime import datetime

class SessaoServiceMock(BaseSessaoService):
    def __init__(self, dal: DataAccessLayer, sessoes: list[Sessao]):
        super().__init__(dal)
        self.sessoes = {sessao.id_sessao: sessao for sessao in sessoes}

    def agendar_dia_horario(self, id_sessao: int, novo_dia_horario: datetime) -> None:
        if id_sessao in self.sessoes:
            self.sessoes[id_sessao].dia = novo_dia_horario.date()
            self.sessoes[id_sessao].horario = novo_dia_horario.time()
            self.sessoes[id_sessao].status_agendamento = True

    def cadastrar_conclusao(self, id_sessao: int) -> None:
        if id_sessao in self.sessoes:
            self.sessoes[id_sessao].conclusao = True
