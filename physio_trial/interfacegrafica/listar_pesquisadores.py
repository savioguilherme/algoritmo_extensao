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

        # Dicionario para mapear nomes e ids
        self.pesquisadores_map: dict[str, int] = {}

        # Configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.option_pesquisadores = self.widgets.option_menu(self, None, self.definir_id_pesquisador_menu_opcao)
        self.option_pesquisadores.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(20,20), pady=(20,10))

        btn_abrir = self.widgets.button(self, texto="Abrir", comando=lambda: self.abrir_menu_atualiza_dados(self.id_pesq), cor="green")
        btn_abrir.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,20))

        self.carregar_pesquisadores()

    def carregar_pesquisadores(self):
        try:
            user_types_list = current_user_types_list.get() or []
            
            pesquisador_tipo_id = user_types_list[2] if len(user_types_list) > 1 else 1
                
            pesquisadores = self.usuario_service.listar_usuarios(
                lista_tipos=[pesquisador_tipo_id], 
                apenas_ativos=False
            )

            self.pesquisadores_map = {
                pesq.nome: pesq.id_pessoa for pesq in pesquisadores
            }

            nome_pesq = list(self.pesquisadores_map.keys())

            self.option_pesquisadores.configure(values=nome_pesq)

            if nome_pesq:
                self.option_pesquisadores.set("Pesquisadores:")
        
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Erro ao carregar dados do usuário: {str(e)}",
                icon="cancel"
            ).get()
            self.voltar_callback()
    
    def definir_id_pesquisador_menu_opcao(self, escolha):
        self.id_pesq = self.pesquisadores_map.get(escolha)