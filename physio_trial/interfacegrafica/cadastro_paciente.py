from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from CTkMessagebox import CTkMessagebox
from armazenamento.armazenamento import Armazenamento
from dados.paciente import Paciente

class CadastroPaciente(BaseFrame):

    '''Classe que cria a tela de cadastro para inserir pacientes no sistema'''

    def __init__(self, master, voltar_callback, abrir_restricoes):
        super().__init__(master, "Cadastro de Pacientes")

        self.voltar_callback = voltar_callback
        self.abrir_restricoes = abrir_restricoes
        self.storage = Armazenamento()
        self.widgets = BaseWidgets()

        #configurando o frame
        self.grid_rowconfigure((0,1,2,3,4,5), weight=0)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.label_nome = self.widgets.label(self, texto="Nome:", cor="transparent")
        self.label_nome.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.entry_nome = self.widgets.entry(self, None, None)
        self.entry_nome.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.label_pesquisador = self.widgets.label(self, "Escolha um pesquisador responsável: ", cor="transparent")
        self.label_pesquisador.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,10))
        
        self.optionmenu_pesquisador = self.widgets.option_menu(self, ["Joana"], None)
        self.optionmenu_pesquisador.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.label_fisioterapeuta = self.widgets.label(self, "Escolha um fisioterapeuta responsável: ", cor="transparent")
        self.label_fisioterapeuta.grid(row=3, column=1, sticky="e", padx=(20,10), pady=(10,10))
        
        self.optionmenu_fisioterapeuta = self.widgets.option_menu(self, ["Maria"], None)
        self.optionmenu_fisioterapeuta.grid(row=3, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.btn_restricao_paciente = self.widgets.button(self, texto="Cadastrar restrição", comando=self.abrir_restricoes, cor="blue")
        self.btn_restricao_paciente.grid(row=4, column=1, sticky="e", padx=(20,20), pady=(10,10))

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.salvar_paciente, cor="blue")
        self.btn_salvar.grid(row=5, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=5, column=2, sticky="w", padx=(10,20), pady=(10,20))

    def buscar_pesquisador(self):
        pass

    def buscar_fisioterapeuta(self):
        pass

    def salvar_paciente(self):
        id_paciente = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        if not (id_paciente and nome):
            CTkMessagebox(title="Erro", message="Preencha todos os campos antes de salvar!", icon="cancel")
            return
        # Criar o objeto Pesquisador
        paciente = Paciente(id_paciente, nome, None, None) #nome pesquisador e fisioterapeuta provisórios. 
        # Converter para dicionário simplificado para salvar no Excel
        dados = {
            "ID": paciente.id_pessoa,
            "Nome": paciente.nome,
        }
        try:
            self.storage.salvar("pacientes", dados)
            CTkMessagebox(title="Sucesso", message=f"Paciente '{nome}' cadastrado com sucesso!", icon="check")
            # Limpar campos
            self.entry_id.delete(0, "end")
            self.entry_nome.delete(0, "end")
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Falha ao salvar os dados: {e}", icon="cancel")