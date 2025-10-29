import customtkinter
from tkinter import TclError
from interfacegrafica.login import Login
from interfacegrafica.menu_principal import MenuPrincipal
from interfacegrafica.cadastro_paciente import CadastroPaciente
from interfacegrafica.cadastro_fisioterapeuta import CadastroFisioterapeuta
from interfacegrafica.cadastro_pesquisador import CadastroPesquisador
from interfacegrafica.menu_administrador import MenuAdministrador
from interfacegrafica.menu_pesquisador import MenuPesquisador
from interfacegrafica.menu_fisioterapeuta import MenuFisioterapeuta
from armazenamento.guardar import Guardar

class App(customtkinter.CTk):

    """Janela principal"""

    # aparencia padrao
    customtkinter.set_default_color_theme("dark-blue")

    def __init__(self):
        super().__init__()

        self.title("Cadastro de Pessoas")
        
        # Compatibilidade Linux e Windows para janela maximizada
        try:
            self.state("zoomed")
        except TclError:
            self.attributes("-zoomed", True)

        #configuração da Janela
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Cria o objeto que salva as classes de objetos em listas
        self.storage = Guardar()

        # Inicia o login
        self.abrir_login()

    def abrir_login(self):
        self.login = Login(self, self.abrir_menu, self.encerrar)

    def abrir_menu(self):
        self.limpar_tela()
        self.menu = MenuPrincipal(self, self.abrir_menu_administrador, self.abrir_menu_fisioterapeuta, self.abrir_menu_pesquisador, self.encerrar)

    def abrir_menu_administrador(self):
        self.limpar_tela()
        self.tela_fisio = MenuAdministrador(self, self.abrir_menu, self.abrir_tela_fisioterapeuta, self.abrir_tela_pesquisador)

    def abrir_menu_fisioterapeuta(self):
        self.limpar_tela()
        self.tela_fisio = MenuFisioterapeuta(self, self.abrir_menu)

    def abrir_tela_fisioterapeuta(self):
        self.limpar_tela()
        self.tela_fisio = CadastroFisioterapeuta(self, self.abrir_menu_administrador, self.storage)

    def abrir_tela_paciente(self):
        self.limpar_tela()
        self.tela_paciente = CadastroPaciente(self, self.abrir_menu_pesquisador, self.storage)

    def abrir_menu_pesquisador(self):
        self.limpar_tela()
        self.tela_menu_pesquisador = MenuPesquisador(self, self.abrir_menu, self.abrir_tela_paciente)

    def abrir_tela_pesquisador(self):
        self.limpar_tela()
        self.tela_pesquisador = CadastroPesquisador(self, self.abrir_menu_administrador, self.storage)

    def encerrar(self): 
        self.destroy()

    def limpar_tela(self):

        """Remove widgets atuais antes de trocar de tela"""
        
        for widget in self.winfo_children():
            widget.destroy()