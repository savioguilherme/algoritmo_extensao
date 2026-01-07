from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from dados.pesquisador import Pesquisador
from inject import autoparams
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.context.app_context import current_user_types_list

class ListarPesquisadores(BaseFrame):

    ''''Lista dos os Pesquisadores do sistema'''

    @autoparams()
    def __init__(self, master, voltar_callback, usuario_service: BaseUsuarioService):
        super().__init__(master, "Lista de Pesquisadores")

        self.voltar_callback = voltar_callback
        self.widgets = BaseWidgets()
        self.usuario_service = usuario_service

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
            
            if not self.pesquisadores:
                self.label_vazio = self.widgets.label(self, texto="Nenhum pesquisador encontrado", cor="transparent")
                self.label_vazio.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))
                return self._criar_botao_voltar(2)
            
            for i, pesq in enumerate(self.pesquisadores):
                label = self.widgets.label(self, texto=pesq.nome, cor="transparent")
                label.grid(row=i+1, column=1, sticky="e", padx=(20,10), pady=(10,20))
            return self._criar_botao_voltar(i)
        
        except Exception as e:
            self.label_erro = self.widgets.label(self, texto=f"Erro ao carregar pesquisadores: {str(e)}", cor="transparent")
            self.label_erro.grid(row=1, column=1, padx=20, pady=20)
    
    def _criar_botao_voltar(self, i):
        btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        btn_voltar.grid(row=i+2, column=1, sticky="e", padx=(20,20), pady=(10,20))