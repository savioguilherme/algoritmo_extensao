import customtkinter
from interfacegrafica.base_frame import BaseFrame

class MenuAdministrador(BaseFrame):
     
    """Menu principal"""

    def __init__(self, master, voltar_callback, cadastro_fisioterapeuta, cadastro_pesquisador):
        super().__init__(master, titulo="Menu Administrador")

        self.voltar_callback = voltar_callback
        self.cadastro_fisioterapeuta = cadastro_fisioterapeuta
        self.cadastro_pesquisador = cadastro_pesquisador

        self.btn_pesquisador = customtkinter.CTkButton(self.container, text="Cadastrar Pesquisador", width=250, height=40, command=self.cadastro_pesquisador, font=("Arial", 20, "bold"))
        self.btn_pesquisador.grid(row=1, column=0, padx=20, pady=20)

        self.btn_fisioterapeuta = customtkinter.CTkButton(self.container, text="Cadastrar Fisioterapeuta", width=250, height=40, command=self.cadastro_fisioterapeuta, font=("Arial", 20, "bold"))
        self.btn_fisioterapeuta.grid(row=1, column=1, padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", width=250, height=40, command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=1, column=2, padx=20, pady=20)