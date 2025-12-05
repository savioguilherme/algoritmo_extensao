import customtkinter as ctk

class BaseWidgets():

    '''Classe que fornece uma padrão para todos os widgets a serem utilizados a fim de evitar redundancias no codigo'''

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
    def entry(self, janela, texto, cor):
        return ctk.CTkEntry(
            master=janela,
            #textvariable=texto_var,
            text=texto,
            width=200,
            height=50,
            corner_radius=10,
            fg_color=cor,
            text_color="black",
            #placeholder_text_color=,
            #placeholder_text=,
            font=("Arial", 20, "bold"),
            state="normal",
        )
    def button(self, janela, texto, cor):
        return ctk.CTkButton(
            master=janela,
            width=200,
            height=50,
            corner_radius=10,
            #border_width=,
            #border_spacing=,
            fg_color=cor,
            #hover_color=,
            #border_color=,
            #text_color="#0077ff",
            #placeholder_text_color=,
            #placeholder_text=,
            #textvariable=texto_var,
            text=texto,
            #font=,
            #state=,
            #hover=,
            #command=,
            #compound=,
            #anchor=,
        )