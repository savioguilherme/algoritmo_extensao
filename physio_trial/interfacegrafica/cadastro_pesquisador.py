from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from CTkMessagebox import CTkMessagebox
from dados.pesquisador import Pesquisador

class CadastroPesquisador(BaseFrame):
    '''Classe que cria a tela de cadastro para inserir pesquisadores no sistema'''

    def __init__(self, master, voltar_callback):
        super().__init__(master, "Cadastro de Pesquisadores")

        self.voltar_callback = voltar_callback 
        self.widgets = BaseWidgets()

        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((0,1,2,3), weight=1)
        
        self.label_id = self.widgets.label(self, texto="ID Pesquisador:", cor="transparent")
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

        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=None, cor="blue")
        self.btn_salvar.grid(row=3, column=1, sticky="e", padx=10, pady=10)

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=3, column=2, sticky="w", padx=10, pady=10)