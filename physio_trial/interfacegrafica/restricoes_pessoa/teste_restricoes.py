import customtkinter as ctk

from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.restricoes_pessoa.restricoes_pessoa import RestricoesPessoa

class TesteRestricoes(BaseFrame):
    """Tela para testar o widget de restrições de agenda."""

    def __init__(self, master, voltar_callback=None, salvar_callback=None, restricoes=None):
        super().__init__(master, titulo="Teste Restrições de Agenda")

        self.salvar_callback = salvar_callback

        # configurando o frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        scrollable_frame = ctk.CTkScrollableFrame(self)
        scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        self.restricoes_widget = RestricoesPessoa(scrollable_frame, restricoes=restricoes)
        self.restricoes_widget.grid(row=0, column=0, sticky="nsew")

        # --- Botões de Ação ---
        action_buttons_frame = ctk.CTkFrame(self)
        action_buttons_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        action_buttons_frame.grid_columnconfigure((0, 1), weight=1)

        btn_voltar = ctk.CTkButton(action_buttons_frame, text="Voltar", command=voltar_callback)
        btn_voltar.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        btn_salvar = ctk.CTkButton(action_buttons_frame, text="Salvar", command=self._salvar)
        btn_salvar.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

    def _salvar(self):
        dados = self.restricoes_widget.get_dados()
        if self.salvar_callback:
            self.salvar_callback(dados)
