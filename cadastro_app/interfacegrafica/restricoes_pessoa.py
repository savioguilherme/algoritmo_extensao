from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class RestricoesPessoa(BaseFrame):

    """Tela para cadastro de restrições de agenda"""

    def __init__(self, master, voltar_callback):
        super().__init__(master, titulo="Restrições de Agenda")

        self.voltar_callback = voltar_callback
        self.widgets = BaseWidgets()

        self.btn_voltar = self.widgets.button(self.container, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=1, column=0, sticky="w", padx=10, pady=10)