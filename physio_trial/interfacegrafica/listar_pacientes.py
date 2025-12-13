from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class ListarPacientes(BaseFrame):
    '''Lista todos os pacientes cadastrados'''

    def __init__(self, master, pacientes, voltar_callback, abrir_menu_paciente):
        super().__init__(master, "Lista de Pacientes")

        self.pacientes = pacientes
        self.voltar_callback = voltar_callback
        self.abrir_menu_paciente = abrir_menu_paciente
        self.widgets = BaseWidgets()

        self._configurar_layout()
        self._criar_lista_pacientes()
        self._criar_botao_voltar()

    def _configurar_layout(self):
        self.grid_columnconfigure((1,2), weight=1)

    def _criar_lista_pacientes(self):
        if not self.pacientes:
            label = self.widgets.label(self, texto="Nenhum paciente cadastrado.", cor="transparent")
            label.grid(row=1, column=1, columnspan=3, pady=20)
            return

        for i, paciente in enumerate(self.pacientes):
            btn = self.widgets.button(self, texto=paciente.nome, comando=lambda p=paciente: self.abrir_menu_paciente(p), cor="blue")
            btn.grid(row=i+1, column=2, sticky="ew", pady=5, padx=20)

    def _criar_botao_voltar(self):
        btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        btn_voltar.grid(row=99, column=1, pady=20)