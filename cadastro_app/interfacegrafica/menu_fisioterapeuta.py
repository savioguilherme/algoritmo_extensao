from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class MenuFisioterapeuta(BaseFrame):
     
    """Menu do fisioterapeuta"""

    def __init__(self, master, voltar_callback, abrir_agenda):
        super().__init__(master, titulo="Menu Fisioterapeuta")

        self.voltar_callback = voltar_callback
        self.abrir_agenda = abrir_agenda
        self.widgets = BaseWidgets()

        self.btn_agenda = self.widgets.button(self.container, texto="Agenda", comando=self.abrir_agenda, cor="blue")
        self.btn_agenda.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.btn_voltar = self.widgets.button(self.container, texto="Sair", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=0, sticky="e", padx=10, pady=10)