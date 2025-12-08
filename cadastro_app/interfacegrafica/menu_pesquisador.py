import customtkinter
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class MenuPesquisador(BaseFrame):

    """Menu do pesquisador"""

    def __init__(self, master, voltar_callback, cadastro_paciente, abrir_agenda, abrir_restricoes):
        super().__init__(master, titulo="Menu Pesquisador")

        self.voltar_callback = voltar_callback
        self.cadastro_paciente = cadastro_paciente
        self.abrir_agenda = abrir_agenda
        self.abrir_restricoes = abrir_restricoes
        self.widgets = BaseWidgets()

        self.btn = customtkinter.CTkButton(self.container, text="Cadastrar Paciente", width=250, height=40, command=self.cadastro_paciente, font=("Arial", 20, "bold"))
        self.btn.grid(row=1, column=0, padx=10, pady=10)

        self.btn_agenda = customtkinter.CTkButton(self.container, text="Agenda", width=250, height=40, command=self.abrir_agenda, font=("Arial", 20, "bold"))
        self.btn_agenda.grid(row=1, column=1, padx=10, pady=10)

        self.btn_restricoes = self.widgets.button(self.container, texto="Cadastrar Restrições Agenda", comando=self.abrir_restricoes, cor="blue")
        self.btn_restricoes.grid(row=1, column=2, sticky="w", padx=10, pady=10)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Sair", width=250, height=40, command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=2, column=2, padx=10, pady=10)