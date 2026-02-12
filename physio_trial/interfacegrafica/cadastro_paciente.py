from inject import autoparams
from datetime import date
import customtkinter as ctk

from CTkMessagebox import CTkMessagebox

from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from interfacegrafica.restricoes_pessoa.restricoes_pessoa import RestricoesPessoa
from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.context.app_context import current_user_types_list
from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador

@autoparams()
class CadastroPaciente(BaseFrame):
    
    '''Classe que cria a tela de cadastro para inserir pacientes no sistema'''

    @autoparams()
    def __init__(self, master, voltar_callback, paciente_service: BasePacienteService, usuario_service: BaseUsuarioService):
        super().__init__(master, "Cadastro de Pacientes")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.paciente_service = paciente_service
        self.usuario_service = usuario_service
        
        self.fisioterapeutas: list[Fisioterapeuta] = []
        self.fisioterapeutas_map: dict[str, Fisioterapeuta] = {}

        self.pesquisadores: list[Pesquisador] = []
        self.pesquisadores_map: dict[str, Pesquisador] = {}

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        self.label_nome = self.widgets.label(self.scrollable_frame, texto="Nome:", cor="transparent")
        self.label_nome.grid(row=0, column=0, sticky="e", padx=(20, 10), pady=(10, 10))

        self.entry_nome = self.widgets.entry(self.scrollable_frame,None,None)
        self.entry_nome.grid(row=0, column=1, sticky="ew", padx=(10, 20), pady=(10, 10))

        self.label_email = self.widgets.label(self.scrollable_frame, texto="Email:", cor="transparent")
        self.label_email.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=(10, 10))

        self.entry_email = self.widgets.entry(self.scrollable_frame,None,None)
        self.entry_email.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=(10, 10))

        self.label_data_nascimento = self.widgets.label(self.scrollable_frame, texto="Data de Nascimento (dd/mm/aaaa):", cor="transparent")
        self.label_data_nascimento.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=(10, 10))

        self.entry_data_nascimento = self.widgets.entry(self.scrollable_frame,None,None)
        self.entry_data_nascimento.grid(row=2, column=1, sticky="ew", padx=(10, 20), pady=(10, 10))

        self.label_fisioterapeuta = self.widgets.label(self.scrollable_frame, "Escolha um fisioterapeuta responsável: ", cor="transparent")
        self.label_fisioterapeuta.grid(row=3, column=0, sticky="e", padx=(20,10), pady=(10,10))
        
        self.optionmenu_fisioterapeuta = self.widgets.option_menu(self.scrollable_frame, [], None)
        self.optionmenu_fisioterapeuta.grid(row=3, column=1, sticky="ew", padx=(10,20), pady=(10,10))

        self.label_pesquisador = self.widgets.label(self.scrollable_frame, "Escolha um pesquisador responsável: ", cor="transparent")
        self.label_pesquisador.grid(row=4, column=0, sticky="e", padx=(20,10), pady=(10,10))
        
        self.optionmenu_pesquisador = self.widgets.option_menu(self.scrollable_frame, [], None)
        self.optionmenu_pesquisador.grid(row=4, column=1, sticky="ew", padx=(10,20), pady=(10,10))

        # Restrições
        self.restricoes_widget = RestricoesPessoa(self.scrollable_frame)
        self.restricoes_widget.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Ações
        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self._realizar_cadastro_paciente, cor="green")
        self.btn_salvar.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=10)
        
        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=10)

        self.listar_fisioterapeuta_ativos()
        self.listar_pesquisadores_ativos()

    def _realizar_cadastro_paciente(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        data_nascimento_str = self.entry_data_nascimento.get()
        nome_fisio = self.optionmenu_fisioterapeuta.get()
        fisioterapeuta = self.fisioterapeutas_map.get(nome_fisio)
        nome_pesq = self.optionmenu_pesquisador.get()
        pesquisador = self.pesquisadores_map.get(nome_pesq)

        if not nome or not email or not data_nascimento_str or not pesquisador or not fisioterapeuta: 
            CTkMessagebox(
                title="Erro", 
                message="Preencha todos os campos!", 
                icon="cancel"
            ).get()
            return
        
        try:
            data_array = [int(d) for d in data_nascimento_str.split("/")]
            data_nascimento = date(data_array[2], data_array[1], data_array[0])
        except (ValueError, IndexError):
            CTkMessagebox(title="Erro", message="Formato de data inválido. Use dd/mm/aaaa.", icon="cancel").get()
            return

        restricoes = self.restricoes_widget.get_dados()

        novo_paciente: Paciente = Paciente(
            id_paciente=None, # O banco de dados irá gerar o ID
            nome_paciente=nome,
            email=email,
            data_nascimento=data_nascimento,
            pesquisador=pesquisador,
            fisioterapeuta=fisioterapeuta,
            status_paciente=True
        )
        novo_paciente.restricoes_paciente = restricoes

        paciente_id = self.paciente_service.cadastrar_paciente(paciente=novo_paciente)

        if paciente_id is not None: 
            CTkMessagebox(
                title="Cadastrado", 
                message="Paciente Cadastrado com Sucesso!", 
                icon="check"
            ).get()
            self.voltar_callback()
        else:
            CTkMessagebox(
                title="Erro no Cadastro", 
                message="Não foi possível cadastrar o paciente!", 
                icon="cancel"
            ).get()
            return

    def listar_fisioterapeuta_ativos(self):
        try:
            user_types_list = current_user_types_list.get() or []
            fisioterapeuta_tipo_id = user_types_list[1] if len(user_types_list) > 1 else 1
                
            fisioterapeutas = self.usuario_service.listar_usuarios(
                lista_tipos=[fisioterapeuta_tipo_id], 
                apenas_ativos=True
            )
        
            self.fisioterapeutas_map = {
                fisio.nome: fisio for fisio in fisioterapeutas
            }

            nomes_fisio = list(self.fisioterapeutas_map.keys())

            self.optionmenu_fisioterapeuta.configure(values=nomes_fisio)

            if nomes_fisio:
                self.optionmenu_fisioterapeuta.set(nomes_fisio[0])

        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Erro ao carregar dados do usuário: {str(e)}", 
                icon="cancel"
            ).get()

            self.voltar_callback()

    def listar_pesquisadores_ativos(self):
        try:
            user_types_list = current_user_types_list.get() or []
            pesquisador_tipo_id = user_types_list[2] if len(user_types_list) > 1 else 1

            pesquisadores = self.usuario_service.listar_usuarios(
                lista_tipos=[pesquisador_tipo_id],
                apenas_ativos=True
            )

            self.pesquisadores_map = {
                pesq.nome: pesq for pesq in pesquisadores
            }

            nome_pesq = list(self.pesquisadores_map.keys())

            self.optionmenu_pesquisador.configure(values=nome_pesq)

            if nome_pesq:
                self.optionmenu_pesquisador.set(nome_pesq[0])
        
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Erro ao carregar dados do usuário: {str(e)}",
                icon="cancel"
            ).get()

            self.voltar_callback()
