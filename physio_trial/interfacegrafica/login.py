from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from CTkMessagebox import CTkMessagebox
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.context.app_context import current_user_type

class Login(BaseFrame):

    """Classe que gera a tela de login"""

    @autoparams()
    def __init__(self, master, abrir_menu_administrador, abrir_menu_fisioterapeuta, abrir_menu_pesquisador, encerrar, usuario_service: BaseUsuarioService):
        super().__init__(master, "Login")

        self.abrir_menu_administrador = abrir_menu_administrador
        self.abrir_menu_fisioterapeuta = abrir_menu_fisioterapeuta
        self.abrir_menu_pesquisador = abrir_menu_pesquisador
        self.encerrar = encerrar
        self.widgets = BaseWidgets()
        self.usuario_service = usuario_service

        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.label_login = self.widgets.label(self, texto="Usuário:", cor="transparent")
        self.label_login.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.entry_login = self.widgets.entry(self, None, None)
        self.entry_login.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_senha = self.widgets.label(self, texto="Senha:", cor="transparent")
        self.label_senha.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,20))
        
        self.entry_senha = self.widgets.entry(self, "*", None)
        self.entry_senha.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,20))

        bnt_entrar = self.widgets.button(self, texto="Entrar", comando=self.realizar_login, cor="blue")
        bnt_entrar.grid(row=3, column=1, sticky="e", padx=(20,10), pady=(10,20))

        bnt_encerrar = self.widgets.button(self, texto="Encerrar", comando=self.encerrar, cor="red")
        bnt_encerrar.grid(row=3, column=2, sticky="w", padx=(10,20), pady=(10,20))

    def realizar_login(self):
        usuario = self.entry_login.get()
        senha = self.entry_senha.get()

        if not usuario or not senha: 
            CTkMessagebox (title="Erro", message="Informe usuário e senha.", icon="cancel").get()
            return

        id_usuario = self.usuario_service.login(usuario, senha)

        if id_usuario is not None:
            # Obtém o tipo do usuário (exemplo)
            tipo = current_user_type.get()

            CTkMessagebox(title="Bem-vindo", message="Acesso permitido!", icon="check").get()
            if tipo == "pesquisadores":
                self.abrir_menu_pesquisador()
            elif tipo == "fisioterapeutas":
                self.abrir_menu_fisioterapeuta()
            elif tipo == "administradores":
                self.abrir_menu_administrador()
        else:
            CTkMessagebox(title="Erro", message="Usuário ou senha incorretos.", icon="cancel").get()
            self.entry_login.delete(0, "end")
            self.entry_senha.delete(0, "end")