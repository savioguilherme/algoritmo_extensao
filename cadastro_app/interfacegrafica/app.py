import customtkinter
from tkinter import TclError
from interfacegrafica.login import Login
from interfacegrafica.menu_administrador import MenuAdministrador
from interfacegrafica.menu_pesquisador import MenuPesquisador
from interfacegrafica.menu_fisioterapeuta import MenuFisioterapeuta
from interfacegrafica.cadastro_paciente import CadastroPaciente
from interfacegrafica.cadastro_fisioterapeuta import CadastroFisioterapeuta
from interfacegrafica.listar_pesquisadores import ListarPesquisadores
from interfacegrafica.listar_fisioterapeutas import ListarFisioterapeutas
from interfacegrafica.cadastro_pesquisador import CadastroPesquisador

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

        # Inicia o login
        self.abrir_login()

    def abrir_login(self):
        self.tela_login = Login(self, self.abrir_menu_administrador, self.abrir_menu_fisioterapeuta, self.abrir_menu_pesquisador, self.encerrar)

    def abrir_menu_administrador(self):
        self.limpar_tela()
        self.tela_menu_administrador = MenuAdministrador(self, self.encerrar, self.cadastro_fisioterapeuta, self.cadastro_pesquisador, self.listar_fisioterapeutas, self.listar_pesquisadores)

    def abrir_menu_fisioterapeuta(self):
        self.limpar_tela()
        self.tela_menu_fisio = MenuFisioterapeuta(self, self.encerrar)

    def abrir_menu_pesquisador(self):
        self.limpar_tela()
        self.tela_menu_pesquisador = MenuPesquisador(self, self.encerrar, self.cadastro_paciente)

    def cadastro_fisioterapeuta(self):
        self.limpar_tela()
        self.tela_cadastro_fisio = CadastroFisioterapeuta(self, self.abrir_menu_administrador)

    def cadastro_paciente(self):
        self.limpar_tela()
        self.tela_cadastro_paciente = CadastroPaciente(self, self.abrir_menu_pesquisador)

    def cadastro_pesquisador(self):
        self.limpar_tela()
        self.tela_cadastro_pesquisador = CadastroPesquisador(self, self.abrir_menu_administrador)

    def listar_fisioterapeutas(self): 
        self.limpar_tela()
        self.tela_listar_fisioterapeutas = ListarFisioterapeutas(self, self.abrir_menu_administrador)

    def listar_pesquisadores(self): 
        self.limpar_tela()
        self.tela_listar_pesquisadores = ListarPesquisadores(self, self.abrir_menu_administrador)

    def encerrar(self): 
        self.destroy()

    def limpar_tela(self):

        """Remove widgets atuais antes de trocar de tela"""
        
        for widget in self.winfo_children():
            widget.destroy()