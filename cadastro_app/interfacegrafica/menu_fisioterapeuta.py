import customtkinter
from interfacegrafica.base_frame import BaseFrame

class MenuFisioterapeuta(BaseFrame):
     
    """Menu principal"""

    def __init__(self, master, voltar_callback, abrir_tela_fisioterapeuta):
        super().__init__(master, titulo="Menu Fisioterapeuta")

        self.voltar_callback = voltar_callback
        self.abrir_tela_fisioterapeuta = abrir_tela_fisioterapeuta

        self.btn = customtkinter.CTkButton(self.container, text="Cadastrar Fisioterapeuta", width=250, height=40, command=self.abrir_tela_fisioterapeuta, font=("Arial", 20, "bold"))
        self.btn.grid(row=1, column=0, padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", width=250, height=40, command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=1, column=1, padx=20, pady=20)