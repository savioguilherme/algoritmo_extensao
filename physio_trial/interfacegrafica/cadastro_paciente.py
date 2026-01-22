from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.context.app_context import current_user_types_list
from CTkMessagebox import CTkMessagebox
from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador
from datetime import date

@autoparams()
class CadastroPaciente(BaseFrame):
    
    '''Classe que cria a tela de cadastro para inserir pacientes no sistema'''

    @autoparams()
    def __init__(self, master, voltar_callback, abrir_restricoes, usuario_paciente_service: BasePacienteService, usuario_service: BaseUsuarioService):
        super().__init__(master, "Cadastro de Pacientes")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.abrir_restricoes = abrir_restricoes

        self.fisioterapeutas: list[Fisioterapeuta] = []
        self.fisioterapeutas_map: dict[str, Fisioterapeuta] = {}

        self.pesquisadores: list[Pesquisador] = []
        self.pesquisadores_map: dict[str, Pesquisador] = {}

        self.usuario_service = usuario_service
        self.usuario_paciente_service = usuario_paciente_service
        
        #configurando o frame
        self.grid_rowconfigure((1,2,3,4,5,6), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.label_nome = self.widgets.label(self, texto="Nome:", cor="transparent")
        self.label_nome.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.entry_nome = self.widgets.entry(self, None, None)
        self.entry_nome.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_email = self.widgets.label(self, texto="Email:", cor="transparent")
        self.label_email.grid(row=2, column=1, sticky="e",padx=(20,10), pady=(10,10))

        self.entry_email = self.widgets.entry(self, None, None)
        self.entry_email.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_data_nascimento = self.widgets.label(self, texto="Data de Nascimento:", cor="transparent")
        self.label_data_nascimento.grid(row=3, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.entry_data_nascimento = self.widgets.entry(self, None, None)
        self.entry_data_nascimento.grid(row=3, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_fisioterapeuta = self.widgets.label(self, "Escolha um fisioterapeuta responsável: ", cor="transparent")
        self.label_fisioterapeuta.grid(row=4, column=1, sticky="e", padx=(20,10), pady=(10,10))
        
        self.optionmenu_fisioterapeuta = self.widgets.option_menu(self, self.fisioterapeutas, None)
        self.optionmenu_fisioterapeuta.grid(row=4, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_pesquisador = self.widgets.label(self, "Escolha um pesquisador responsável: ", cor="transparent")
        self.label_pesquisador.grid(row=5, column=1, sticky="e", padx=(20,10), pady=(10,10))
        
        self.optionmenu_pesquisador = self.widgets.option_menu(self, self.pesquisadores, None)
        self.optionmenu_pesquisador.grid(row=5, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_cadastro_restricoes = self.widgets.label(self, "Cadastrar Horários:", cor="transparent")
        self.label_cadastro_restricoes.grid(row=6, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.btn_restricao_paciente = self.widgets.button(self, texto="Cadastrar Horários", comando=self.abrir_restricoes, cor="blue")
        self.btn_restricao_paciente.grid(row=6, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.realizar_cadastro_paciente, cor="blue")
        self.btn_salvar.grid(row=7, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=7, column=2, sticky="w", padx=(10,20), pady=(10,20))

        self.listar_fisioterapeuta_ativos()
        self.listar_pesquisadores_ativos()

    def realizar_cadastro_paciente(self):

        nome = self.entry_nome.get()
        email = self.entry_email.get()
        data_nascimento = self.entry_data_nascimento.get()
        pesquisador = self.optionmenu_pesquisador.get()
        nome_fisio = self.optionmenu_fisioterapeuta.get()
        fisioterapeuta = self.fisioterapeutas_map.get(nome_fisio)
        nome_pesq = self.optionmenu_pesquisador.get()
        pesquisador = self.pesquisadores_map.get(nome_pesq)


        if not nome or not email or not data_nascimento or not pesquisador or not fisioterapeuta: 
            CTkMessagebox(
                title="Erro", 
                message="Preencha todos os campos!", 
                icon="cancel"
            ).get()
            return
        
        data_array: list[int] = [int(data) for data in data_nascimento.split("/")]

        novo_paciente: Paciente = Paciente(
            id_paciente=1,
            nome_paciente=nome,
            email=email,
            data_nascimento=date(data_array[2], data_array[1], data_array[0]),
            pesquisador=pesquisador,
            fisioterapeuta=fisioterapeuta,
            status_paciente=True
        )

        paciente = self.usuario_paciente_service.cadastrar_paciente(paciente=novo_paciente)

        if paciente is not None: 
            CTkMessagebox(
                title="Cadastrado", 
                message="Paciente Cadastrado com Sucesso!", 
                icon="check"
            ).get()
            self.voltar_callback()
        else:
            CTkMessagebox(
                title="Erro no Cadastro", 
                message="Não foi possível cadastrar o usuário!", 
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
                self.optionmenu_fisioterapeuta.set("Fisioterapeuta: ")

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
                self.optionmenu_pesquisador.set("Pesquisador: ")
        
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Erro ao carregar dados do usuário: {str(e)}",
                icon="cancel"
            ).get()

            self.voltar_callback()