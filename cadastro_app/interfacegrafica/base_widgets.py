import customtkinter as ctk

class BaseWidgets():
    def __init__(self):
        pass
    def label(self, janela, texto_var):
        return ctk.CTkLabel(
            master=janela,
            text=texto_var,
            #textvariable=texto_var,
            font=("Arial", 20, "bold"),
            #text_color="#0077ff",
            fg_color="transparent",
            width=200,
            height=40,
            corner_radius=10,
            anchor="center",
            justify="center",
            padx=10,
            pady=5,
            #cursor="hand2"
        )