import customtkinter
from interfacegrafica.base_frame import BaseFrame

class ListarPesquisadores(BaseFrame):

    ''' '''

    def __init__(self, master, voltar_callback):
        super().__init__(master, "Lista de Pesquisadores")

        self.voltar_callback = voltar_callback

        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.label_id = customtkinter.CTkLabel(self, text=self.texto_pesquisadores, font=("Arial", 20, "bold"))
        self.label_id.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.btn_voltar = customtkinter.CTkButton(self, text="Voltar", command=self.voltar_callback, font=("Arial", 20, "bold"), fg_color="red")
        self.btn_voltar.grid(row=3, column=1, padx=20, pady=20)