from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class RestricoesPessoa(BaseFrame):

    """Tela para cadastro de restrições de agenda"""

    def __init__(self, master, voltar_callback):
        super().__init__(master, titulo="Restrições de Agenda")

        self.voltar_callback = voltar_callback
        self.widgets = BaseWidgets()

        #configurando o frame
        self.grid_rowconfigure((1,2,3,4,5), weight=0)
        self.grid_columnconfigure((1,2,3,4,5), weight=1)

        self.label_dia = self.widgets.label(self, "Escolha um dia da semana: ", cor="transparent")
        self.label_dia.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.optionmenu_dia = self.widgets.option_menu(self, ["Selecione", "Segunda - Feira", "Terça - Feira", "Quarta - Feira", "Quinta - Feira", "Sexta - Feira"], None)
        self.optionmenu_dia.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_dia_especificio = self.widgets.label(self, "Ou, Insira um dia específico: ", cor="transparent")
        self.label_dia_especificio.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_dia_especificio = self.widgets.entry(self, None, "DD/MM/AAAA")
        self.entry_dia_especificio.grid(row=2, column=2, sticky="w",padx=(10,20), pady=(10,10))

        self.label_horario_ini = self.widgets.label(self, "Escolha o intervalo de horario desse dia: ", cor="transparent")
        self.label_horario_ini.grid(row=3, column=1, sticky="e", padx=(20,10), pady=(10,10))
        
        self.optionmenu_horario_ini = self.widgets.option_menu(self, ["Selecione", "08:00h", "09:00h", "10:00h", "11:00h", "13:00h", "14:00h", "15:00h", "16:00h", "17:00h", "18:00h" ], None)
        self.optionmenu_horario_ini.grid(row=3, column=2, sticky="w",padx=(10,20), pady=(10,10))

        self.label_horario_fim = self.widgets.label(self, "Até:  ", cor="transparent")
        self.label_horario_fim.grid(row=4, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.optionmenu_horario_fim = self.widgets.option_menu(self, ["Selecione", "08:00h", "09:00h", "10:00h", "11:00h", "13:00h", "14:00h", "15:00h", "16:00h", "17:00h", "18:00h" ], None)
        self.optionmenu_horario_fim.grid(row=4, column=2, sticky="w",padx=(10,20), pady=(10,10))

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.pegar_dia_horario, cor="blue")
        self.btn_salvar.grid(row=5, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=5, column=2, sticky="w", padx=(10,20), pady=(10,20))

    def pegar_dia_horario(self):
        dia = self.optionmenu_dia.get()
        horarioini = self.optionmenu_horario_ini.get()
        horariofim = self.optionmenu_horario_fim.get()
        print(horarioini)
        print(horariofim)
        print(dia)