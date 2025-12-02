import customtkinter
from interfacegrafica.base_frame import BaseFrame

class Agenda(BaseFrame):

    """Agenda"""

    def __init__(self, master, voltar_callback):
        super().__init__(master, titulo="Agenda")

        self.voltar_callback = voltar_callback

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", width=250, height=40, command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=1, column=2, padx=20, pady=20)
        