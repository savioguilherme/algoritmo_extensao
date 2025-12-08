import customtkinter
from interfacegrafica.base_frame import BaseFrame
from armazenamento.armazenamento import Armazenamento
from dados.pesquisador import Pesquisador
from tkinter import messagebox
from interfacegrafica.base_widgets import BaseWidgets

class CadastroPesquisador(BaseFrame):

    '''Classe que cria a tela de cadastro para inserir pesquisadores no sistema'''

    def __init__(self, master, voltar_callback):
        super().__init__(master, "Cadastro de Pesquisadores")

        self.voltar_callback = voltar_callback
        self.storage = Armazenamento()  
        self.widgets = BaseWidgets()

        self.label_id = self.widgets.label(self.container, texto="ID Pesquisador:")
        self.label_id.grid(row=1, column=0, sticky="e", padx=20, pady=20)

        self.entry_id = customtkinter.CTkEntry(self.container)
        self.entry_id.grid(row=1, column=1, sticky="w", padx=20, pady=20)

        self.label_nome = customtkinter.CTkLabel(self.container, text="Nome:", font=("Arial", 20, "bold"))
        self.label_nome.grid(row=1, column=2, sticky="e", padx=20, pady=20)

        self.entry_nome = customtkinter.CTkEntry(self.container)
        self.entry_nome.grid(row=1, column=3, sticky="w", padx=20, pady=20)

        self.label_login = customtkinter.CTkLabel(self.container, text="Login:", font=("Arial", 20, "bold"))
        self.label_login.grid(row=2, column=0, sticky="e", padx=20, pady=20)

        self.entry_login = customtkinter.CTkEntry(self.container)
        self.entry_login.grid(row=2, column=1, sticky="w", padx=20, pady=20)

        self.label_senha = customtkinter.CTkLabel(self.container, text="Senha:", font=("Arial", 20, "bold"))
        self.label_senha.grid(row=2, column=2, sticky="e", padx=20, pady=20)

        self.entry_senha = customtkinter.CTkEntry(self.container, show="*")
        self.entry_senha.grid(row=2, column=3, sticky="w", padx=20, pady=20)

        self.btn_salvar = customtkinter.CTkButton(self.container, text="Salvar", command=self.salvar_pesquisador, font=("Arial", 20, "bold"))
        self.btn_salvar.grid(row=3, column=1, sticky="e", padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=3, column=2, sticky="w", padx=20, pady=20)

    def salvar_pesquisador(self):
        id_pesquisador = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not (id_pesquisador and nome and login and senha):
            messagebox.showerror("Erro", "Preencha todos os campos antes de salvar!")
            return

        # Criar o objeto Pesquisador
        pesquisador = Pesquisador(id_pesquisador, nome, login, senha)

        # Converter para dicionário simplificado para salvar no Excel
        dados = {
            "ID": pesquisador.id_pessoa,
            "Nome": pesquisador.nome,
            "Login": pesquisador.login,
            "Senha": pesquisador.senha
        }

        try:
            self.storage.salvar("pesquisadores", dados)
            messagebox.showinfo("Sucesso", f"Pesquisador '{nome}' cadastrado com sucesso!")

            # Limpar campos
            self.entry_id.delete(0, "end")
            self.entry_nome.delete(0, "end")
            self.entry_login.delete(0, "end")
            self.entry_senha.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar os dados: {e}")