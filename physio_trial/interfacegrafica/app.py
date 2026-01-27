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
from interfacegrafica.menu_atualiza_dados_usuario import MenuAtualizaDadosUsuario

class App(customtkinter.CTk):

    """Classe que é a janela principal e controla todo o aplicativo enviando e recebendo as funções e parâmetros"""

    # Aparencia padrao
    customtkinter.set_default_color_theme("dark-blue")

    def __init__(self):
        super().__init__()
        self.title("PhysioTrial")

        # Compatibilidade Linux e Windows para janela maximizada
        try:
            self.state("zoomed")
        except TclError:
            self.attributes("-zoomed", True)

        # Configuração da Janela
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #
        self.user_id = None

        # Inicia o login
        self.abrir_login()

    # Menus em geral
    def abrir_login(self):
        self.limpar_tela()
        self.user_id = None
        self.tela_login = Login(
            self, 
            self.abrir_menu_administrador, 
            self.abrir_menu_fisioterapeuta, 
            self.abrir_menu_pesquisador, 
            self.encerrar
        )

    def abrir_menu_administrador(self, user_id):
        self.limpar_tela()
        self.user_id = user_id
        self.tela_menu_administrador = MenuAdministrador(
            self,
            self.user_id,
            self.abrir_login,
            lambda: self.abrir_menu_atualiza_dados(self.user_id, self.abrir_menu_administrador),
            self.cadastro_fisioterapeuta, 
            self.cadastro_pesquisador,  
            lambda: self.listar_fisioterapeutas(self.user_id),  
            lambda: self.listar_pesquisadores(self.user_id)
        )
        
    def abrir_menu_fisioterapeuta(self, user_id):
        self.limpar_tela()
        self.user_id = user_id
        self.tela_menu_fisio = MenuFisioterapeuta(
            self,
            self.user_id,
            self.abrir_login,
            lambda: self.abrir_menu_atualiza_dados(self.user_id, self.abrir_menu_fisioterapeuta),
            self.abrir_agenda
        )

    def abrir_menu_pesquisador(self, user_id):
        self.limpar_tela()
        self.user_id = user_id
        self.tela_menu_pesquisador = MenuPesquisador(
            self,
            self.user_id,
            self.abrir_login,
            lambda: self.abrir_menu_atualiza_dados(self.user_id, self.abrir_menu_pesquisador),
            self.cadastro_paciente,
            self.abrir_agenda,
            lambda: self.listar_pacientes(self.user_id)
        )

    def abrir_agenda(self):
        self.limpar_tela()
        if self.user_type == 1:
            retornar = lambda: self.abrir_menu_fisioterapeuta(self.user_id, self.user_type)
        elif self.user_type == 2:
            retornar = lambda: self.abrir_menu_pesquisador(self.user_id, self.user_type)
        else:
            retornar = self.abrir_login()
        self.agenda = AgendaPessoa(
            self, 
            retornar
        )

    def abrir_menu_atualiza_dados(self, user_id, retornar_tela):
        self.limpar_tela()
        self.tela_atualiza_dados_usuario = MenuAtualizaDadosUsuario(
            self,
            user_id,
            lambda: retornar_tela(self.user_id)
        )

    def abrir_menu_paciente(self, user_id, retornar_tela):
        self.limpar_tela()
        self.tela_menu_paciente = MenuPaciente(
            self,
            user_id, 
            lambda: retornar_tela(user_id,)
        )

    # Cadastros de Objetos em geral
    def cadastro_fisioterapeuta(self):
        self.limpar_tela()
        self.tela_cadastro_fisio = CadastroFisioterapeuta(
            self, 
            lambda: self.abrir_menu_administrador(self.user_id)
        )

    def cadastro_paciente(self):
        self.limpar_tela()
        self.tela_cadastro_paciente = CadastroPaciente(
            self, 
            lambda: self.abrir_menu_pesquisador(self.user_id), 
        )

    def cadastro_pesquisador(self):
        self.limpar_tela()
        self.tela_cadastro_pesquisador = CadastroPesquisador(
            self, 
            lambda: self.abrir_menu_administrador(self.user_id)
        )

    # Telas de listagem de objetos salvos
    def listar_fisioterapeutas(self, user_id): 
        self.limpar_tela()
        self.tela_listar_fisioterapeutas = ListarFisioterapeutas(
            self, 
            lambda: self.abrir_menu_administrador(user_id),
            lambda user_id: self.abrir_menu_atualiza_dados(
                user_id=user_id,
                retornar_tela=self.listar_fisioterapeutas
            )
        )
    
    def listar_pacientes(self, user_id): 
        self.limpar_tela()
        self.tela_listar_pacientes = ListarPacientes(
            self,
            lambda: self.abrir_menu_pesquisador(user_id),
            lambda user_id: self.abrir_menu_paciente(
                user_id=user_id,
                retornar_tela=self.listar_pacientes
            )
        )

    def listar_pesquisadores(self, user_id): 
        self.limpar_tela()
        self.tela_listar_pesquisadores = ListarPesquisadores(
            self, 
            lambda: self.abrir_menu_administrador(user_id),
            lambda user_id: self.abrir_menu_atualiza_dados(
                user_id=user_id,
                retornar_tela=self.listar_pesquisadores
            )
        )

    # Encerra a aplicacao
    def encerrar(self): 
        self.destroy()

    # Remove widgets atuais antes de trocar de tela
    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()
