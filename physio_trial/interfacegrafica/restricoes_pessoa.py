from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class RestricoesPessoa(BaseFrame):

    """Tela para cadastro de restrições de agenda"""

    def __init__(self, master, voltar_callback):
        super().__init__(master, titulo="Restrições de Agenda")

        self.voltar_callback = voltar_callback
        self.widgets = BaseWidgets()

        self.label_dia = self.widgets.label(self, "Escolha o dia da semana: ", cor="transparent")
        self.label_dia.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        
        self.optionmenu_dia = self.widgets.option_menu(self, ["Segunda - Feira", "Terça - Feira", "Quarta - Feira", "Quinta - Feira","Sexta - Feira"], None)
        self.optionmenu_dia.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.label_horario = self.widgets.label(self, "Escolha o horário do dia: ", cor="transparent")
        self.label_horario.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        
        self.optionmenu_horario = self.widgets.option_menu(self, ["08:00h", "09:00h", "10:00h", "11:00h", "13:00h", "14:00h"], None)
        self.optionmenu_horario.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=3, column=0, sticky="w", padx=10, pady=10)