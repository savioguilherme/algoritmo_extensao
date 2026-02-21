import customtkinter as ctk
from datetime import datetime

from interfacegrafica.base_widgets import BaseWidgets
from interfacegrafica.restricoes_pessoa.restricao_card import RestricaoCard
from interfacegrafica.restricoes_pessoa.disponibilidade_semanal_card import DisponibilidadeSemanalCard
from dados.restricoes_dias_horarios import RestricoesDiasHorarios


class RestricoesPessoa(ctk.CTkFrame):
    """Widget para cadastro de restrições de agenda."""

    def __init__(self, master, restricoes=None):
        super().__init__(master, fg_color="transparent")

        if restricoes is None:
            restricoes = RestricoesDiasHorarios()

        self.widgets = BaseWidgets()

        self.grid_columnconfigure(0, weight=1)

        # Frame de Disponibilidades
        disponibilidades_outer_frame = ctk.CTkFrame(self, fg_color="transparent")
        disponibilidades_outer_frame.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")
        disponibilidades_outer_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(disponibilidades_outer_frame, text="Disponibilidades Semanais", font=("Arial", 16, "bold")).pack(pady=5)

        self.disponibilidades_frame = ctk.CTkFrame(disponibilidades_outer_frame, fg_color="transparent", height=0)
        self.disponibilidades_frame.pack(fill="x", expand=True, padx=5)

        self.disponibilidade_cards = []
        if restricoes.disponibilidade_semanal:
            for dia_semana, horarios in enumerate(restricoes.disponibilidade_semanal):
                for horario in sorted(list(horarios)):  # sort for consistent order
                    self._adicionar_disponibilidade_card(dia_semana, horario)

        #btn_add_disp = ctk.CTkButton(disponibilidades_outer_frame, text="Adicionar Disponibilidade", command=self._adicionar_disponibilidade_card)
        #btn_add_disp.pack(pady=10)

        btn_add_disp = self.widgets.button(disponibilidades_outer_frame, texto="Adicionar Disponibilidades", comando=self._adicionar_disponibilidade_card, cor="blue")
        btn_add_disp.pack(pady=10)

        # Frame de Restrições
        restricoes_outer_frame = ctk.CTkFrame(self, fg_color="transparent")
        restricoes_outer_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        restricoes_outer_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(restricoes_outer_frame, text="Restrições", font=("Arial", 16, "bold")).pack(pady=5)

        self.restricoes_frame = ctk.CTkFrame(restricoes_outer_frame, fg_color="transparent", height=0)
        self.restricoes_frame.pack(fill="x", expand=True, padx=5)

        self.restricoes_cards = []
        if restricoes.restricoes:
            for restricao_dt in sorted(list(restricoes.restricoes)):  # sort
                self._adicionar_restricao_card(restricao_dt)

        #btn_add_rest = ctk.CTkButton(restricoes_outer_frame, text="Adicionar Restrição", command=self._adicionar_restricao_card)
        
        btn_add_rest = self.widgets.button(restricoes_outer_frame, "Adicionar Restrição", self._adicionar_restricao_card, "blue")
        btn_add_rest.pack(pady=10)

    def _adicionar_disponibilidade_card(self, day=None, time_obj=None):
        if day is None:
            day = datetime.now().weekday()
        if time_obj is None:
            time_obj = datetime.now().time().replace(second=0, microsecond=0)

        card = DisponibilidadeSemanalCard(
            parent=self.disponibilidades_frame,
            day=day,
            time_obj=time_obj
        )
        card.set_delete_callback(lambda: self._remover_card(card, self.disponibilidade_cards))
        card.pack(fill="x", expand=True, pady=5)
        self.disponibilidade_cards.append(card)

    def _adicionar_restricao_card(self, data=None):
        if data is None:
            data = datetime.now().replace(second=0, microsecond=0)

        card = RestricaoCard(
            parent=self.restricoes_frame,
            data=data
        )
        card.set_delete_callback(lambda: self._remover_card(card, self.restricoes_cards))
        card.pack(fill="x", expand=True, pady=5)
        self.restricoes_cards.append(card)

    def _remover_card(self, card, card_list):
        card.destroy()
        if card in card_list:
            card_list.remove(card)

    def get_dados(self):
        novas_restricoes = RestricoesDiasHorarios()
        has_error = False

        for card in self.disponibilidade_cards:
            data = card.get_data()
            if data:
                dia_semana, horario = data
                novas_restricoes.adicionar_disponibilidade(dia_semana, horario)
            else:
                has_error = True

        for card in self.restricoes_cards:
            data = card.get_data()
            if data:
                novas_restricoes.adicionar_restricao(data)
            else:
                has_error = True

        if has_error:
            return None

        return novas_restricoes
