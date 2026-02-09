from inject import autoparams
import customtkinter as ctk
from datetime import date

from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from interfacegrafica.restricoes_pessoa.restricoes_pessoa import RestricoesPessoa
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from CTkMessagebox import CTkMessagebox
from dados.fisioterapeuta import Fisioterapeuta

@autoparams()
class CadastroFisioterapeuta(BaseFrame):

    '''Classe que gera a tela de cadastro de um fisioterapeuta'''

    def __init__(self, master, voltar_callback, usuario_service: BaseUsuarioService):
        super().__init__(master, "Cadastro de Fisioterapeutas")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.usuario_service = usuario_service

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        self.label_nome = self.widgets.label(self.scrollable_frame, texto="Nome:", cor="transparent")
        self.label_nome.grid(row=0, column=0, sticky="e", padx=(20,10) ,pady=(10,5))
        self.entry_nome = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_nome.grid(row=0, column=1, sticky="ew", padx=(10,20), pady=(10,5))

        self.label_email = self.widgets.label(self.scrollable_frame, texto="Email:", cor="transparent")
        self.label_email.grid(row=1, column=0, sticky="e",padx=(20,10), pady=(5,5))
        self.entry_email = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_email.grid(row=1, column=1, sticky="ew", padx=(10,20), pady=(5,5))

        self.label_data_nascimento = self.widgets.label(self.scrollable_frame, texto="Data de Nascimento (dd/mm/aaaa):", cor="transparent")
        self.label_data_nascimento.grid(row=2, column=0, sticky="e", padx=(20,10), pady=(5,5))
        self.entry_data_nascimento = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_data_nascimento.grid(row=2, column=1, sticky="ew", padx=(10,20), pady=(5,5))

        self.label_login = self.widgets.label(self.scrollable_frame, texto="Login:", cor="transparent")
        self.label_login.grid(row=3, column=0, sticky="e", padx=(20,10), pady=(5,5))
        self.entry_login = self.widgets.entry(self.scrollable_frame, None , None)
        self.entry_login.grid(row=3, column=1, sticky="ew", padx=(10,20), pady=(5,5))

        self.label_senha = self.widgets.label(self.scrollable_frame, texto="Senha:", cor="transparent")
        self.label_senha.grid(row=4, column=0, sticky="e", padx=(20,10), pady=(5,5))
        self.entry_senha = self.widgets.entry(self.scrollable_frame, "*",  None)
        self.entry_senha.grid(row=4, column=1, sticky="ew", padx=(10,20), pady=(5,5))

        self.label_confirma_nova_senha = self.widgets.label(self.scrollable_frame, "Confirme a senha:", cor="transparent")
        self.label_confirma_nova_senha.grid(row=5, column=0, sticky="e", padx=(20,10), pady=(5,5))
        self.entry_confirma_nova_senha = self.widgets.entry(self.scrollable_frame, "*", None)
        self.entry_confirma_nova_senha.grid(row=5, column=1, sticky="ew", padx=(10,20), pady=(5,5))
        
        # Restrições
        self.restricoes_widget = RestricoesPessoa(self.scrollable_frame)
        self.restricoes_widget.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Ações
        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.realizar_cadastro_fisioterapeuta, cor="green")
        self.btn_salvar.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=10)

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=10)

    def realizar_cadastro_fisioterapeuta(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        data_nascimento = self.entry_data_nascimento.get()
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        confirmar_senha = self.entry_confirma_nova_senha.get()
        restricoes = self.restricoes_widget.get_dados()

        if not login or not senha or not nome or not email or not data_nascimento: 
            CTkMessagebox(title="Erro", message="Preencha todos os campos!", icon="cancel").get()
            return
        
        if senha != confirmar_senha: 
            CTkMessagebox(title="Erro", message="As senhas não correspondem!", icon="cancel").get()
            self.entry_senha.delete(0, "end")
            self.entry_confirma_nova_senha.delete(0, "end")
            return

        if not restricoes:
            CTkMessagebox(title="Erro", message="Restrições ou disponibilidades inválidas!", icon="cancel").get()
            return
        
        try:
            data_array: list[int] = [int(data) for data in data_nascimento.split("/")]
            parsed_date = date(data_array[2], data_array[1], data_array[0])
        except (ValueError, IndexError):
            CTkMessagebox(title="Erro", message="Formato de data inválido. Use dd/mm/aaaa.", icon="cancel").get()
            return

        novo_fisio: Fisioterapeuta = Fisioterapeuta(
            id_fisioterapeuta=None, 
            nome_fisioterapeuta=nome, 
            email=email, 
            data_nascimento=parsed_date, 
            login=login, 
            senha=senha, 
            status_fisioterapeuta=True
        )
        novo_fisio.restricoes_fisioterapeuta = restricoes
        
        fisioterapeuta = self.usuario_service.inserir_fisioterapeuta(fisio=novo_fisio)

        if fisioterapeuta is not None: 
            CTkMessagebox(title="Cadastrado", message="Fisioterapeuta Cadastrado com Sucesso!", icon="check").get()
            self.voltar_callback()
        else:
            CTkMessagebox(title="Erro no Cadastro", message="Não foi possível cadastrar o usuário!", icon="cancel").get()
            return
