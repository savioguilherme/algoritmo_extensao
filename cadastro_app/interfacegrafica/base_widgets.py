import customtkinter as ctk

class BaseWidgets():

    '''Classe que fornece uma padrão para todos os widgets a serem utilizados a fim de evitar redundancias no codigo'''

    def label(self, janela, texto, cor):
        return ctk.CTkLabel(
            master=janela,
            text=texto,
            width=100,
            height=25,
            corner_radius=10,
            fg_color=cor,
            text_color="black",
            font=("Arial", 20, "bold"),
            padx=1,
            pady=1,
        )
    
    def entry(self, janela, simbolo):
        return ctk.CTkEntry(
            master=janela,
            width=200,
            height=50,
            corner_radius=10,
            text_color="black",
            font=("Arial", 20, "bold"),
            state="normal",
            show=simbolo,
        )
    
    def button(self, janela, texto, comando, cor):
        return ctk.CTkButton(
            master=janela,
            width=200,
            height=50,
            corner_radius=10,
            fg_color=cor,
            text=texto,
            font=("Arial", 20, "bold"),
            command=comando,
        )
    
    def frame(self, janela):
        return ctk.CTkFrame(
            master=janela, 
            fg_color="transparent"
        )
    
    def option_menu(self, janela, opcoes, comando): 
        return ctk.CTkOptionMenu(
            master=janela, 
            values=opcoes, 
            command=comando,
            width=200,
            height=50,
            text_color="black",
            font=("Arial", 20, "bold"),
        )
    
    def switch(self, janela, texto, comando=None):
        return ctk.CTkSwitch(
            master=janela,
            text=texto,
            command=comando,
            text_color="black",
            font=("Arial", 20, "bold"),
        )