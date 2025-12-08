from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class Agenda(BaseFrame):

    """Agenda constanto todas as sessões de uma determinada pessoa"""

    def __init__(self, master, voltar_callback, pessoa):
        super().__init__(master, titulo="Agenda" + " " + pessoa)

        self.voltar_callback = voltar_callback
        self.pessoa = pessoa
        self.widgets = BaseWidgets()

        self.btn_voltar = self.widgets.button(self.container, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=0, padx=10, pady=10)