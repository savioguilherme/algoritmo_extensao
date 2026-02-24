import customtkinter as ctk
import inject
from datetime import datetime, date, time
from CTkMessagebox import CTkMessagebox

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

    def _classificar_sessao(self, codigo_sessao: str) -> tuple[bool, bool]:
        """
        Verifica se a sessão é para um pesquisador ou fisioterapeuta.
        Retorna (is_pesquisador, is_fisioterapeuta).
        """
        if codigo_sessao:
            if codigo_sessao.startswith("F") or codigo_sessao == "S08":
                return True, False  # Pesquisador
            return False, True  # Fisioterapeuta
        return False, False

    def _carregar_sessoes(self):
        """
        Carrega e filtra as sessões a serem exibidas, verificando conflitos de horário.
        """
        # Limpa cards existentes antes de carregar novos
        for card in self.sessao_cards:
            card.destroy()
        self.sessao_cards = []

        # Obter pacientes e sessões filtradas
        pacientes = self.paciente_service.listar_pacientes(apenas_ativos=False)
        sessoes_filtradas: list[Sessao] = []
        profissionais_ids = set()

        for paciente in pacientes:
            if self.pacientes_ids is not None and paciente.id_pessoa not in self.pacientes_ids:
                continue

            for sessao in paciente.sessoes_paciente:
                is_pesquisador_session, is_fisio_session = self._classificar_sessao(sessao.codigo)

                print("sessao recebida {} {}: {} {}".format(sessao.paciente.id_pessoa, sessao.codigo, sessao.status_agendamento, sessao.conclusao)) #dbg

                passes_pesquisador_filter = True
                if is_pesquisador_session and self.pesquisadores_ids is not None:
                    if paciente.pesquisador_responsavel is None or \
                       paciente.pesquisador_responsavel.id_pessoa not in self.pesquisadores_ids:
                        passes_pesquisador_filter = False

                passes_fisioterapeuta_filter = True
                if is_fisio_session and self.fisioterapeutas_ids is not None:
                    if paciente.fisioterapeuta_responsavel is None or \
                       paciente.fisioterapeuta_responsavel.id_pessoa not in self.fisioterapeutas_ids:
                        passes_fisioterapeuta_filter = False

                if passes_pesquisador_filter and passes_fisioterapeuta_filter:
                    sessoes_filtradas.append(sessao)
                    if paciente.pesquisador_responsavel:
                        profissionais_ids.add(paciente.pesquisador_responsavel.id_pessoa)
                    if paciente.fisioterapeuta_responsavel:
                        profissionais_ids.add(paciente.fisioterapeuta_responsavel.id_pessoa)

        # Obter dados completos dos profissionais com suas restrições
        profissionais = {uid: self.usuario_service.consultar(uid) for uid in profissionais_ids}

        # Ordenar sessoes e criar cards com avisos
        sessoes_filtradas.sort(key=lambda s: (s.dia or date.max, s.horario or time.max))

        for sessao in sessoes_filtradas:
            avisos = []
            if sessao.dia and sessao.horario:
                dia_horario = datetime.combine(sessao.dia, sessao.horario)

                # Checar disponibilidade do paciente
                if not sessao.paciente.restricoes_paciente.esta_disponivel(dia_horario):
                    avisos.append(f"Conflito de horário para o paciente.")

                is_pesquisador_session, is_fisio_session = self._classificar_sessao(sessao.codigo)

                # Checar disponibilidade do Fisioterapeuta
                if is_fisio_session and sessao.paciente.fisioterapeuta_responsavel:
                    fisio = profissionais.get(sessao.paciente.fisioterapeuta_responsavel.id_pessoa)
                    if not fisio.restricoes_fisioterapeuta.esta_disponivel(dia_horario):
                         avisos.append(f"Conflito de horário para o fisioterapeuta.")

                # Checar disponibilidade do Pesquisador
                if is_pesquisador_session and sessao.paciente.pesquisador_responsavel:
                    pesq = profissionais.get(sessao.paciente.pesquisador_responsavel.id_pessoa)
                    if not pesq.restricoes_pesquisador.esta_disponivel(dia_horario):
                        avisos.append(f"Conflito de horário para o pesquisador.")

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

            print("sessao enviada {} {}: {} {}".format(sessao.paciente.id_pessoa, sessao.codigo, sessao.status_agendamento, sessao.conclusao)) #dbg

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
                    print("agenda widget pre wrapper")
                    wrapper()
                    print("agenda widget post wrapper")
            except Exception as e:
                CTkMessagebox(title="Erro", message="Ocorreu um erro no auto-agendamento das sessões", icon="cancel")
            else:
                CTkMessagebox(title="Sucesso", message="Sessões atualizadas com sucesso!")
                self._carregar_sessoes() # Recarrega os dados para refletir as mudanças
