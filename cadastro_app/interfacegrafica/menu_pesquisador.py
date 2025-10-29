import customtkinter
from interfacegrafica.base_frame import BaseFrame

class MenuPesquisador(BaseFrame):

    """Menu principal"""

    def __init__(self, master, voltar_callback, abrir_tela_paciente):
        super().__init__(master, titulo="Menu Pesquisador")

        self.voltar_callback = voltar_callback
        self.abrir_tela_paciente = abrir_tela_paciente

        self.btn = customtkinter.CTkButton(self.container, text="Cadastrar Paciente", width=250, height=40, command=self.abrir_tela_paciente, font=("Arial", 20, "bold"))
        self.btn.grid(row=1, column=1, padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", width=250, height=40, command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=1, column=2, padx=20, pady=20)