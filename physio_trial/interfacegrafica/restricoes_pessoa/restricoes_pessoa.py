import customtkinter as ctk
from datetime import datetime, time
from typing import Dict, List

from interfacegrafica.base_widgets import BaseWidgets
from interfacegrafica.restricoes_pessoa.restricao_card import RestricaoCard
from interfacegrafica.restricoes_pessoa.disponibilidade_semanal_tabela import DisponibilidadeSemanalTabela
from dados.restricoes_dias_horarios import RestricoesDiasHorarios


class RestricoesPessoa(ctk.CTkFrame):
    """Widget para cadastro de restrições de agenda."""

    def __init__(self, master, restricoes: RestricoesDiasHorarios | None = None):
        super().__init__(master, fg_color="transparent")

        if restricoes is None:
            restricoes = RestricoesDiasHorarios()

        self.widgets = BaseWidgets()
        self.grid_columnconfigure(0, weight=1)

        # --- Frame de Disponibilidades ---
        disponibilidades_outer_frame = ctk.CTkFrame(self, fg_color="transparent")
        disponibilidades_outer_frame.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")
        disponibilidades_outer_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(disponibilidades_outer_frame, text="Disponibilidades Semanais", font=("Arial", 16, "bold")).pack(pady=5)

        # Convert data and create the availability table
        initial_table_data = self._convert_restricoes_to_table_data(restricoes)
        for horario in [time(8),time(10),time(13),time(14)]:
            if not horario in initial_table_data:
                initial_table_data[horario] = [False] * 7
        self.disponibilidade_tabela = DisponibilidadeSemanalTabela(disponibilidades_outer_frame, initial_data=initial_table_data)
        self.disponibilidade_tabela.pack(fill="x", expand=True, padx=5)

        # Button to add a new row (time) to the table
        btn_add_disp = self.widgets.button(disponibilidades_outer_frame, texto="Adicionar Horário", comando=self.disponibilidade_tabela.adicionar_linha, cor="blue")
        btn_add_disp.pack(pady=10)

        # --- Frame de Restrições (Specific one-time restrictions) ---
        restricoes_outer_frame = ctk.CTkFrame(self, fg_color="transparent")
        restricoes_outer_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        restricoes_outer_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(restricoes_outer_frame, text="Restrições", font=("Arial", 16, "bold")).pack(pady=5)

        self.restricoes_frame = ctk.CTkFrame(restricoes_outer_frame, fg_color="transparent", height=0)
        self.restricoes_frame.pack(fill="x", expand=True, padx=5)

        self.restricoes_cards = []
        if restricoes.restricoes:
            for restricao_dt in sorted(list(restricoes.restricoes)):
                self._adicionar_restricao_card(restricao_dt)

        #btn_add_rest = ctk.CTkButton(restricoes_outer_frame, text="Adicionar Restrição", command=self._adicionar_restricao_card)
        
        btn_add_rest = self.widgets.button(restricoes_outer_frame, "Adicionar Restrição", self._adicionar_restricao_card, "blue")
        btn_add_rest.pack(pady=10)

    def _convert_restricoes_to_table_data(self, restricoes: RestricoesDiasHorarios) -> Dict[time, List[bool]]:
        """Converts a RestricoesDiasHorarios object to the dict format for the table widget."""
        table_data = {}
        for dia_semana, horarios in enumerate(restricoes.disponibilidade_semanal):
            for horario in horarios:
                if not horario in table_data:
                    table_data[horario] = [False] * 7
                table_data[horario][dia_semana] = True
        return table_data

    def _adicionar_restricao_card(self, data: datetime | None = None):
        """Adds a new card for a specific one-time restriction."""
        if data is None:
            data = datetime.now().replace(second=0, microsecond=0)

        card = RestricaoCard(
            parent=self.restricoes_frame,
            data=data
        )
        card.set_delete_callback(lambda: self._remover_card(card, self.restricoes_cards))
        card.pack(fill="x", expand=True, pady=5)
        self.restricoes_cards.append(card)

    def _remover_card(self, card: ctk.CTkFrame, card_list: list):
        """Removes a card from the UI and the tracking list."""
        card.destroy()
        if card in card_list:
            card_list.remove(card)

    def get_dados(self) -> RestricoesDiasHorarios | None:
        """
        Retrieves and validates all data from the widgets.
        Returns a RestricoesDiasHorarios object or None if any validation fails.
        """
        novas_restricoes = RestricoesDiasHorarios()
        has_error = False

        # Get data from the availability table
        table_data = self.disponibilidade_tabela.get_data()
        if table_data is None:
            has_error = True
        else:
            for horario, availability_list in table_data.items():
                for dia_semana, is_available in enumerate(availability_list):
                    if is_available:
                        novas_restricoes.adicionar_disponibilidade(dia_semana, horario)

        # Get data from the one-time restriction cards
        for card in self.restricoes_cards:
            data = card.get_data()
            if data:
                novas_restricoes.adicionar_restricao(data)
            else:
                has_error = True

        if has_error:
            return None

        return novas_restricoes
