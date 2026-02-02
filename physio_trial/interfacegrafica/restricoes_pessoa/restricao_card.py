import customtkinter as ctk
from datetime import datetime, time

class RestricaoCard(ctk.CTkFrame):
    def __init__(self, parent, data=datetime.now(), delete_callback=None):
        super().__init__(parent)

        # Estilo
        self.configure(fg_color=["#EEEEEE", "#222222"], corner_radius=10)

        # Grid
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(4, weight=0)

        # Dia
        self.lbl_date = ctk.CTkLabel(self, text="Dia (DD/MM/AAAA):", font=("Arial", 12))
        self.lbl_date.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        self.date_entry = ctk.CTkEntry(self, width=90, placeholder_text="DD/MM/AAAA")
        self.date_entry.insert(0, data.strftime("%d/%m/%Y"))
        self.date_entry.grid(row=0, column=1, padx=(5, 15), pady=(10, 5))

        # Horário
        self.lbl_time = ctk.CTkLabel(self, text="Horário (HH:MM):", font=("Arial", 12))
        self.lbl_time.grid(row=0, column=2, sticky="w", padx=15, pady=(10, 5))

        self.time_entry = ctk.CTkEntry(self, width=60, placeholder_text="HH:MM")
        self.time_entry.insert(0, data.strftime("%H:%M"))
        self.time_entry.grid(row=0, column=3, padx=(5, 15), pady=(10, 5))

        # Botão de deletar
        self.set_delete_callback(delete_callback)
        self.delete_button = ctk.CTkButton(self, text="X", width=30, command=self.delete)
        self.delete_button.grid(row=0, column=4, padx=(5, 15), pady=(10, 5))

        self.error_frame = None

    def set_delete_callback(self, delete_callback):
        self.delete_callback = delete_callback

    def delete(self):
        if self.delete_callback:
            self.delete_callback()

    def get_data(self):
        """
        Returns a Python datetime object.
        Returns None if the date is invalid.
        """

        if self.error_frame:
            self.error_frame.destroy()
        errors = []

        date_str = self.date_entry.get()
        time_str = self.time_entry.get()
        date_obj = None
        time_obj = None

        # Validate date
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            errors.append("Data inválida.")

        # Validate time
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            errors.append("Horário inválido.")

        # Check time constraint
        if time_obj and time_obj >= time(22, 0):
            errors.append("Horário deve ser anterior às 22:00.")
            time_obj = None # Invalidate to prevent combination

        if errors:
            self.error_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.error_frame.grid(row=1, column=0, columnspan=5, sticky="ew", padx=15, pady=(0, 10))
            for error_text in errors:
                ctk.CTkLabel(self.error_frame, text=error_text, text_color="red", font=("Arial", 10)).pack(anchor="w")
            return None

        if date_obj and time_obj:
            return datetime.combine(date_obj, time_obj)

        return None
