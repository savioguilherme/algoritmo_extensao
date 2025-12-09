from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from CTkMessagebox import CTkMessagebox
from armazenamento.armazenamento import Armazenamento
from dados.paciente import Paciente

class CadastroPaciente(BaseFrame):

    '''Classe que cria a tela de cadastro para inserir pacientes no sistema'''

    def __init__(self, master, voltar_callback):
        super().__init__(master, "Cadastro de Pacientes")

        self.voltar_callback = voltar_callback
        self.storage = Armazenamento()
        self.widgets = BaseWidgets()

        self.label_id = self.widgets.label(self.container, texto="ID Paciente:", cor="transparent")
        self.label_id.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.entry_id = self.widgets.entry(self.container, None)
        self.entry_id.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.label_nome = self.widgets.label(self.container, texto="Nome:", cor="transparent")
        self.label_nome.grid(row=1, column=2, sticky="e", padx=10, pady=10)

        self.entry_nome = self.widgets.entry(self.container, None)
        self.entry_nome.grid(row=1, column=3, sticky="w", padx=10, pady=10)

        self.btn_salvar = self.widgets.button(self.container, texto="Salvar", comando=self.salvar_paciente, cor="blue")
        self.btn_salvar.grid(row=2, column=1, sticky="e", padx=10, pady=10)

        self.btn_voltar = self.widgets.button(self.container, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=2, sticky="w", padx=10, pady=10)

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