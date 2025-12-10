from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from CTkMessagebox import CTkMessagebox
from armazenamento.armazenamento import Armazenamento
from dados.fisioterapeuta import Fisioterapeuta
from CTkMessagebox import CTkMessagebox

class CadastroFisioterapeuta(BaseFrame):

    '''Classe que gera a tela de cadastro de um fisioterapeuta'''

    def __init__(self, master, voltar_callback):
        super().__init__(master, "Cadastro de Fisioterapeutas")

        self.voltar_callback = voltar_callback
        self.storage = Armazenamento()
        self.widgets = BaseWidgets()

        self.label_id = self.widgets.label(self, texto="ID Fisioterapeuta:", cor="transparent")
        self.label_id.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        
        self.entry_id = self.widgets.entry(self, None)
        self.entry_id.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.label_nome = self.widgets.label(self, texto="Nome:", cor="transparent")
        self.label_nome.grid(row=1, column=2, sticky="e", padx=10, pady=10)

        self.entry_nome = self.widgets.entry(self, None)
        self.entry_nome.grid(row=1, column=3, sticky="w", padx=10, pady=10)

        self.label_login = self.widgets.label(self, texto="Login:", cor="transparent")
        self.label_login.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        self.entry_login = self.widgets.entry(self, None)
        self.entry_login.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.label_senha = self.widgets.label(self, texto="Senha:", cor="transparent")
        self.label_senha.grid(row=2, column=2, sticky="e", padx=10, pady=10)

        self.entry_senha = self.widgets.entry(self, "*")
        self.entry_senha.grid(row=2, column=3, sticky="w", padx=10, pady=10)

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self.salvar_fisioterapeuta, cor="blue")
        self.btn_salvar.grid(row=3, column=1, sticky="e", padx=10, pady=10)

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=3, column=2, sticky="w", padx=10, pady=10)

    def salvar_fisioterapeuta(self):
        id_fisio = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not (id_fisio and nome and login and senha):
            CTkMessagebox(title="Erro", message="Preencha todos os campos antes de salvar!", icon="cancel")
            return

        # Criar o objeto Fisioterapeuta
        fisioterapeuta = Fisioterapeuta(id_fisio, nome, login, senha)

        # Converter para dicionário simplificado para salvar no Excel
        dados = {
            "ID": fisioterapeuta.id_pessoa,
            "Nome": fisioterapeuta.nome,
            "Login": fisioterapeuta.login,
            "Senha": fisioterapeuta.senha
        }

        try:
            self.storage.salvar("fisioterapeutas", dados)
            CTkMessagebox(title="Sucesso", message=f"Fisioterapeuta, '{nome}' cadastrado com sucesso", icon="check")
            # Limpar campos
            self.entry_id.delete(0, "end")
            self.entry_nome.delete(0, "end")
            self.entry_login.delete(0, "end")
            self.entry_senha.delete(0, "end")

        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Falha ao salvar os dados: {e}", icon="cancel")