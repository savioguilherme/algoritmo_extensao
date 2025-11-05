import customtkinter
from interfacegrafica.base_frame import BaseFrame
from armazenamento.armazenamento import Armazenamento
from dados.fisioterapeuta import Fisioterapeuta
from tkinter import messagebox

class CadastroFisioterapeuta(BaseFrame):

    ''' '''

    def __init__(self, master, voltar_callback, storage: Armazenamento):
        super().__init__(master, "Cadastro de Fisioterapeutas")

        self.voltar_callback = voltar_callback
        self.storage = storage 

        self.label_id = customtkinter.CTkLabel(self.container, text="ID Fisioterapeuta:", font=("Arial", 20, "bold"))
        self.label_id.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        
        self.entry_id = customtkinter.CTkEntry(self.container)
        self.entry_id.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.label_nome = customtkinter.CTkLabel(self.container, text="Nome:", font=("Arial", 20, "bold"))
        self.label_nome.grid(row=1, column=2, sticky="e", padx=10, pady=10)

        self.entry_nome = customtkinter.CTkEntry(self.container)
        self.entry_nome.grid(row=1, column=3, sticky="w", padx=10, pady=10)

        self.label_login = customtkinter.CTkLabel(self.container, text="Login:", font=("Arial", 20, "bold"))
        self.label_login.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        self.entry_login = customtkinter.CTkEntry(self.container)
        self.entry_login.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.label_senha = customtkinter.CTkLabel(self.container, text="Senha:", font=("Arial", 20, "bold"))
        self.label_senha.grid(row=2, column=2, sticky="e", padx=10, pady=10)

        self.entry_senha = customtkinter.CTkEntry(self.container, show="*")
        self.entry_senha.grid(row=2, column=3, sticky="w", padx=10, pady=10)

        self.btn_salvar = customtkinter.CTkButton(self.container, text="Salvar", command=self.salvar_fisioterapeuta, font=("Arial", 20, "bold"))
        self.btn_salvar.grid(row=3, column=0, padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=3, column=1, padx=20, pady=20)

    def salvar_fisioterapeuta(self):
        id_fisio = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not (id_fisio and nome and login and senha):
            messagebox.showerror("Erro", "Preencha todos os campos antes de salvar!")
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
            messagebox.showinfo("Sucesso", f"Fisioterapeuta '{nome}' cadastrado com sucesso!")

            # Limpar campos
            self.entry_id.delete(0, "end")
            self.entry_nome.delete(0, "end")
            self.entry_login.delete(0, "end")
            self.entry_senha.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar os dados: {e}")