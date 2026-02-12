import customtkinter as ctk
from inject import autoparams
from datetime import date

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


class MenuPaciente(BaseFrame): 

    '''Menu para atualizar e verificar dados de um paciente'''

    @autoparams()
    def __init__(self, master, user_id, voltar_callback, paciente_service: BasePacienteService, usuario_service: BaseUsuarioService):
        super().__init__(master, titulo="Menu Paciente")

        self.widgets = BaseWidgets()
        self.paciente_service = paciente_service
        self.usuario_service = usuario_service
        self.voltar_callback = voltar_callback
        self.user_id = user_id
        self.paciente: Paciente | None = None

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
        self.label_nome.grid(row=0, column=0, sticky="e", padx=(20,10) ,pady=(10,5))
        self.entry_nome = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_nome.grid(row=0, column=1, sticky="ew", padx=(10,20), pady=(10,5))

        self.label_email = self.widgets.label(self.scrollable_frame, texto="Email:", cor="transparent")
        self.label_email.grid(row=1, column=0, sticky="e",padx=(20,10), pady=(5,5))
        self.entry_email = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_email.grid(row=1, column=1, sticky="ew", padx=(10,20), pady=(5,5))

        self.label_data_nascimento = self.widgets.label(self.scrollable_frame, texto="Data de Nascimento (dd/mm/aaaa):", cor="transparent")
        self.label_data_nascimento.grid(row=2, column=0, sticky="e", padx=(20,10), pady=(5,5))
        self.entry_data_nascimento = self.widgets.entry(self.scrollable_frame, None, None)
        self.entry_data_nascimento.grid(row=2, column=1, sticky="ew", padx=(10,20), pady=(5,5))
        
        self.label_fisioterapeuta = self.widgets.label(self.scrollable_frame, "Fisioterapeuta:", cor="transparent")
        self.label_fisioterapeuta.grid(row=3, column=0, sticky="e", padx=(20,10), pady=(10,10))
        self.optionmenu_fisioterapeuta = self.widgets.option_menu(self.scrollable_frame, [], None)
        self.optionmenu_fisioterapeuta.grid(row=3, column=1, sticky="ew", padx=(10,20), pady=(10,10))

        self.label_pesquisador = self.widgets.label(self.scrollable_frame, "Pesquisador:", cor="transparent")
        self.label_pesquisador.grid(row=4, column=0, sticky="e", padx=(20,10), pady=(10,10))
        self.optionmenu_pesquisador = self.widgets.option_menu(self.scrollable_frame, [], None)
        self.optionmenu_pesquisador.grid(row=4, column=1, sticky="ew", padx=(10,20), pady=(10,10))
        
        self.label_status_conclusao = self.widgets.label(self.scrollable_frame, "Concluiu a pesquisa: ", cor="transparent")
        self.label_status_conclusao.grid(row=5, column=0, sticky="e", padx=(20,10), pady=(10,10))
        self.switch_status_conclusao = self.widgets.switch(self.scrollable_frame, texto="", comando=None)
        self.switch_status_conclusao.grid(row=5, column=1, sticky="w", padx=(10,20), pady=(10,10))

        self.label_status_abandono = self.widgets.label(self.scrollable_frame, "Abandonou a pesquisa: ", cor="transparent")
        self.label_status_abandono.grid(row=6, column=0, sticky="e", padx=(20,10), pady=(10,10))
        self.switch_status_abandono = self.widgets.switch(self.scrollable_frame, texto="", comando=None)
        self.switch_status_abandono.grid(row=6, column=1, sticky="w", padx=(10,20), pady=(10,10))

        self.restricoes_widget = None

        # Acões
        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.__atualizar_dados, cor="Green")
        self.btn_salvar.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=10)

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=10)

        self.__carregar_paciente()
        self.__listar_fisioterapeuta_ativos()
        self.__listar_pesquisadores_ativos()

    def __carregar_paciente(self):
        try:
            self.paciente = self.paciente_service.consultar(self.user_id)
            if self.paciente:
                self.entry_nome.insert(0, self.paciente.nome)
                self.entry_email.insert(0, self.paciente.email)
                self.entry_data_nascimento.insert(0, self.__formatar_data(self.paciente.data_nascimento))

                if self.paciente.conclusao_pesquisa:
                    self.switch_status_conclusao.select()
                if self.paciente.abandono_pesquisa:
                    self.switch_status_abandono.select()

                self.restricoes_widget = RestricoesPessoa(self.scrollable_frame, self.paciente.restricoes_paciente)
                self.restricoes_widget.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Erro ao carregar dados do paciente: {str(e)}", icon="cancel")
            self.voltar_callback()
    
    def __formatar_data(self, data):
        if hasattr(data, 'strftime'):
            return data.strftime("%d/%m/%Y")
        return str(data)

    def __listar_fisioterapeuta_ativos(self):
        try:
            user_types_list = current_user_types_list.get() or []
            fisioterapeuta_tipo_id = user_types_list[1] if len(user_types_list) > 1 else 1
            fisioterapeutas = self.usuario_service.listar_usuarios(lista_tipos=[fisioterapeuta_tipo_id], apenas_ativos=True)
            self.fisioterapeutas_map = {fisio.nome: fisio for fisio in fisioterapeutas}
            nomes_fisio = list(self.fisioterapeutas_map.keys())
            self.optionmenu_fisioterapeuta.configure(values=nomes_fisio)
            if self.paciente and self.paciente.fisioterapeuta_responsavel:
                self.optionmenu_fisioterapeuta.set(self.paciente.fisioterapeuta_responsavel.nome)
            elif nomes_fisio:
                self.optionmenu_fisioterapeuta.set(nomes_fisio[0])
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Erro ao carregar fisioterapeutas: {str(e)}", icon="cancel")
            self.voltar_callback()

    def __listar_pesquisadores_ativos(self):
        try:
            user_types_list = current_user_types_list.get() or []
            pesquisador_tipo_id = user_types_list[2] if len(user_types_list) > 2 else 1
            pesquisadores = self.usuario_service.listar_usuarios(lista_tipos=[pesquisador_tipo_id], apenas_ativos=True)
            self.pesquisadores_map = {pesq.nome: pesq for pesq in pesquisadores}
            nome_pesq = list(self.pesquisadores_map.keys())
            self.optionmenu_pesquisador.configure(values=nome_pesq)
            if self.paciente and self.paciente.pesquisador_responsavel:
                self.optionmenu_pesquisador.set(self.paciente.pesquisador_responsavel.nome)
            elif nome_pesq:
                self.optionmenu_pesquisador.set(nome_pesq[0])
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Erro ao carregar pesquisadores: {str(e)}", icon="cancel")
            self.voltar_callback()

    def __atualizar_dados(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        data_nascimento_str = self.entry_data_nascimento.get()
        restricoes = self.restricoes_widget.get_dados()
        
        nome_fisio = self.optionmenu_fisioterapeuta.get()
        fisioterapeuta = self.fisioterapeutas_map.get(nome_fisio)
        nome_pesq = self.optionmenu_pesquisador.get()
        pesquisador = self.pesquisadores_map.get(nome_pesq)

        status_conclusao = self.switch_status_conclusao.get() == 1
        status_abandono = self.switch_status_abandono.get() == 1

        if not nome or not email or not data_nascimento_str or not fisioterapeuta or not pesquisador:
            CTkMessagebox(title="Erro", message="Preencha todos os campos!", icon="cancel").get()
            return

        if not restricoes:
            CTkMessagebox(title="Erro", message="Restrições ou disponibilidades inválidas!", icon="cancel").get()
            return
            
        try:
            data_array = [int(d) for d in data_nascimento_str.split("/")]
            data_nascimento = date(data_array[2], data_array[1], data_array[0])
        except (ValueError, IndexError):
            CTkMessagebox(title="Erro", message="Formato de data inválido. Use dd/mm/aaaa.", icon="cancel").get()
            return
        
        paciente_atualizado = Paciente(
            id_paciente=self.paciente.id_pessoa,
            nome_paciente=nome,
            email=email,
            data_nascimento=data_nascimento,
            pesquisador=pesquisador,
            fisioterapeuta=fisioterapeuta,
            status_paciente=self.paciente.status_pessoa
        )
        paciente_atualizado.restricoes_paciente = restricoes
        # As seções não são modificadas, mas são necessárias para atualizar_paciente
        paciente_atualizado.sessoes_paciente = self.paciente.sessoes_paciente

        #try:
        self.paciente_service.atualizar_paciente(
            paciente=paciente_atualizado, 
            status_abandono=status_abandono, 
            status_conclusao=status_conclusao
        )
        CTkMessagebox(title="Sucesso", message="Paciente atualizado com sucesso!", icon="check").get()
        self.voltar_callback()
        #except Exception as e:
        #    CTkMessagebox(title="Erro", message=f"Erro ao atualizar paciente: {str(e)}", icon="cancel").get()
