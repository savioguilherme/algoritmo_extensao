from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class MenuPaciente(BaseFrame):
     
    """Menu do paciente"""

    def __init__(self, master, voltar_callback):
        super().__init__(master, titulo="Menu Paciente")

        self.voltar_callback = voltar_callback
        self.widgets = BaseWidgets()
        
        #self.btn_fisioterapeuta = self.widgets.button(self, texto="Cadastrar Fisioterapeuta", comando=self.cadastro_fisioterapeuta, cor="blue")
        #self.btn_fisioterapeuta.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        #self.btn_pesquisador = self.btn_cadastrar_paci = self.widgets.button(self, texto="Cadastrar Pesquisador", comando=self.cadastro_pesquisador, cor="blue")
        #self.btn_pesquisador.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        #self.btn_listar_fisioterapeuta = self.widgets.button(self, texto="Listar Fisioterapeutas", comando=self.listar_fisioterapeutas, cor="blue")
        #self.btn_listar_fisioterapeuta.grid(row=1, column=2, sticky="w", padx=10, pady=10)

        #self.btn_listar_pesquisadores = self.widgets.button(self, texto="Listar Pesquisadores", comando=self.listar_pesquisadores, cor="blue")
        #self.btn_listar_pesquisadores.grid(row=1, column=3, sticky="w", padx=10, pady=10)

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=1, sticky="e", padx=10, pady=10)