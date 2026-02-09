import customtkinter as ctk
from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador
from interfacegrafica.restricoes_pessoa.restricoes_pessoa import RestricoesPessoa
from CTkMessagebox import CTkMessagebox
from datetime import date

class MenuAtualizaDadosUsuario(BaseFrame): 

    '''Menu para que usuário altere seus dados pessoais e/ou suas restrições de horários'''

    @autoparams()
    def __init__(self, master, user_id, voltar_callback, usuario_service: BaseUsuarioService):
        super().__init__(master, titulo="Alterar Dados")

        self.widgets = BaseWidgets()
        self.usuario_service = usuario_service

        self.voltar_callback = voltar_callback

        self.user_id = user_id

        #configurando o frame
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure((1,2), weight=1)

        self.label_nome = self.widgets.label(self.scrollable_frame, texto="Nome:", cor="transparent")
        self.label_nome.grid(row=1, column=1, sticky="e", padx=(20,10) ,pady=(20,10))

        self.entry_nome = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_nome.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_email = self.widgets.label(self.scrollable_frame, texto="Email:", cor="transparent")
        self.label_email.grid(row=2, column=1, sticky="e",padx=(20,10), pady=(10,10))

        self.entry_email = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_email.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_data_nascimento = self.widgets.label(self.scrollable_frame, texto="Data de Nascimento:", cor="transparent")
        self.label_data_nascimento.grid(row=3, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_data_nascimento = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_data_nascimento.grid(row=3, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_nova_senha = self.widgets.label(self.scrollable_frame, "Senha:", cor="transparent")
        self.label_nova_senha.grid(row=4, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.entry_nova_senha = self.widgets.entry(self.scrollable_frame, "*", None)
        self.entry_nova_senha.grid(row=4, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_confirma_nova_senha = self.widgets.label(self.scrollable_frame, "Confirme a senha:", cor="transparent")
        self.label_confirma_nova_senha.grid(row=5, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_confirma_nova_senha = self.widgets.entry(self.scrollable_frame, "*", None)
        self.entry_confirma_nova_senha.grid(row=5, column=2, sticky="w", padx=(10,20), pady=(10,10))

        # self.label_status_usuario = self.widgets.label(self.scrollable_frame, "Status Usuário: ", cor="transparent")
        # self.label_status_usuario.grid(row=6, column=1, sticky="e", padx=(20,10), pady=(10,10))

        # self.switch_status_usuario = self.widgets.switch(self.scrollable_frame, texto="Ativo", comando=None)
        # self.switch_status_usuario.grid(row=6, column=2, sticky="w", columnspan=1, padx=(10,20), pady=(10,10))

        self.widget_restricoes = None

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.__atualizar_dados, cor="Green")
        self.btn_salvar.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self.__carregar_usuario()

    def __carregar_usuario(self):
        try:
            self.usuario = self.usuario_service.consultar(self.user_id)
            if self.usuario:
        
                self.entry_nome.delete(0, 'end')
                self.entry_nome.insert(0, self.usuario.nome)
                
                self.entry_email.delete(0, 'end')
                self.entry_email.insert(0, self.usuario.email)
                
                # Converter data para formato string se necessário
                data_nascimento = self.__formatar_data(self.usuario.data_nascimento)
                self.entry_data_nascimento.delete(0, 'end')
                self.entry_data_nascimento.insert(0, data_nascimento)

                restricoes = None
                if isinstance(self.usuario, Fisioterapeuta):
                    restricoes = self.usuario.restricoes_fisioterapeuta
                elif isinstance(self.usuario, Pesquisador):
                    restricoes = self.usuario.restricoes_pesquisador
                if restricoes:
                    self.widget_restricoes = RestricoesPessoa(self.scrollable_frame, restricoes)
                    self.widget_restricoes.grid(row=7, column=1, columnspan=2, sticky="nsew")
                
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Erro ao carregar dados do usuário: {str(e)}", 
                icon="cancel"
            )
            return
    
    def __formatar_data(self, data):
        if hasattr(data, 'strftime'):
            return data.strftime("%d/%m/%Y")
        return str(data)
        
    def __atualizar_dados(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        data_nascimento = self.entry_data_nascimento.get()
        senha = self.entry_nova_senha.get()
        confirmar_senha = self.entry_confirma_nova_senha.get()
        restricoes = None
        if self.widget_restricoes:
            restricoes = self.widget_restricoes.get_dados()
        
        # Validar campos básicos
        if not nome or not email or not data_nascimento:
            CTkMessagebox(
                title="Erro", 
                message="Preencha todos os campos!", 
                icon="cancel"
                ).get()
            return
        
        # Validar senha
        if not senha or not confirmar_senha:
            CTkMessagebox(
                title="Erro", 
                message="Preencha os campos de senha com a senha atual ou com uma nova senha", 
                icon="cancel"
            ).get()
            return
        
        if senha != confirmar_senha:
            CTkMessagebox(
                title="Erro", 
                message="As senhas não coincidem!", 
                icon="cancel"
                ).get()
            return
        
        if len(senha) < 6:
            CTkMessagebox(
                title="Erro", 
                message="A senha deve ter pelo menos 6 caracteres!", 
                icon="cancel"
                ).get()
            return

        if self.widget_restricoes and not restricoes:
            CTkMessagebox(
                title="Erro", 
                message="Restrições ou disponibilidades inválidas!", 
                icon="cancel"
                ).get()
            return

        data_array: list[int] = [int(data) for data in data_nascimento.split("/")]
        
        try:
            if isinstance(self.usuario, Administrador):
                administrador_atualizado = Administrador(
                    id_administrador=self.usuario.id_pessoa,
                    nome_administrador=nome,
                    email=email,
                    data_nascimento=date(data_array[2], data_array[1], data_array[0]), 
                    login=self.usuario.login,
                    senha=senha,  
                    status_administrador=self.usuario.status_pessoa,
                    tipo=self.usuario.tipo
                )
                self.usuario_service.atualizar_adm(administrador_atualizado)
            
            elif isinstance(self.usuario, Fisioterapeuta):
                fisioterapeuta_atualizado = Fisioterapeuta(
                    id_fisioterapeuta=self.usuario.id_pessoa,
                    nome_fisioterapeuta=nome,
                    email=email,
                    data_nascimento=date(data_array[2], data_array[1], data_array[0]), 
                    login=self.usuario.login,
                    senha=senha,  
                    status_fisioterapeuta=self.usuario.status_pessoa,
                    tipo=self.usuario.tipo
                )
                fisioterapeuta_atualizado.restricoes_fisioterapeuta = restricoes
                self.usuario_service.atualizar_fisioterapeuta(fisioterapeuta_atualizado)

            elif isinstance(self.usuario, Pesquisador):
                pesquisador_atualizado = Pesquisador(
                    id_pesquisador=self.usuario.id_pessoa,
                    nome_pesquisador=nome,
                    email=email,
                    data_nascimento=date(data_array[2], data_array[1], data_array[0]), 
                    login=self.usuario.login,
                    senha=senha,  
                    status_pesquisador=self.usuario.status_pessoa,
                    tipo=self.usuario.tipo
                )
                pesquisador_atualizado.restricoes_pesquisador = restricoes
                self.usuario_service.atualizar_pesquisador(pesquisador_atualizado)

            CTkMessagebox(
                title="Sucesso", 
                message="Dados atualizados com sucesso!", 
                icon="check"
            ).get()

            self.voltar_callback()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Erro ao atualizar dados: {str(e)}", 
                icon="cancel"
            ).get()
