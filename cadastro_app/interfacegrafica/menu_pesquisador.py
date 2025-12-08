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

        self.btn_cadastrar_paci = self.widgets.button(self.container, texto="Cadastrar Paciente", comando=self.cadastro_paciente, cor="blue")
        self.btn_cadastrar_paci.grid(row=1, column=0, padx=10, pady=10)

        self.btn_agenda = self.widgets.button(self.container, texto="Agenda", comando=self.abrir_agenda, cor="blue")
        self.btn_agenda.grid(row=1, column=1, padx=10, pady=10)

        self.btn_restricoes = self.widgets.button(self.container, texto="Cadastrar Restrições Agenda", comando=self.abrir_restricoes, cor="blue")
        self.btn_restricoes.grid(row=1, column=2, sticky="w", padx=10, pady=10)

        self.btn_voltar = self.widgets.button(self.container, texto="Sair", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=2, padx=10, pady=10)