from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_paciente_service import BasePacienteService
from dados.administrador import Administrador
from CTkMessagebox import CTkMessagebox
from datetime import date

class MenuPaciente(BaseFrame): 

    '''Menu para atualizar e verificar dados de um paciente'''

    @autoparams()
    def __init__(self, master, user_id, voltar_callback, usuario_paciente_service: BasePacienteService):
        super().__init__(master, titulo="Menu Paciente")

        self.widgets = BaseWidgets()
        self.usuario_paciente_service = usuario_paciente_service

        self.voltar_callback = voltar_callback

        self.user_id = user_id

        #configurando o frame
        self.grid_rowconfigure((1,2,3,4,5,6,7,8,9), weight=0)
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

        self.label_pesquisador = self.widgets.label(self, "Pesquisador:", cor="transparent")
        self.label_pesquisador.grid(row=4, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.entry_pesquisador = self.widgets.entry(self, None, None)
        self.entry_pesquisador.grid(row=4, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_fisioterapeuta = self.widgets.label(self, "Fisioterapeuta:", cor="transparent")
        self.label_fisioterapeuta.grid(row=5, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_fisioterapeuta = self.widgets.entry(self, None, None)
        self.entry_fisioterapeuta.grid(row=5, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_status_usuario = self.widgets.label(self, "Status Usuário: ", cor="transparent")
        self.label_status_usuario.grid(row=6, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.switch_status_usuario = self.widgets.switch(self, texto="Ativo", comando=None)
        self.switch_status_usuario.grid(row=6, column=2, sticky="w", columnspan=1, padx=(10,20), pady=(10,10))

        self.label_cadastro_restricoes = self.widgets.label(self, "Cadastrar Horários:", cor="transparent")
        self.label_cadastro_restricoes.grid(row=7, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.bnt_restricoes = self.widgets.button(self, texto="Cadastro de Horários", comando=None, cor="blue")
        self.bnt_restricoes.grid(row=7, column=2, sticky="w", columnspan=1, padx=(10,20), pady=(10,10))

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=None, cor="Green")
        self.btn_salvar.grid(row=8, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=8, column=2, sticky="w", padx=(10,20), pady=(10,20))

        self.__carregar_usuario()

    def __carregar_usuario(self):
        try:
            self.usuario = self.usuario_paciente_service.consultar(self.user_id)
            if self.usuario:
        
                self.entry_nome.delete(0, 'end')
                self.entry_nome.insert(0, self.usuario.nome)
                
                self.entry_email.delete(0, 'end')
                self.entry_email.insert(0, self.usuario.email)
                
                # Converter data para formato string se necessário
                data_nascimento = self.__formatar_data(self.usuario.data_nascimento)
                self.entry_data_nascimento.delete(0, 'end')
                self.entry_data_nascimento.insert(0, data_nascimento)

                self.entry_fisioterapeuta.delete(0, 'end')
                self.entry_fisioterapeuta.insert(0, self.usuario.fisioterapeuta_responsavel)

                self.entry_pesquisador.delete(0, 'end')
                self.entry_pesquisador.insert(0, self.usuario.pesquisador_responsavel)
                
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
        
    '''def __atualizar_dados(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        data_nascimento = self.entry_data_nascimento.get()
        senha = self.entry_nova_senha.get()
        confirmar_senha = self.entry_confirma_nova_senha.get()
        
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

        data_array: list[int] = [int(data) for data in data_nascimento.split("/")]
        
        try:
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
            ).get()'''