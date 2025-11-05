import customtkinter
from interfacegrafica.base_frame import BaseFrame

class MenuAdministrador(BaseFrame):
     
    """Menu principal"""

    def __init__(self, master, voltar_callback, cadastro_fisioterapeuta, cadastro_pesquisador, listar_fisioterapeutas, listar_pesquisadores):
        super().__init__(master, titulo="Menu Administrador")

        self.voltar_callback = voltar_callback
        self.cadastro_fisioterapeuta = cadastro_fisioterapeuta
        self.cadastro_pesquisador = cadastro_pesquisador
        self.listar_fisioterapeutas = listar_fisioterapeutas
        self.listar_pesquisadores = listar_pesquisadores

        self.btn_pesquisador = customtkinter.CTkButton(self.container, text="Cadastrar Pesquisador", width=250, height=40, command=self.cadastro_pesquisador, font=("Arial", 20, "bold"))
        self.btn_pesquisador.grid(row=1, column=0, padx=20, pady=20)

        self.btn_fisioterapeuta = customtkinter.CTkButton(self.container, text="Cadastrar Fisioterapeuta", width=250, height=40, command=self.cadastro_fisioterapeuta, font=("Arial", 20, "bold"))
        self.btn_fisioterapeuta.grid(row=1, column=1, padx=20, pady=20)

        self.btn_listar_fisioterapeuta = customtkinter.CTkButton(self.container, text="Listar Fisioterapeutas", width=250, height=40, command=self.listar_fisioterapeutas, font=("Arial", 20, "bold"))
        self.btn_listar_fisioterapeuta.grid(row=2, column=0, padx=20, pady=20)

        self.btn_listar_pesquisadores = customtkinter.CTkButton(self.container, text="Listar Pesquisadores", width=250, height=40, command=self.listar_pesquisadores, font=("Arial", 20, "bold"))
        self.btn_listar_pesquisadores.grid(row=2, column=1, padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Encerrar", width=250, height=40, command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=3, column=0, padx=20, pady=20)