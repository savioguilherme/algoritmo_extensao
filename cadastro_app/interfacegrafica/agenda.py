from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from datetime import datetime
import calendar

class Agenda(BaseFrame):

    """Agenda constanto todas as sessões de uma determinada pessoa"""

    def __init__(self, master, voltar_callback, pessoa):
        super().__init__(master, titulo="Agenda" + " " + pessoa)

        self.voltar_callback = voltar_callback
        self.pessoa = pessoa
        self.widgets = BaseWidgets()
        self.exibir_sessoes()

        self.btn_voltar = self.widgets.button(self.container, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=5, column=0, padx=10, pady=10)

    def buscar_sessoes(self):
        pass
    def exibir_sessoes(self):
        sessoes = [
        {"Código": 1,  "Horário": "14:00", "Paciente": "Cleiton"},
        {"Código": 2,  "Horário": "14:00", "Paciente": "Cleiton"},
        {"Código": 3,  "Horário": "14:00", "Paciente": "Cleiton"},
        {"Código": 4,  "Horário": "14:00", "Paciente": "Cleiton"},
        ]
        x = 0
        for s in sessoes:
            texto = f"Código da Sessão: {s['Código']}, Horário: {s['Horário']}, Paciente: {s['Paciente']}"
            self.label_sessao = self.widgets.label(self.container, texto=texto, cor="Blue")
            self.label_sessao.grid(row=x, column=0, padx=10, pady=10)
            x = x + 1
    
    