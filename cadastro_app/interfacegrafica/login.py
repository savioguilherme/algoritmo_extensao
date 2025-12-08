from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.autenticacao import Autenticacao
from CTkMessagebox import CTkMessagebox

class Login(BaseFrame):

    """Classe que gera a tela de login"""

    def __init__(self, master, abrir_menu_administrador, abrir_menu_fisioterapeuta, abrir_menu_pesquisador, encerrar):
        super().__init__(master, "Login")

        self.abrir_menu_administrador = abrir_menu_administrador
        self.abrir_menu_fisioterapeuta = abrir_menu_fisioterapeuta
        self.abrir_menu_pesquisador = abrir_menu_pesquisador
        self.encerrar = encerrar
        self.widgets = BaseWidgets()

        self.label_login = self.widgets.label(self.container, texto="Usuário:")
        self.label_login.grid(row=1, column=0, sticky="e", padx=20, pady=10)

        self.entry_login = self.widgets.entry(self.container, None)
        self.entry_login.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.label_senha = self.widgets.label(self.container, texto="Senha:")
        self.label_senha.grid(row=2, column=0, sticky="e", padx=20, pady=10)
        
        self.entry_senha = self.widgets.entry(self.container, "*")
        self.entry_senha.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        bnt_entrar = self.widgets.button(self.container, texto="Entrar", comando=self.verificar_login, cor="blue")
        bnt_entrar.grid(row=3, column=0, padx=20, pady=20)

        bnt_encerrar = self.widgets.button(self.container, texto="Encerrar", comando=self.encerrar, cor="red")
        bnt_encerrar.grid(row=3, column=1, padx=20, pady=20)

    def verificar_login(self):
        usuario = self.entry_login.get()
        senha = self.entry_senha.get()

        auth = Autenticacao(usuario, senha)
        resultado = auth.verificar()

        if resultado["autenticado"]:
            msg = CTkMessagebox(title="Bem-vindo", message=f"Acesso permitido, {resultado['nome']}!", icon="check")
            msg.get()
            if resultado['tipo'] == "pesquisadores":
                self.abrir_menu_pesquisador()
            if resultado['tipo'] == "fisioterapeutas":
                self.abrir_menu_fisioterapeuta()
            if resultado['tipo'] == "administradores":
                self.abrir_menu_administrador()
        else:
            CTkMessagebox(title="Erro", message="Usuário ou senha incorretos.", icon="cancel")