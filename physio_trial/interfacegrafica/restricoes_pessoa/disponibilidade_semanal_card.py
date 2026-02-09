import customtkinter as ctk
from datetime import time, datetime

class DisponibilidadeSemanalCard(ctk.CTkFrame):
    def __init__(self, parent, day=datetime.now().weekday(), time_obj=datetime.now().time(), delete_callback=None):
        super().__init__(parent)
        
        # Estilo
        self.configure(fg_color=["#EEEEEE", "#222222"], corner_radius=10)

        # Grid
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(4, weight=0)

        # Dia da semana
        self.lbl_date = ctk.CTkLabel(self, text="Dia da semana:", font=("Arial", 12))
        self.lbl_date.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        self.days = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]

        self.weekday_var = ctk.StringVar(value=self.days[day])
        self.weekday_menu = ctk.CTkOptionMenu(self, values=self.days, variable=self.weekday_var)
        self.weekday_menu.grid(row=0, column=1, padx=(5, 15), pady=(10, 5))

        # Horário
        self.lbl_time = ctk.CTkLabel(self, text="Horário (HH:MM):", font=("Arial", 12))
        self.lbl_time.grid(row=0, column=2, sticky="w", padx=15, pady=(10, 5))

        self.time_entry = ctk.CTkEntry(self, width=60, placeholder_text="HH:MM")
        self.time_entry.insert(0, time_obj.strftime("%H:%M"))
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
        Returns a tuple (weekday, time).
        `weekday` is an integer from 0 (Monday) to 6 (Sunday).
        `time` is a Python time object.
        Returns None if the format is invalid.
        """

        if self.error_frame:
            self.error_frame.destroy()
        errors = []

        time_str = self.time_entry.get()
        time_obj = None
        weekday = None

        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            errors.append("Horário inválido.")

        if time_obj and time_obj >= time(22, 0):
            errors.append("Horário deve ser anterior às 22:00.")
            time_obj = None

        try:
            weekday = self.days.index(self.weekday_var.get())
        except ValueError:
            errors.append("Dia da semana inválido.")

        if errors:
            self.error_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.error_frame.grid(row=1, column=0, columnspan=5, sticky="ew", padx=15, pady=(0, 10))
            for error_text in errors:
                ctk.CTkLabel(self.error_frame, text=error_text, text_color="red", font=("Arial", 10)).pack(anchor="w")
            return None

        return (weekday, time_obj)



