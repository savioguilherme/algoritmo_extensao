from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.context.app_context import current_user_types_list
from CTkMessagebox import CTkMessagebox
from dados.fisioterapeuta import Fisioterapeuta

class ListarFisioterapeutas(BaseFrame):

    '''Lista dos os Fisioterapeutas do sistema'''

    @autoparams()
    def __init__(self, master, voltar_callback, abrir_menu_atualiza_dados, usuario_service: BaseUsuarioService):
        super().__init__(master, "Lista de Fisioterapeutas")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.abrir_menu_atualiza_dados = abrir_menu_atualiza_dados
        
        self.usuario_service = usuario_service

        self.fisioterapeutas_map: dict[str, int] = {}

        # Configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.option_fisioterapeutas = self.widgets.option_menu(self, None, self.definir_id_fisioterapeuta_menu_opcao)
        self.option_fisioterapeutas.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(20,20), pady=(20,10))

        btn_abrir = self.widgets.button(self, texto="Abrir", comando=lambda: self.abrir_menu_atualiza_dados(self.id_fisio), cor="green")
        btn_abrir.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,20))

        self.carregar_fisioterapeutas()

    def carregar_fisioterapeutas(self):
        try:
            user_types_list = current_user_types_list.get() or []
            
            fisioterapeuta_tipo_id = user_types_list[1] if len(user_types_list) > 1 else 1
                
            fisioterapeutas = self.usuario_service.listar_usuarios(
                lista_tipos=[fisioterapeuta_tipo_id], 
                apenas_ativos=False
            )
            
            self.fisioterapeutas_map = {
                fisio.nome: fisio.id_pessoa for fisio in fisioterapeutas
            }
            nome_fisio = list(self.fisioterapeutas_map.keys())

            self.option_fisioterapeutas.configure(values=nome_fisio)

            if nome_fisio:
               self.option_fisioterapeutas.set("Fisioterapeutas:")
        
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Erro ao carregar dados do usuário: {str(e)}", 
                icon="cancel"
            ).get()
            self.voltar_callback()

    def definir_id_fisioterapeuta_menu_opcao(self, escolha):
        self.id_fisio = self.fisioterapeutas_map.get(escolha)