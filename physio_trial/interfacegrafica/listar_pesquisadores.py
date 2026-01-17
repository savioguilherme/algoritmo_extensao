from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.context.app_context import current_user_types_list
from CTkMessagebox import CTkMessagebox
from dados.pesquisador import Pesquisador

class ListarPesquisadores(BaseFrame):

    ''''Lista dos os Pesquisadores do sistema'''

    @autoparams()
    def __init__(self, master, voltar_callback, abrir_menu_atualiza_dados, usuario_service: BaseUsuarioService):
        super().__init__(master, "Lista de Pesquisadores")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.usuario_service = usuario_service
        self.abrir_menu_atualiza_dados = abrir_menu_atualiza_dados

        # Dados dos pesquisadores
        self.pesquisadores: list[Pesquisador] = []

        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.carregar_pesquisadores()

    def carregar_pesquisadores(self):
        try:
            user_types_list = current_user_types_list.get() or []
            
            pesquisador_tipo_id = user_types_list[2] if len(user_types_list) > 1 else 1
                
            self.pesquisadores = self.usuario_service.listar_usuarios(lista_tipos=[pesquisador_tipo_id], apenas_ativos=False)
            
            for i, pesq in enumerate(self.pesquisadores):
                label = self.widgets.button(self, texto=pesq.nome, comando=lambda p_id=pesq.id_pessoa: self.abrir_menu_atualiza_dados(p_id), cor="Green")
                label.grid(row=i+1, column=1, sticky="e", padx=(20,10), pady=(10,20))
            return self._criar_botao_voltar(i)
        
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Erro ao carregar dados do usuário: {str(e)}", 
                icon="cancel"
            ).get()
            self.voltar_callback()
    
    def _criar_botao_voltar(self, i):
        btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        btn_voltar.grid(row=i+2, column=1, sticky="e", padx=(20,20), pady=(10,20))