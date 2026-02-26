from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from CTkMessagebox import CTkMessagebox

class MenuFisioterapeuta(BaseFrame):
     
    """Menu do fisioterapeuta"""

    @autoparams()
    def __init__(self, master, user_id, voltar_callback, abrir_menu_atualiza_dados, abrir_agenda, usuario_service: BaseUsuarioService):
        super().__init__(master, titulo="Menu Fisioterapeuta")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.abrir_agenda = abrir_agenda
        self.abrir_menu_atualiza_dados = abrir_menu_atualiza_dados

        self.usuario_service = usuario_service
        self.user_id = user_id
        self.usuario_logado = None

        self.carregar_usuario_logado()

        #configurando o frame
        self.grid_rowconfigure((2), weight=1)
        self.grid_rowconfigure((1), weight=0)
        self.grid_columnconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((4), weight=1)

        self.btn_agenda = self.widgets.button(self, texto="Agenda", comando=self.abrir_agenda, cor="blue")
        self.btn_agenda.grid(row=1, column=1, sticky="", padx=(20,10), pady=(40,40))

        self.btn_alterar_dados = self.widgets.button(self, texto="Alterar meus dados", comando=self.abrir_menu_atualiza_dados, cor="green")
        self.btn_alterar_dados.grid(row=1, column=2, sticky="", padx=(10,10), pady=(40,40))

        self.btn_voltar = self.widgets.button(self, texto="Sair", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=1, column=3, sticky="", padx=(10,20), pady=(40,40))

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