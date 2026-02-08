from inject import autoparams
import customtkinter as ctk

from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from interfacegrafica.agenda_pessoa.agenda_pessoa_widget import AgendaPessoaWidget

class AgendaPessoa(BaseFrame):
    """
    Tela para exibir e gerenciar a agenda de sessões de um ou mais usuários.
    Permite filtrar por pesquisador, fisioterapeuta ou paciente.
    """

    @autoparams()
    def __init__(self, master, voltar_callback,
                 pesquisadores_ids: list[int] | None = None,
                 fisioterapeutas_ids: list[int] | None = None,
                 pacientes_ids: list[int] | None = None):
        super().__init__(master, "Agenda")

        self.widgets = BaseWidgets()
        self.voltar_callback = voltar_callback
        self.pesquisadores_ids = pesquisadores_ids
        self.fisioterapeutas_ids = fisioterapeutas_ids
        self.pacientes_ids = pacientes_ids

        self.grid_columnconfigure((0, 1), weight=1) # Configure columns for buttons
        self.grid_rowconfigure(1, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10) # Span across 2 columns
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # AgendaPessoaWidget
        self.agenda_pessoa_widget = AgendaPessoaWidget(
            self.scrollable_frame,
            pesquisadores_ids=self.pesquisadores_ids,
            fisioterapeutas_ids=self.fisioterapeutas_ids,
            pacientes_ids=self.pacientes_ids
        )
        self.agenda_pessoa_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Botões de ação
        self.btn_salvar = self.widgets.button(self, texto="Salvar", comando=self._salvar_agenda, cor="green")
        self.btn_salvar.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=10)
        
        self.btn_voltar = self.widgets.button(self, texto="Voltar", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=10)

    def _salvar_agenda(self):
        """
        Invoca o método salvar de AgendaPessoaWidget para persistir as alterações.
        """
        self.agenda_pessoa_widget.salvar()
