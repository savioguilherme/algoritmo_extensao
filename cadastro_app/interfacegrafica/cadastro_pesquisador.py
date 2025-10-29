import customtkinter
from interfacegrafica.base_frame import BaseFrame
from armazenamento.guardar import Guardar

class CadastroPesquisador(BaseFrame):
    def __init__(self, master, voltar_callback, storage: Guardar):
        super().__init__(master, "Cadastro de Pesquisadores")

        self.voltar_callback = voltar_callback
        self.storage = storage  

        self.label_id = customtkinter.CTkLabel(self.container, text="ID Pesquisador:", font=("Arial", 20, "bold"))
        self.label_id.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.entry_id = customtkinter.CTkEntry(self.container)
        self.entry_id.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.label_nome = customtkinter.CTkLabel(self.container, text="Nome:", font=("Arial", 20, "bold"))
        self.label_nome.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        self.entry_nome = customtkinter.CTkEntry(self.container)
        self.entry_nome.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.btn_salvar = customtkinter.CTkButton(self.container, text="Salvar", command=self.enviar, font=("Arial", 20, "bold"))
        self.btn_salvar.grid(row=3, column=0, padx=20, pady=20)

        self.btn_voltar = customtkinter.CTkButton(self.container, text="Voltar", command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=3, column=1, padx=20, pady=20)

    def enviar(self):
        id_pesquisador = self.entry_id.get()
        nome = self.entry_nome.get()
        self.storage.adiciona_pesquisador(id_pesquisador, nome)
        print("Pesquisador salvo com sucesso!")
        self.storage.retorna_pesquisador()