import customtkinter
from tkinter import messagebox
from armazenamento.autenticacao import Autenticacao
from interfacegrafica.base_frame import BaseFrame

class Login(BaseFrame):

    """   """

    def __init__(self, master, abrir_menu_administrador, abrir_menu_fisioterapeuta, abrir_menu_pesquisador, encerrar):
        super().__init__(master, "Login")

        self.abrir_menu_administrador = abrir_menu_administrador
        self.abrir_menu_fisioterapeuta = abrir_menu_fisioterapeuta
        self.abrir_menu_pesquisador = abrir_menu_pesquisador
        self.encerrar = encerrar

        self.login = customtkinter.CTkLabel(self.container, text="Login: ", font=("Arial", 20, "bold"))
        self.login.grid(row=1, column=0, sticky="e", padx=20, pady=10)

        self.entry_login= customtkinter.CTkEntry(self.container)
        self.entry_login.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.senha = customtkinter.CTkLabel(self.container, text="Senha: ", font=("Arial", 20, "bold"))
        self.senha.grid(row=2, column=0, sticky="e", padx=20, pady=10)
        
        self.entry_senha= customtkinter.CTkEntry(self.container, show="*")
        self.entry_senha.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        botao_entrar = customtkinter.CTkButton(self.container, text="Entrar", width=250, height=40, command=self.verificar_login, font=("Arial", 20, "bold"))
        botao_entrar.grid(row=3, column=0, padx=20, pady=20)

        botao_encerrar = customtkinter.CTkButton(self.container, text="Encerrar", width=250, height=40, command=self.encerrar, font=("Arial", 20, "bold"), fg_color="red")
        botao_encerrar.grid(row=3, column=1, padx=20, pady=20)

    def verificar_login(self):
        usuario = self.entry_login.get()
        senha = self.entry_senha.get()

        auth = Autenticacao(usuario, senha)
        resultado = auth.verificar()

        if resultado["autenticado"]:
            messagebox.showinfo("Bem-vindo", f"Acesso permitido, {resultado['nome']}!")
            if resultado['tipo'] == "pesquisadores":
                self.abrir_menu_pesquisador()
            if resultado['tipo'] == "fisioterapeutas":
                self.abrir_menu_fisioterapeuta()
            if resultado['tipo'] == "administradores":
                self.abrir_menu_administrador()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")