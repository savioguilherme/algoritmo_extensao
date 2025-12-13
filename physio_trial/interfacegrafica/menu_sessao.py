from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets

class MenuSessao(BaseFrame):
     
    """Menu de uma sessao"""

    def __init__(self, master, voltar_callback):
        super().__init__(master, titulo="Sessao: ") #trazer informações sobre essa sessao

        self.voltar_callback = voltar_callback
        self.widgets = BaseWidgets()

        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure(2, weight=1)
        
        
        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=1, sticky="e", padx=20, pady=20)