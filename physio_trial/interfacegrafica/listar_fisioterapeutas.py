import customtkinter
from interfacegrafica.base_frame import BaseFrame
from armazenamento.armazenamento import Armazenamento
from tkinter import messagebox

class ListarFisioterapeutas(BaseFrame):

    ''' '''

    def __init__(self, master, voltar_callback):
        super().__init__(master, "Lista de Fisioterapeutas")

        self.voltar_callback = voltar_callback
        self.guardar = Armazenamento()
        self.texto_fisioterapeutas = self.exibir_fisioterapeutas()

        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.label_id = customtkinter.CTkLabel(self, text=self.texto_fisioterapeutas, font=("Arial", 20, "bold"))
        self.label_id.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.btn_voltar = customtkinter.CTkButton(self, text="Voltar", command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=3, column=1, padx=20, pady=20)

    def exibir_fisioterapeutas(self):
        
        """Carrega e retorna o texto formatado com os fisioterapeutas cadastrados."""

        try:
            df = self.guardar.carregar("fisioterapeutas")

            if df.empty:
                return "Nenhum fisioterapeuta cadastrado."

            texto = "Fisioterapeutas cadastrados:\n\n"
            for i, row in df.iterrows():
                nome = row.get("Nome", "—")
                texto += f"• {nome} \n"

            return texto.strip()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar fisioterapeutas:\n{e}")
            return "Erro ao carregar dados."