from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.context.app_context import current_user_types_list
from CTkMessagebox import CTkMessagebox
from dados.paciente import Paciente

class ListarPacientes(BaseFrame):

    '''Lista todos os pacientes cadastrados'''

    @autoparams()
    def __init__(self, master, voltar_callback, abrir_menu_paciente, usuario_service: BasePacienteService):
        super().__init__(master, "Lista de Pacientes")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback 
        self.abrir_menu_paciente = abrir_menu_paciente
        self.usuario_service = usuario_service

        self.pacientes_map: dict[str, int] = {}
        
        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.option_pacientes = self.widgets.option_menu(self, None, self.definir_id_pacientes_menu_opcao)
        self.option_pacientes.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(20,20), pady=(20,10))

        btn_abrir = self.widgets.button(self, texto="Abrir", comando=lambda: self.abrir_menu_paciente(self.id_fisio), cor="green")
        btn_abrir.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,20))

        self.carregar_pacientes()

    def carregar_pacientes(self):
        try:
            pacientes = self.usuario_service.listar_pacientes(
                apenas_ativos=False
            )
            
            self.pacientes_map = {
                paci.nome: paci.id_pessoa for paci in pacientes
            }

            nome_paci = list(self.pacientes_map.keys())

            self.option_pacientes.configure(values=nome_paci)

            if nome_paci:
               self.option_pacientes.set("Pacientes:")
        
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Erro ao carregar dados do usuário: {str(e)}", 
                icon="cancel"
            ).get()
            self.voltar_callback()

    def definir_id_pacientes_menu_opcao(self, escolha):
        self.id_fisio = self.pacientes_map.get(escolha)