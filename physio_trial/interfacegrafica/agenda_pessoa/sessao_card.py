import customtkinter as ctk
from datetime import date, time, datetime
from dados.sessao import Sessao
from copy import copy

class SessaoCard(ctk.CTkFrame):
    """
    Card para exibir e editar os detalhes de uma sessão.
    """
    def __init__(self, parent, sessao: Sessao, avisos: list[str] | None = None):
        super().__init__(parent)
        self.sessao = sessao
        self.avisos = avisos or []

        # Estilo
        self.configure(fg_color=["#EEEEEE", "#222222"], corner_radius=10)

        # Configuração do Grid
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure((1, 3), weight=1)

        # Linha 0: Nome do Paciente e sessão
        lbl_paciente = ctk.CTkLabel(self, text=f"Paciente: {sessao.paciente.nome}", font=("Arial", 14, "bold"))
        lbl_paciente.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        try:
            tipo_sessao = sessao.codigo[0]
            numero_sessao = int(sessao.codigo[1:])+1
            if tipo_sessao == "S":
                nome_sessao = f"Sessão {numero_sessao}"
            elif tipo_sessao == "F":
                nome_sessao = f"Follow-up {numero_sessao}"
        except:
            nome_sessao = "Sessão desconhecida"
        lbl_sessao = ctk.CTkLabel(self, text=nome_sessao, font=("Arial", 14, "bold"))
        lbl_sessao.grid(row=0, column=2, columnspan=2, sticky="e", padx=10, pady=(10, 5))

        # Linha 1: Dia e Horário
        lbl_dia = ctk.CTkLabel(self, text="Dia (DD/MM/AAAA):")
        lbl_dia.grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))
        self.dia_entry = ctk.CTkEntry(self, placeholder_text="DD/MM/AAAA")
        if sessao.dia:
            self.dia_entry.insert(0, sessao.dia.strftime("%d/%m/%Y"))
        self.dia_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=(10, 5))

        lbl_horario = ctk.CTkLabel(self, text="Horário (HH:MM):")
        lbl_horario.grid(row=1, column=2, sticky="w", padx=10, pady=(10, 5))
        self.horario_entry = ctk.CTkEntry(self, placeholder_text="HH:MM")
        if sessao.horario:
            self.horario_entry.insert(0, sessao.horario.strftime("%H:%M"))
        self.horario_entry.grid(row=1, column=3, sticky="ew", padx=10, pady=(10, 5))

        # Linha 2: Agendamento e Conclusão
        lbl_agendamento = ctk.CTkLabel(self, text="Agendar automaticamente:")
        lbl_agendamento.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 10))
        self.agendamento_var = ctk.BooleanVar(value=not sessao.status_agendamento)
        agendamento_toggle = ctk.CTkSwitch(self, text="", variable=self.agendamento_var)
        agendamento_toggle.grid(row=2, column=1, sticky="w", padx=10, pady=(5, 10))

        lbl_conclusao = ctk.CTkLabel(self, text="Concluída:")
        lbl_conclusao.grid(row=2, column=2, sticky="w", padx=10, pady=(5, 10))
        self.conclusao_var = ctk.BooleanVar(value=sessao.conclusao)
        conclusao_toggle = ctk.CTkSwitch(self, text="", variable=self.conclusao_var)
        conclusao_toggle.grid(row=2, column=3, sticky="w", padx=10, pady=(5, 10))
        
        # Frame para avisos e erros
        self.message_frame = ctk.CTkFrame(self, fg_color="transparent", height=0)
        self.message_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=(0, 10))
        
        self._display_messages()

    def _display_messages(self, errors: list[str] | None = None):
        """Exibe as mensagens de aviso e erro."""
        errors = errors or []
        
        # Limpa o frame de mensagens
        for widget in self.message_frame.winfo_children():
            widget.destroy()
            
        # Exibe avisos
        if self.avisos:
            for aviso_text in self.avisos:
                ctk.CTkLabel(self.message_frame, text=aviso_text, text_color="orange", font=("Arial", 10)).pack(anchor="w")

        # Exibe erros
        if errors:
            for error_text in errors:
                ctk.CTkLabel(self.message_frame, text=error_text, text_color="red", font=("Arial", 10)).pack(anchor="w")

    def get_data(self) -> Sessao | None:
        """
        Valida os dados de entrada e retorna um objeto Sessao atualizado.
        Retorna None se houver erro de validação.
        """
        errors = []
        dia_str = self.dia_entry.get()
        horario_str = self.horario_entry.get()
        dia_obj: date | None = None
        horario_obj: time | None = None

        conclusao_marcada = self.conclusao_var.get()
        agendamento_automatico_marcado = self.agendamento_var.get()

        if conclusao_marcada and agendamento_automatico_marcado:
            errors.append("Sessão concluída não pode ser agendada.")

        if not agendamento_automatico_marcado and (not dia_str or not horario_str):
            errors.append("Sessão agendada deve ter dia e horário preenchidos.")

        if dia_str:
            try:
                dia_obj = datetime.strptime(dia_str, "%d/%m/%Y").date()
            except ValueError:
                errors.append("Data inválida. Use o formato DD/MM/AAAA.")

        if horario_str:
            try:
                horario_obj = datetime.strptime(horario_str, "%H:%M").time()
            except ValueError:
                errors.append("Horário inválido. Use o formato HH:MM.")

            if horario_obj and horario_obj >= time(22, 0):
                errors.append("Horário deve ser anterior às 22:00.")
                horario_obj = None

        self._display_messages(errors)
        if errors:
            return None

        nova_sessao = copy(self.sessao)
        nova_sessao.dia = dia_obj
        nova_sessao.horario = horario_obj
        nova_sessao.status_agendamento = not agendamento_automatico_marcado
        nova_sessao.conclusao = conclusao_marcada
        
        return nova_sessao
