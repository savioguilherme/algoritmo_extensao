import customtkinter as ctk
import inject
from datetime import datetime, date, time, timedelta
from CTkMessagebox import CTkMessagebox
from typing import Dict, List

from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.services.base.base_sessao_service import BaseSessaoService
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador
from dados.sessao import Sessao
from interfacegrafica.agenda_pessoa.sessao_card import SessaoCard
from greedy.wrapper import wrapper


class AgendaPessoaWidget(ctk.CTkFrame):
    """
    Widget para exibir e gerenciar a agenda de sessões de um ou mais usuários.
    """

    @inject.params(paciente_service=BasePacienteService, sessao_service=BaseSessaoService, usuario_service=BaseUsuarioService)
    def __init__(self, master,
                 paciente_service: BasePacienteService,
                 sessao_service: BaseSessaoService,
                 usuario_service: BaseUsuarioService,
                 pesquisadores_ids: list[int] | None = None,
                 fisioterapeutas_ids: list[int] | None = None,
                 pacientes_ids: list[int] | None = None):
        super().__init__(master, fg_color="transparent")

        self.paciente_service = paciente_service
        self.sessao_service = sessao_service
        self.usuario_service = usuario_service
        self.pesquisadores_ids = pesquisadores_ids
        self.fisioterapeutas_ids = fisioterapeutas_ids
        self.pacientes_ids = pacientes_ids

        self.grid_columnconfigure(0, weight=1)
        self.sessao_cards: list[SessaoCard] = []

        self._carregar_sessoes()

    def _enumerar_sessao(self, codigo: str) -> int:
        """Retorna um valor numérico para ordenar as sessões na sequência correta."""
        if not codigo:
            return -1
        if codigo.startswith('S'):
            return int(codigo[1:])
        elif codigo == 'F00':
            return 9
        elif codigo == 'F01':
            return 10
        return -1

    def _classificar_sessao(self, codigo_sessao: str) -> tuple[bool, bool]:
        """
        Verifica se a sessão é para um pesquisador ou fisioterapeuta.
        Retorna (is_pesquisador, is_fisioterapeuta).
        """
        if codigo_sessao:
            if codigo_sessao.startswith('F') or codigo_sessao == "S08":
                return True, False  # Pesquisador
            return False, True  # Fisioterapeuta
        return False, False

    def _carregar_sessoes(self):
        """
        Carrega e filtra as sessões a serem exibidas, verificando conflitos de horário.
        """
        for card in self.sessao_cards:
            card.destroy()
        self.sessao_cards = []

        pacientes = self.paciente_service.listar_pacientes(apenas_ativos=True)
        sessoes_filtradas: list[Sessao] = []
        profissionais_ids = set()
        agenda_profissional: Dict[int, Dict[datetime, int]] = {}
        sessoes_por_paciente: Dict[int, List[Sessao]] = {}

        for paciente in pacientes:
            if self.pacientes_ids is not None and paciente.id_pessoa not in self.pacientes_ids:
                continue

            for sessao in paciente.sessoes_paciente:
                indice = self._enumerar_sessao(sessao.codigo)

                if indice >= 0:
                    if not sessao.paciente.id_pessoa in sessoes_por_paciente:
                        sessoes_por_paciente[sessao.paciente.id_pessoa] = [None] * 11
                    sessoes_por_paciente[sessao.paciente.id_pessoa][indice] = sessao

                is_pesq, is_fisio = self._classificar_sessao(sessao.codigo)

                passes_pesq_filter = True
                if is_pesq and self.pesquisadores_ids is not None and (paciente.pesquisador_responsavel is None or paciente.pesquisador_responsavel.id_pessoa not in self.pesquisadores_ids):
                    passes_pesq_filter = False

                passes_fisio_filter = True
                if is_fisio and self.fisioterapeutas_ids is not None and (paciente.fisioterapeuta_responsavel is None or paciente.fisioterapeuta_responsavel.id_pessoa not in self.fisioterapeutas_ids):
                    passes_fisio_filter = False

                if passes_pesq_filter and passes_fisio_filter:
                    sessoes_filtradas.append(sessao)
                    prof_id = None
                    if is_pesq and paciente.pesquisador_responsavel:
                        prof_id = paciente.pesquisador_responsavel.id_pessoa
                        profissionais_ids.add(prof_id)
                    elif is_fisio and paciente.fisioterapeuta_responsavel:
                        prof_id = paciente.fisioterapeuta_responsavel.id_pessoa
                        profissionais_ids.add(prof_id)

                    if prof_id and sessao.dia and sessao.horario:
                        dia_horario = datetime.combine(sessao.dia, sessao.horario)
                        if prof_id not in agenda_profissional:
                            agenda_profissional[prof_id] = {}
                        if dia_horario not in agenda_profissional[prof_id]:
                            agenda_profissional[prof_id][dia_horario] = 0
                        agenda_profissional[prof_id][dia_horario] += 1

        profissionais = {uid: self.usuario_service.consultar(uid) for uid in profissionais_ids}
        sessoes_filtradas.sort(key=lambda s: (s.dia or date.max, s.horario or time.max))

        for sessao in sessoes_filtradas:
            avisos = []
            dia_horario = datetime.combine(sessao.dia, sessao.horario) if sessao.dia and sessao.horario else None

            if dia_horario:
                if not sessao.paciente.restricoes_paciente.esta_disponivel(dia_horario):
                    avisos.append("Conflito de horário para o paciente.")

                is_pesq, is_fisio = self._classificar_sessao(sessao.codigo)
                prof_id, prof_obj, prof_tipo = (None, None, None)
                if is_pesq and sessao.paciente.pesquisador_responsavel:
                    prof_id = sessao.paciente.pesquisador_responsavel.id_pessoa
                    prof_obj = profissionais.get(prof_id)
                    if isinstance(prof_obj, Pesquisador) and not prof_obj.restricoes_pesquisador.esta_disponivel(dia_horario):
                        avisos.append("Conflito de horário para o pesquisador.")
                elif is_fisio and sessao.paciente.fisioterapeuta_responsavel:
                    prof_id = sessao.paciente.fisioterapeuta_responsavel.id_pessoa
                    prof_obj = profissionais.get(prof_id)
                    if isinstance(prof_obj, Fisioterapeuta) and not prof_obj.restricoes_fisioterapeuta.esta_disponivel(dia_horario):
                        avisos.append("Conflito de horário para o fisioterapeuta.")

                if prof_id and agenda_profissional.get(prof_id, {}).get(dia_horario, 0) > 1:
                    avisos.append("Profissional com outra sessão neste horário.")

            paciente_sessoes = sessoes_por_paciente[paciente.id_pessoa]
            indice_sessao = self._enumerar_sessao(sessao.codigo)
            print(paciente_sessoes) #dbg

            if sessao.codigo.startswith('S') and dia_horario and indice_sessao > 0:
                previous_session = paciente_sessoes[indice_sessao - 1]
                if previous_session.dia:
                    delta = sessao.dia - previous_session.dia
                    if delta.days <= 0:
                        avisos.append("Agendado no mesmo dia ou antes da sessão anterior.")
                    elif delta.days < 4:
                            avisos.append("Agendado em menos de 4 dias após a sessão anterior.")
                    elif 14 < delta.days:
                            avisos.append("Agendado em mais de 14 dias após sessão anterior.")

            if sessao.codigo.startswith('F') and dia_horario:
                sessao_inicial = paciente_sessoes[0]
                if sessao_inicial and sessao_inicial.dia:
                    delta_f = sessao.dia - sessao_inicial.dia
                    if sessao.codigo == 'F00':
                        if delta_f.days < 60:
                            avisos.append("Primeiro follow-up agendado menos de 60 dias após a sessão inicial.")
                        elif 120 < delta_f.days:
                            avisos.append("Primeiro follow-up agendado mais de 120 dias após a sessão inicial.")
                    if sessao.codigo == 'F01':
                        if delta_f.days < 150:
                            avisos.append("Segundo follow-up agendado menos de 150 dias após a sessão inicial.")
                        elif 210 < delta_f.days:
                            avisos.append("Segundo follow-up agendado mais de 210 dias após a sessão inicial.")

            card = SessaoCard(self, sessao, avisos=avisos)
            card.pack(fill="x", expand=True, padx=10, pady=5)
            self.sessao_cards.append(card)

    def salvar(self):
        """
        Coleta os dados de todos os cards de sessão e atualiza o dia e horário
        das sessões que tiveram dados alterados.
        """
        sessoes_modificadas = []
        agendamento_pendente = False
        dados_invalidos = False

        for card in self.sessao_cards:
            nova_sessao = card.get_data()
            if nova_sessao is None:
                dados_invalidos = True
                break

            if \
                nova_sessao.dia != card.sessao.dia or \
                nova_sessao.horario != card.sessao.horario or \
                nova_sessao.status_agendamento != card.sessao.status_agendamento or \
                nova_sessao.conclusao != card.sessao.conclusao:
                sessoes_modificadas.append(nova_sessao)

            if not nova_sessao.status_agendamento:
                agendamento_pendente = True

        if dados_invalidos:
            CTkMessagebox(title="Erro de Validação", message="Existem erros nos dados das sessões. Por favor, corrija-os antes de salvar.", icon="cancel")
            return

        if not sessoes_modificadas and not agendamento_pendente:
            CTkMessagebox(title="Informação", message="Nenhuma atualização a ser feita.", icon="info")
            return

        payload = []
        for sessao in sessoes_modificadas:
            dia_horario = None
            if sessao.dia and sessao.horario:
                dia_horario = datetime.combine(sessao.dia, sessao.horario)

            payload.append({
                'id_sessao': sessao.id_sessao,
                'dia_horario': dia_horario.isoformat() if dia_horario else None,
                'status_agendamento': sessao.status_agendamento,
                'conclusao': sessao.conclusao
            })

        try:
            if sessoes_modificadas:
                self.sessao_service.atualizar_sessoes_agendadas(payload)
        except Exception as e:
            CTkMessagebox(title="Erro", message="Ocorreu um erro ao atualizar as sessões", icon="cancel")
        else:
            try:
                if agendamento_pendente:
                    wrapper()
            except Exception as e:
                CTkMessagebox(title="Erro", message="Ocorreu um erro no auto-agendamento das sessões", icon="cancel")
            else:
                CTkMessagebox(title="Sucesso", message="Sessões atualizadas com sucesso!")
                self._carregar_sessoes() # Recarrega os dados para refletir as mudanças
