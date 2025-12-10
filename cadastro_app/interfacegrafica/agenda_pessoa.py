from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from datetime import datetime
import calendar

class AgendaPessoa(BaseFrame):

    """Agenda constanto todas as sessões de uma determinada pessoa"""

    def __init__(self, master, voltar_callback, pessoa):
        super().__init__(master, titulo="Agenda" + " " + pessoa)

        self.voltar_callback = voltar_callback
        self.pessoa = pessoa
        self.widgets = BaseWidgets()
        self.frame_auxiliar = self.widgets.frame(self)
        self.frame_auxiliar.grid(row=1, column=0, columnspan=4, sticky="nsew")
        self.frame_auxiliar.grid_columnconfigure((0,1,2,3), weight=1)
        self.frame_auxiliar.grid_rowconfigure((0,1,2,3), weight=1)
        self.exibir_sessoes()

        #self.btn_restricoes = self.widgets.button(self, texto="Provisório", comando=None, cor="blue")
        #self.btn_restricoes.grid(row=2, column=2, sticky="w", padx=10, pady=10)

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=2, sticky="w", padx=10, pady=10)
    def buscar_sessoes(self):
        pass
    def exibir_sessoes(self):
        sessoes = [
        {"Código": 1,  "Horário": "14:00", "Paciente": "Cleiton"},
        {"Código": 2,  "Horário": "14:00", "Paciente": "Cleiton"},
        {"Código": 3,  "Horário": "14:00", "Paciente": "Cleiton"},
        {"Código": 4,  "Horário": "14:00", "Paciente": "Cleiton"},
        ]
        for i, s in enumerate(sessoes):
            texto = f"Código da Sessão: {s['Código']}, Horário: {s['Horário']}, Paciente: {s['Paciente']}"
            self.label_sessao = self.widgets.label(self.frame_auxiliar, texto=texto, cor="Blue")
            self.label_sessao.grid(row=i, column=0, sticky="w", padx=10, pady=10)