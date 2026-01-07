from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from dados.fisioterapeuta import Fisioterapeuta
from inject import autoparams
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.context.app_context import current_user_types_list

class ListarFisioterapeutas(BaseFrame):

    '''Lista dos os Fisioterapeutas do sistema'''

    @autoparams()
    def __init__(self, master, voltar_callback, usuario_service: BaseUsuarioService):
        super().__init__(master, "Lista de Fisioterapeutas")

        self.voltar_callback = voltar_callback
        self.widgets = BaseWidgets()
        self.usuario_service = usuario_service

        # Dados dos fisioterapeutas
        self.fisioterapeutas: list[Fisioterapeuta] = []

        # Configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        label_nome = self.widgets.label(self, texto="Nome:", cor="transparent")
        label_nome.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))

        label_email = self.widgets.label(self, texto="Email:", cor="transparent")
        label_email.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.carregar_fisioterapeutas()

    def carregar_fisioterapeutas(self):
        try:
            user_types_list = current_user_types_list.get() or []
            
            fisioterapeuta_tipo_id = user_types_list[1] if len(user_types_list) > 1 else 1
                
            self.fisioterapeutas = self.usuario_service.listar_usuarios(lista_tipos=[fisioterapeuta_tipo_id], apenas_ativos=False)
            
            if not self.fisioterapeutas:
                self.label_vazio = self.widgets.label(self, texto="Nenhum fisioterapeuta encontrado", cor="transparent")
                self.label_vazio.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))
                return self._criar_botao_voltar(2)
            
            for i, fisio in enumerate(self.fisioterapeutas):
                label = self.widgets.label(self, texto=fisio.nome, cor="transparent")
                label.grid(row=i+2, column=1, sticky="e", padx=(20,10), pady=(10,20))
                label_email = self.widgets.label(self, texto=fisio.email, cor="transparent")
                label_email.grid(row=i+2, column=2, sticky="w", padx=(20,10), pady=(10,20))
            return self._criar_botao_voltar(i)
        
        except Exception as e:
            self.label_erro = self.widgets.label(self, texto=f"Erro ao carregar fisioterapeutas: {str(e)}", cor="transparent")
            self.label_erro.grid(row=1, column=1, padx=20, pady=20)
    
    def _criar_botao_voltar(self, i):
        btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        btn_voltar.grid(row=i+3, column=1, sticky="e", padx=(20,20), pady=(10,20))