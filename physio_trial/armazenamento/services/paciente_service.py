from psycopg.types.json import Jsonb
from datetime import datetime, time
from typing import Any, Dict, List
import inject

from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.services.base.base_sessao_service import BaseSessaoService
from armazenamento.decorators.auth_class import auth_class
from armazenamento.context.app_context import current_user_types_list

from dados.paciente import Paciente
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador
from dados.sessao import Sessao
from greedy.wrapper import wrapper

@auth_class
class PacienteService(BasePacienteService):
    @inject.autoparams()
    def __init__(self, dal: DataAccessLayer):
        super().__init__(dal)
    
    def atualizar_acompanhamentos_com_sessoes(self, lista_acompanhamentos: List[Dict[str, int]], sessoes_atualizadas: list[dict[str, int | datetime]]) -> bool:
        _ = self._dal.call_procedure(
            "usp_paciente_alterar_acompanhamentos_com_sessoes",
            p_lista_acompanhamentos=Jsonb(lista_acompanhamentos),
            p_sessoes_atualizadas=Jsonb(sessoes_atualizadas)
        )

        return True

    def cadastrar_paciente(self, paciente: Paciente) -> int | None:
        """
        Implementação do método para cadastrar um novo paciente no sistema.

        Args:
            paciente: Objeto Paciente a ser cadastrado.
        """

        result = self._dal.call_procedure(
            "usp_paciente_inserir",
            p_nome=paciente.nome,
            p_email=paciente.email,
            p_data_nascimento=paciente.data_nascimento,
            p_id_pesquisador=paciente.pesquisador_responsavel.id_pessoa if paciente.pesquisador_responsavel else None,
            p_id_fisioterapeuta=paciente.fisioterapeuta_responsavel.id_pessoa if paciente.fisioterapeuta_responsavel else None,
            p_disponibilidades=Jsonb(
                [
                    {"dia": dia, "horarios": [h.isoformat() for h in horarios]}
                    for dia, horarios in enumerate(paciente.restricoes_paciente.disponibilidade_semanal)
                ]
            ),
            p_restricoes=Jsonb([dt.isoformat() for dt in paciente.restricoes_paciente.restricoes]),
            p_id_paciente=None
        )

        if result is None:
            return None

        return result['p_id_paciente'] if wrapper() else None

    def consultar(self, id: int) -> Paciente:
        row = self._dal.call_function("ufn_paciente_consultar", p_id_paciente=id)

        if row is None:
            return None

        fisio_result = row['fisioterapeuta']
        pesq_result = row['pesquisador']

        fisio: Fisioterapeuta | None = None if fisio_result is None else Fisioterapeuta(
            id_fisioterapeuta=fisio_result['id_usuario'],
            nome_fisioterapeuta=fisio_result['nome'],
            email=fisio_result['email'],
            data_nascimento=fisio_result['data_nascimento'],
            login=fisio_result['login'],
            senha=None,
            tipo=current_user_types_list.get()[1], # Tipo de Fisioterapeuta
            status_fisioterapeuta=fisio_result['ativo']
        )

        pesq: Pesquisador | None = None if pesq_result is None else Pesquisador(
            id_pesquisador=pesq_result['id_usuario'],
            nome_pesquisador=pesq_result['nome'],
            email=pesq_result['email'],
            data_nascimento=pesq_result['data_nascimento'],
            login=pesq_result['login'],
            senha=None,
            tipo=current_user_types_list.get()[2], # Tipo de Pesquisador
            status_pesquisador=pesq_result['ativo']
        )

        paciente = Paciente(
            id_paciente=row['id_paciente'],
            nome_paciente=row['nome'],
            email=row['email'],
            data_nascimento=row['data_nascimento'],
            pesquisador=pesq,
            fisioterapeuta=fisio,
            status_paciente=True
        )

        paciente.conclusao_pesquisa = row['status_conclusao']
        paciente.abandono_pesquisa = row['status_abandono']

        if paciente.abandono_pesquisa or paciente.conclusao_pesquisa:
            paciente.desabilitar_paciente()

        paciente.restricoes_paciente.disponibilidade_semanal = [set() for _ in range(7)]

        for disp in row["disponibilidades"] or []:
            dia: int = disp["dia"]           # 0..6
            horarios = disp["horarios"]      # list[str]

            paciente.restricoes_paciente.disponibilidade_semanal[dia] = {
                time.fromisoformat(h) for h in horarios
            }
        
        restricoes: set[datetime] = set(row['restricoes'] or [])
        paciente.restricoes_paciente.restricoes = restricoes
        
        for sessao_row in row['sessoes'] or []:
            sessao = Sessao(
                id_sessao=sessao_row['id_sessao'],
                codigo=sessao_row['cod_sigla'],
                dia=sessao_row['dia'],
                horario=sessao_row['horario'],
                conclusao=sessao_row['conclusao'],
                paciente=paciente,
                status_agendamento=sessao_row['status_agendamento']
            )

            paciente.sessoes_paciente.append(sessao)

        return paciente

    def listar_pacientes(self, apenas_ativos: bool) -> list[Paciente]:
        results = self._dal.call_function("ufn_paciente_listar", p_apenas_ativos=apenas_ativos)

        if results is None:
            return []

        final_list: list[Paciente] = []
        
        for row in results:
            fisio_result = row['fisioterapeuta']
            pesq_result = row['pesquisador']

            fisio: Fisioterapeuta | None = None if fisio_result is None else Fisioterapeuta(
                id_fisioterapeuta=fisio_result['id_usuario'],
                nome_fisioterapeuta=fisio_result['nome'],
                email=fisio_result['email'],
                data_nascimento=fisio_result['data_nascimento'],
                login=fisio_result['login'],
                senha=None,
                tipo=current_user_types_list.get()[1], # Tipo de Fisioterapeuta
                status_fisioterapeuta=fisio_result['ativo']
            )

            pesq: Pesquisador | None = None if pesq_result is None else Pesquisador(
                id_pesquisador=pesq_result['id_usuario'],
                nome_pesquisador=pesq_result['nome'],
                email=pesq_result['email'],
                data_nascimento=pesq_result['data_nascimento'],
                login=pesq_result['login'],
                senha=None,
                tipo=current_user_types_list.get()[2], # Tipo de Pesquisador
                status_pesquisador=pesq_result['ativo']
            )

            paciente = Paciente(
                id_paciente=row['id_paciente'],
                nome_paciente=row['nome'],
                email=row['email'],
                data_nascimento=row['data_nascimento'],
                pesquisador=pesq,
                fisioterapeuta=fisio,
                status_paciente=True
            )

            paciente.conclusao_pesquisa = row['status_conclusao']
            paciente.abandono_pesquisa = row['status_abandono']

            if paciente.abandono_pesquisa or paciente.conclusao_pesquisa:
                paciente.desabilitar_paciente()

            paciente.restricoes_paciente.disponibilidade_semanal = [set() for _ in range(7)]

            for disp in row["disponibilidades"] or []:
                dia: int = disp["dia"]           # 0..6
                horarios = disp["horarios"]      # list[str]

                paciente.restricoes_paciente.disponibilidade_semanal[dia] = {
                    time.fromisoformat(h) for h in horarios
                }

            restricoes: set[datetime] = set(row['restricoes'] or [])

            paciente.restricoes_paciente.restricoes = restricoes

            for sessao_row in row['sessoes'] or []:
                sessao = Sessao(
                    id_sessao=sessao_row['id_sessao'],
                    codigo=sessao_row['cod_sigla'],
                    dia=sessao_row['dia'],
                    horario=sessao_row['horario'],
                    conclusao=sessao_row['conclusao'],
                    paciente=paciente,
                    status_agendamento=sessao_row['status_agendamento']
                )

                paciente.sessoes_paciente.append(sessao)

            final_list.append(paciente)

        return final_list

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

    def atualizar_acompanhamentos(self, lista_acompanhamentos: List[Dict[str, int]]) -> bool:
        _ = self._dal.call_procedure(
            "usp_paciente_alterar_acompanhamentos",
            p_lista_acompanhamentos=Jsonb(lista_acompanhamentos)
        )

        return True
