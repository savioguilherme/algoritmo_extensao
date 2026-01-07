from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from dados.administrador import Administrador
from CTkMessagebox import CTkMessagebox

class MenuAtualizaUsuario(BaseFrame): 

    ''' '''
    @autoparams()
    def __init__(self, master, voltar_callback, user_id, usuario_service: BaseUsuarioService):
        super().__init__(master, titulo="Alterar Senha")

        self.widgets = BaseWidgets()
        self.usuario_service = usuario_service

        self.voltar_callback = voltar_callback

        self.user_id = user_id
        self.usuario_logado = None
        

        #configurando o frame
        self.grid_rowconfigure((1,2), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.label_nova_senha = self.widgets.label(self, "Nova senha:", cor="transparent")
        self.label_nova_senha.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.entry_nova_senha = self.widgets.entry(self, None, None)
        self.entry_nova_senha.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_confirma_nova_senha = self.widgets.label(self, "Confirme a nova senha:", cor="transparent")
        self.label_confirma_nova_senha.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_confirma_nova_senha = self.widgets.entry(self, None, None)
        self.entry_confirma_nova_senha.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.trocar_senha, cor="Green")
        self.btn_salvar.grid(row=3, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=3, column=2, sticky="w", padx=(10,20), pady=(10,20))

    def trocar_senha(self):
        self.usuario_logado = self.usuario_service.consultar(self.user_id)
        
        senha = self.entry_nova_senha.get()
        nova_senha = self.entry_confirma_nova_senha.get()

        if not senha or not nova_senha:
            CTkMessagebox(title="Erro", message="Preencha todos os campos!", icon="cancel").get()
            return
        
        if senha != nova_senha:
            CTkMessagebox(title="Erro", message="As senhas não coincidem!", icon="cancel").get()
            return
        
        if len(senha) < 6:
            CTkMessagebox(title="Erro", message="A senha deve ter pelo menos 6 caracteres!", icon="cancel").get()
            return
        
        self.usuario_service.atualizar_adm(
            Administrador(
                id_administrador=self.usuario_logado.id_pessoa,
                nome_administrador=self.usuario_logado.nome,
                email=self.usuario_logado.email,
                data_nascimento=self.usuario_logado.data_nascimento,
                login=self.usuario_logado.login,
                senha=senha,
                status_administrador=self.usuario_logado.status_pessoa,
                tipo=self.usuario_logado.tipo
            )
        )
