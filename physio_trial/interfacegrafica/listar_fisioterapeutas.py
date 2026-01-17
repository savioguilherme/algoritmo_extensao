from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.context.app_context import current_user_types_list
from CTkMessagebox import CTkMessagebox
from dados.fisioterapeuta import Fisioterapeuta
from interfacegrafica.menu_atualiza_dados_usuario import MenuAtualizaDadosUsuario

class ListarFisioterapeutas(BaseFrame):

    '''Lista dos os Fisioterapeutas do sistema'''

    @autoparams()
    def __init__(self, master, voltar_callback, abrir_menu_atualiza_dados, usuario_service: BaseUsuarioService):
        super().__init__(master, "Lista de Fisioterapeutas")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.abrir_menu_atualiza_dados = abrir_menu_atualiza_dados
        
        self.usuario_service = usuario_service

        # Dados dos fisioterapeutas
        self.fisioterapeutas: list[Fisioterapeuta] = []

        # Configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.carregar_fisioterapeutas()

    def carregar_fisioterapeutas(self):
        try:
            user_types_list = current_user_types_list.get() or []
            
            fisioterapeuta_tipo_id = user_types_list[1] if len(user_types_list) > 1 else 1
                
            self.fisioterapeutas = self.usuario_service.listar_usuarios(lista_tipos=[fisioterapeuta_tipo_id], apenas_ativos=False)
            
            for i, fisio in enumerate(self.fisioterapeutas):
                self.bnt_nome = self.widgets.button(self, texto=fisio.nome, comando=lambda f_id=fisio.id_pessoa: self.abrir_menu_atualiza_dados(f_id), cor="Green")
                self.bnt_nome.grid(row=i+1, column=1, sticky="e", padx=(20,10), pady=(10,20))
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