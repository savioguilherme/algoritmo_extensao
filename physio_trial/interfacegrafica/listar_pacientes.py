from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.armazenamento import Armazenamento
from tkinter import messagebox

class ListarPacientes(BaseFrame):
    '''Lista todos os pacientes cadastrados'''

    def __init__(self, master, voltar_callback):
        super().__init__(master, "Lista de Pacientes")

        self.voltar_callback = voltar_callback
        self.guardar = Armazenamento()
        self.texto_pacientes = self.exibir_pacientes()
        self.widgets = BaseWidgets()

        #configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.label_nome = self.widgets.label(self, texto=self.texto_pacientes, cor="transparent")
        self.label_nome.grid(row=1, column=1, sticky="e", padx=(20,20), pady=(20,10))

        self.btn_paciente = self.widgets.button(self, texto="Mario", comando=self.voltar_callback, cor="transparent")
        self.btn_paciente.grid(row=2, column=1, sticky="e", padx=(20,20), pady=(10,10))

        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=3, column=1, sticky="e", padx=(20,20), pady=(10,20))

    def exibir_pacientes(self):
        """Carrega e retorna o texto formatado com os pacientes cadastrados."""

        try:
            df = self.guardar.carregar("pacientes")

            if df.empty:
                return "Nenhum paciente cadastrado."

            texto = "Pacientes cadastrados:\n\n"
            for i, row in df.iterrows():
                nome = row.get("Nome", "—")
                texto += f"• {nome} \n"

            return texto.strip()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar Pacientes:\n{e}")
            return "Erro ao carregar dados."