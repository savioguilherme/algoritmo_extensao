from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from CTkMessagebox import CTkMessagebox
from dados.pesquisador import Pesquisador
from datetime import date

@autoparams()
class CadastroPesquisador(BaseFrame):

    '''Classe que cria a tela de cadastro para inserir pesquisadores no sistema'''

    def __init__(self, master, voltar_callback, usuario_service: BaseUsuarioService):
        super().__init__(master, "Cadastro de Pesquisadores")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback 
        
        self.usuario_service = usuario_service

       #configurando o frame
        self.grid_rowconfigure((1,2,3,4,5,6,7,8), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.label_nome = self.widgets.label(self, texto="Nome:", cor="transparent")
        self.label_nome.grid(row=1, column=1, sticky="e", padx=(20,10) ,pady=(20,10))

        self.entry_nome = self.widgets.entry(self, None, None)
        self.entry_nome.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_email = self.widgets.label(self, texto="Email:", cor="transparent")
        self.label_email.grid(row=2, column=1, sticky="e",padx=(20,10), pady=(10,10))

        self.entry_email = self.widgets.entry(self, None, None)
        self.entry_email.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_data_nascimento = self.widgets.label(self, texto="Data de Nascimento:", cor="transparent")
        self.label_data_nascimento.grid(row=3, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_data_nascimento = self.widgets.entry(self, None, None)
        self.entry_data_nascimento.grid(row=3, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_login = self.widgets.label(self, texto="Login:", cor="transparent")
        self.label_login.grid(row=4, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_login = self.widgets.entry(self, None , None)
        self.entry_login.grid(row=4, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_senha = self.widgets.label(self, texto="Senha:", cor="transparent")
        self.label_senha.grid(row=5, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_senha = self.widgets.entry(self, "*",  None)
        self.entry_senha.grid(row=5, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_confirma_nova_senha = self.widgets.label(self, "Confirme a senha:", cor="transparent")
        self.label_confirma_nova_senha.grid(row=6, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_confirma_nova_senha = self.widgets.entry(self, "*", None)
        self.entry_confirma_nova_senha.grid(row=6, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_cadastro_restricoes = self.widgets.label(self, "Cadastrar Horários:", cor="transparent")
        self.label_cadastro_restricoes.grid(row=7, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.bnt_restricoes = self.widgets.button(self, texto="Cadastro de Horários", comando=None, cor="blue")
        self.bnt_restricoes.grid(row=7, column=2, sticky="w", columnspan=1, padx=(10,20), pady=(10,10))

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.realizar_cadastro_pesquisador , cor="green")
        self.btn_salvar.grid(row=8, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=8, column=2, sticky="w", padx=(10,20), pady=(10,20))

    def realizar_cadastro_pesquisador(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        data_nascimento = self.entry_data_nascimento.get()
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        confirmar_senha = self.entry_confirma_nova_senha.get()

        if not login or not senha or not nome or not email or not data_nascimento: 
            CTkMessagebox(
                title="Erro", 
                message="Preencha todos os campos!", 
                icon="cancel"
            ).get()
            return
        
        if senha != confirmar_senha: 
            CTkMessagebox(
                title="Erro", 
                message="As senhas não correspondem!", 
                icon="cancel"
            ).get()
            self.entry_senha.delete(0, "end")
            self.entry_confirma_nova_senha.delete(0, "end")
            return
        
        data_array: list[int] = [int(data) for data in data_nascimento.split("/")]
        
        novo_pesquisador: Pesquisador = Pesquisador(
            id_pesquisador=1,
            nome_pesquisador=nome,
            email=email,
            data_nascimento=date(data_array[2], data_array[1], data_array[0]),
            login=login,
            senha=senha,
            status_pesquisador=True
        )

        pesquisador = self.usuario_service.inserir_pesquisador(pesq=novo_pesquisador)

        if pesquisador is not None: 
            CTkMessagebox(
                title="Cadastrado", 
                message="Pesquisador Cadastrado com Sucesso!", 
                icon="check"
            ).get()
            self.voltar_callback()
        else:
            CTkMessagebox(
                title="Erro no Cadastro", 
                message="Não foi possível cadastrar o usuário!", 
                icon="cancel"
            ).get()
            return