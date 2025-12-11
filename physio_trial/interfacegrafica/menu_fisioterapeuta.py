from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class MenuFisioterapeuta(BaseFrame):
     
    """Menu do fisioterapeuta"""

    def __init__(self, master, voltar_callback, abrir_agenda):
        super().__init__(master, titulo="Menu Fisioterapeuta")

        self.voltar_callback = voltar_callback
        self.abrir_agenda = abrir_agenda
        self.widgets = BaseWidgets()

        #configurando o frame
        self.grid_rowconfigure((0,1,2,3), weight=0)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.btn_agenda = self.widgets.button(self, texto="Agenda", comando=self.abrir_agenda, cor="blue")
        self.btn_agenda.grid(row=1, column=1, sticky="e", padx=20, pady=(20,10))

        self.btn_voltar = self.widgets.button(self, texto="Sair", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=1, sticky="e", padx=20, pady=(10,20))