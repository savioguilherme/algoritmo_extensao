from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class MenuPaciente(BaseFrame):
    """Menu do paciente"""

    def __init__(self, master, voltar_callback):
        super().__init__(master, titulo="Menu Paciente")

        self.voltar_callback = voltar_callback
        self.widgets = BaseWidgets()

        #configurando o frame
        self.grid_rowconfigure((1,2,3,4,5,6), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)
        
        self.label_nome = self.widgets.label(janela=self, texto="Nome do Paciente", cor="transparent")
        self.label_nome.grid(row=1, column=1, sticky="e", padx=(20,20), pady=(20,10))

        self.label_fisioterapeuta = self.widgets.label(janela=self, texto="Nome do fisio", cor="transparent")
        self.label_fisioterapeuta.grid(row=2, column=1, sticky="e", padx=(20,20), pady=(10,10))
        
        self.label_pesquisador = self.widgets.label(janela=self, texto="Nome do pesqui", cor="transparent")
        self.label_pesquisador.grid(row=3, column=1, sticky="e", padx=(20,20), pady=(10,20))

        self.label_status = self.widgets.label(janela=self, texto="ativo/não-ativo", cor="transparent")
        self.label_status.grid(row=4, column=1, sticky="e", padx=(20,20), pady=(10,20))

        self.label_sessao = self.widgets.label(janela=self, texto="sessao tal", cor="transparent")
        self.label_sessao.grid(row=5, column=1, sticky="e", padx=(20,20), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=6, column=1, sticky="e", padx=20, pady=20)