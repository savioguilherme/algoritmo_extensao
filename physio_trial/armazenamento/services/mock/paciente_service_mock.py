from typing import Any, Dict, List

from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService
from armazenamento.services.base.base_paciente_service import BasePacienteService

from dados.paciente import Paciente
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

class PacienteServiceMock(BasePacienteService):
    def __init__(
        self,
        dal: DataAccessLayer,
        codigo_sessao_service: BaseCodigoSessaoService,
        pacientes: list[Paciente],
        fisioterapeutas: list[Fisioterapeuta],
        pesquisadores: list[Pesquisador],
    ):
        super().__init__(dal)
        self.pacientes = {paciente.id_pessoa: paciente for paciente in pacientes}
        self.pesquisadores = {pesquisador.id_pessoa: pesquisador for pesquisador in pesquisadores}
        self.fisioterapeutas = {fisioterapeuta.id_pessoa: fisioterapeuta for fisioterapeuta in fisioterapeutas}

    def listar_pacientes(self) -> list[Paciente]:
        return [self.pacientes[paciente_id] for paciente_id in self.pacientes]

    def cadastrar_abandono_pesquisa(self, paciente_id: int) -> Dict[str, Any] | None:
        if paciente_id in self.pacientes:
            self.pacientes[paciente_id].abandono_pesquisa = True

    def alterar_pesquisador(self, paciente_id: int, novo_pesquisador_id: int) -> Dict[str, Any] | None:
        if paciente_id in self.pacientes and novo_pesquisador_id in self.pesquisadores:
            self.pacientes[paciente_id].pesquisador_responsavel = self.pesquisadores[novo_pesquisador_id]

    def alterar_fisioterapeuta(self, paciente_id: int, novo_fisioterapeuta_id: int) -> Dict[str, Any] | None:
        if paciente_id in self.pacientes and novo_fisioterapeuta_id in self.fisioterapeutas:
            self.pacientes[paciente_id].fisioterapeuta_responsavel = self.fisioterapeutas[novo_fisioterapeuta_id]
