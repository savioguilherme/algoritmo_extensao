import customtkinter as ctk
from datetime import datetime

class RestricoesCard(ctk.CTkFrame):
    def __init__(self, parent, data=datetime.now(), delete_callback=None):
        super().__init__(parent)
        
        # Estilo
        self.configure(fg_color=["#EBEBEB", "#2B2B2B"], corner_radius=10)

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
        try:
            date_str = self.date_entry.get()
            time_str = self.time_entry.get()
            
            dt_obj = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
            return dt_obj

        except ValueError:
            return None



