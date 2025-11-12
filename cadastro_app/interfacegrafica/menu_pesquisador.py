import customtkinter
from interfacegrafica.base_frame import BaseFrame

class MenuPesquisador(BaseFrame):

    """Menu principal"""

    def __init__(self, master, voltar_callback, cadastro_paciente):
        super().__init__(master, titulo="Menu Pesquisador")

        self.voltar_callback = voltar_callback
        self.cadastro_paciente = cadastro_paciente

        self.btn = customtkinter.CTkButton(self.container, text="Cadastrar Paciente", width=250, height=40, command=self.cadastro_paciente, font=("Arial", 20, "bold"))
        self.btn.grid(row=1, column=1, padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Sair", width=250, height=40, command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=1, column=2, padx=20, pady=20)

        def listar_pacientes(self): 
            pass