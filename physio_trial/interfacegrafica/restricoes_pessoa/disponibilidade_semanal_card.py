import customtkinter as ctk
from datetime import time, datetime

class DisponibilidadeSemanalCard(ctk.CTkFrame):
    def __init__(self, parent, day=datetime.now().weekday(), time_obj=datetime.now().time(), delete_callback=None):
        super().__init__(parent)
        
        # Estilo
        self.configure(fg_color=["#EBEBEB", "#2B2B2B"], corner_radius=10)

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
        try:
            weekday = self.days.index(self.weekday_var.get())
            time_components = [int(x) for x in self.time_entry.get().split(":")]

            time_obj = time(*time_components)
            return (weekday, time_obj)

        except (ValueError, TypeError):
            return None



