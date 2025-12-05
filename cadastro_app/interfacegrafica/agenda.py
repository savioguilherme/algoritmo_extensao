import customtkinter
from interfacegrafica.base_frame import BaseFrame

class Agenda(BaseFrame):

    """Agenda constanto todas as sessões de uma determinada pessoa"""

    def __init__(self, master, voltar_callback, pessoa):
        super().__init__(master, titulo="Agenda" + " " + pessoa)

        self.voltar_callback = voltar_callback
        self.pessoa = pessoa

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", width=250, height=40, command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=2, column=0, padx=20, pady=20)