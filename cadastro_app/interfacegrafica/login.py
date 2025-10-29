import customtkinter
from interfacegrafica.base_frame import BaseFrame

class Login(BaseFrame):

    """   """

    def __init__(self, master, abrir_menu, encerrar):
        super().__init__(master, "Login")

        self.abrir_menu = abrir_menu
        self.encerrar = encerrar

        self.login = customtkinter.CTkLabel(self.container, text="Login: ", font=("Arial", 20, "bold"))
        self.login.grid(row=1, column=0, sticky="e", padx=20, pady=10)

        self.entry_login= customtkinter.CTkEntry(self.container)
        self.entry_login.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.senha = customtkinter.CTkLabel(self.container, text="Senha: ", font=("Arial", 20, "bold"))
        self.senha.grid(row=2, column=0, sticky="e", padx=20, pady=10)
        
        self.entry_senha= customtkinter.CTkEntry(self.container)
        self.entry_senha.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        botao_entrar = customtkinter.CTkButton(self.container, text="Entrar", width=250, height=40, command=self.abrir_menu, font=("Arial", 20, "bold"))
        botao_entrar.grid(row=3, column=0, padx=20, pady=20)

        botao_encerrar = customtkinter.CTkButton(self.container, text="Encerrar", width=250, height=40, command=self.encerrar, font=("Arial", 20, "bold"), fg_color="red")
        botao_encerrar.grid(row=3, column=1, padx=20, pady=20)