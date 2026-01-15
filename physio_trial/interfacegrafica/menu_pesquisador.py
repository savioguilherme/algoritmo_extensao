from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from CTkMessagebox import CTkMessagebox

class MenuPesquisador(BaseFrame):

    """Menu do pesquisador"""

    @autoparams()
    def __init__(self, master, user_id, voltar_callback, abrir_menu_atualiza_dados, cadastro_paciente, abrir_agenda, abrir_menu_paciente, usuario_service: BaseUsuarioService):
        super().__init__(master, titulo="Menu Pesquisador")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.cadastro_paciente = cadastro_paciente
        self.listar_paciente = abrir_menu_paciente
        self.abrir_agenda = abrir_agenda
        self.abrir_menu_atualiza_dados = abrir_menu_atualiza_dados

        self.usuario_service = usuario_service
        self.user_id = user_id
        self.usuario_logado = None

        self.carregar_usuario_logado()

        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.btn_cadastrar_paci = self.widgets.button(self, texto="Cadastrar Paciente", comando=self.cadastro_paciente, cor="blue")
        self.btn_cadastrar_paci.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.btn_listar_paci = self.widgets.button(self, texto="Listar Pacientes", comando=self.listar_paciente, cor="blue")
        self.btn_listar_paci.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.btn_agenda = self.widgets.button(self, texto="Agenda", comando=self.abrir_agenda, cor="blue")
        self.btn_agenda.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.btn_alterar_dados = self.widgets.button(self, texto="Alterar meus dados", comando=self.abrir_menu_atualiza_dados, cor="green")
        self.btn_alterar_dados.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.btn_voltar = self.widgets.button(self, texto="Sair", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=3, column=1, sticky="e", padx=(20,20), pady=(10,20))

    def carregar_usuario_logado(self):
        try:
            self.usuario_logado = self.usuario_service.consultar(self.user_id)
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Erro ao carregar dados do usuário: {str(e)}", 
                icon="cancel"
            ).get()
            return None