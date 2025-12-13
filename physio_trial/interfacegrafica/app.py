import customtkinter
from tkinter import TclError
from interfacegrafica.login import Login
from interfacegrafica.menu_administrador import MenuAdministrador
from interfacegrafica.menu_fisioterapeuta import MenuFisioterapeuta
from interfacegrafica.menu_paciente import MenuPaciente
from interfacegrafica.menu_pesquisador import MenuPesquisador
from interfacegrafica.agenda_pessoa import AgendaPessoa
from interfacegrafica.cadastro_paciente import CadastroPaciente
from interfacegrafica.cadastro_fisioterapeuta import CadastroFisioterapeuta
from interfacegrafica.listar_pesquisadores import ListarPesquisadores
from interfacegrafica.listar_pacientes import ListarPacientes
from interfacegrafica.listar_fisioterapeutas import ListarFisioterapeutas
from interfacegrafica.cadastro_pesquisador import CadastroPesquisador
from interfacegrafica.restricoes_pessoa import RestricoesPessoa

class App(customtkinter.CTk):

    """Classe que é a janela principal e controla todo o aplicativo enviando e recebendo as funções e parâmetros"""

    # aparencia padrao
    customtkinter.set_default_color_theme("dark-blue")

    def __init__(self):
        super().__init__()
        self.title("PhysioTrial")

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

    # Menus em geral
    def abrir_login(self):
        self.tela_login = Login(self, self.abrir_menu_administrador, self.abrir_menu_fisioterapeuta, self.abrir_menu_pesquisador, self.encerrar)

    def abrir_menu_administrador(self):
        self.limpar_tela()
        self.tela_menu_administrador = MenuAdministrador(self, self.abrir_login, self.cadastro_fisioterapeuta, self.cadastro_pesquisador, self.listar_fisioterapeutas, self.listar_pesquisadores)

    def abrir_menu_fisioterapeuta(self):
        self.limpar_tela()
        self.tela_menu_fisio = MenuFisioterapeuta(self, self.abrir_login, lambda: self.abrir_agenda(self.abrir_menu_fisioterapeuta, "fisioterapeuta"))

    def abrir_menu_pesquisador(self):
        self.limpar_tela()
        self.tela_menu_pesquisador = MenuPesquisador(
            self, 
            self.abrir_login, 
            self.cadastro_paciente, 
            lambda: self.abrir_agenda(self.abrir_menu_pesquisador, "pesquisador"), 
            lambda: self.cadastro_restricoes(self.abrir_menu_pesquisador),
            self.listar_pacientes)

    def abrir_menu_paciente(self):
        self.limpar_tela()
        self.tela_menu_paciente = MenuPaciente(self, self.abrir_menu_pesquisador)

    def abrir_agenda(self, retornar, pessoa):
        self.limpar_tela()
        self.agenda = AgendaPessoa(self, retornar, pessoa)

    # Cadastros de Objetos em geral
    def cadastro_fisioterapeuta(self):
        self.limpar_tela()
        self.tela_cadastro_fisio = CadastroFisioterapeuta(
            self, 
            self.abrir_menu_administrador
            )

    def cadastro_paciente(self):
        self.limpar_tela()
        self.tela_cadastro_paciente = CadastroPaciente(
            self, 
            self.abrir_menu_pesquisador, 
            lambda: self.cadastro_restricoes(self.cadastro_paciente)
            )

    def cadastro_pesquisador(self):
        self.limpar_tela()
        self.tela_cadastro_pesquisador = CadastroPesquisador(self, self.abrir_menu_administrador)

    def cadastro_restricoes(self, retornar):
        self.limpar_tela()
        self.tela_cadastro_restricoes = RestricoesPessoa(self, retornar)

    # Telas de listagem de objetos salvos
    def listar_fisioterapeutas(self): 
        self.limpar_tela()
        self.tela_listar_fisioterapeutas = ListarFisioterapeutas(self, self.abrir_menu_administrador)
    
    def listar_pacientes(self): 
        self.limpar_tela()
        self.tela_listar_pacientes = ListarPacientes(self, self.abrir_menu_pesquisador)

    def listar_pesquisadores(self): 
        self.limpar_tela()
        self.tela_listar_pesquisadores = ListarPesquisadores(self, self.abrir_menu_administrador)

    # Encerra a aplicacao
    def encerrar(self): 
        self.destroy()

    # Remove widgets atuais antes de trocar de tela
    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()