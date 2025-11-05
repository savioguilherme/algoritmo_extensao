import customtkinter
from interfacegrafica.base_frame import BaseFrame
from armazenamento.armazenamento import Armazenamento
from dados.paciente import Paciente
from tkinter import messagebox

class CadastroPaciente(BaseFrame):



    def __init__(self, master, voltar_callback):
        super().__init__(master, "Cadastro de Pacientes")

        self.voltar_callback = voltar_callback
        self.storage = Armazenamento() 

        self.label_id = customtkinter.CTkLabel(self.container, text="ID Paciente:", font=("Arial", 20, "bold"))
        self.label_id.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.entry_id = customtkinter.CTkEntry(self.container)
        self.entry_id.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.label_nome = customtkinter.CTkLabel(self.container, text="Nome:", font=("Arial", 20, "bold"))
        self.label_nome.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        self.entry_nome = customtkinter.CTkEntry(self.container)
        self.entry_nome.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.btn_salvar = customtkinter.CTkButton(self.container, text="Salvar", command=self.salvar_paciente, font=("Arial", 20, "bold"))
        self.btn_salvar.grid(row=3, column=0, padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=3, column=1, padx=20, pady=20)

    def salvar_paciente(self):
        id_paciente = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()

        if not (id_paciente and nome):
            messagebox.showerror("Erro", "Preencha todos os campos antes de salvar!")
            return

        # Criar o objeto Pesquisador
        paciente = Paciente(id_paciente, nome)

        # Converter para dicionário simplificado para salvar no Excel
        dados = {
            "ID": paciente.id_pessoa,
            "Nome": paciente.nome,
        }

        try:
            self.storage.salvar("pacientes", dados)
            messagebox.showinfo("Sucesso", f"Paciente '{nome}' cadastrado com sucesso!")

            # Limpar campos
            self.entry_id.delete(0, "end")
            self.entry_nome.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar os dados: {e}")
