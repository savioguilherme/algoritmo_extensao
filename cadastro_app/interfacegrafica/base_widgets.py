import customtkinter as ctk

class BaseWidgets():
    def __init__(self):
        pass
    def label(self, janela, texto, cor):
        return ctk.CTkLabel(
            master=janela,
            #textvariable=texto_var,
            text=texto,
            width=200,
            height=50,
            corner_radius=10,
            fg_color=cor,
            #text_color="#0077ff",
            font=("Arial", 20, "bold"),
            #compound="top"
            #justify="center",
            padx=1,
            pady=1,
        )