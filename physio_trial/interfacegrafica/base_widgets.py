import customtkinter as ctk

class BaseWidgets():

    '''Classe que fornece uma padrão para todos os widgets a serem utilizados a fim de evitar redundancias no codigo'''

    def label(self, janela, texto, cor):
        return ctk.CTkLabel(
            master=janela,
            text=texto,
            width=200,
            height=50,
            corner_radius=10,
            fg_color=cor,
            text_color="black",
            font=("Arial", 20, "bold"),
            padx=1,
            pady=1,
        )
    
    def entry(self, janela, simbolo, placeholder):
        return ctk.CTkEntry(
            master=janela,
            width=200,
            height=50,
            corner_radius=10,
            text_color="black",
            font=("Arial", 20, "bold"),
            state="normal",
            show=simbolo,
            placeholder_text=placeholder,
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
    
    def option_menu(self, janela, values, command): 
        return ctk.CTkOptionMenu(
            master=janela, 
            values=values, 
            command=command,
            width=250,
            height=75,
            text_color="black",
            font=("Arial", 25, "bold"),
            fg_color="#f0f0f0",  # Fundo do botão transparente
            bg_color="transparent",  # Fundo do widget transparente
            button_color="#e0e0e0",  # Cor do botão
            button_hover_color="#d0d0d0",  # Cor do botão ao passar mouse
            dropdown_font=("Arial", 25, "bold"),  # Mesma fonte
            dropdown_hover_color="#c0c0c0",  # Cor ao passar mouse
            dropdown_text_color="black",  # Cor do texto
            dynamic_resizing=True  # Impede redimensionamento automático

        )
    
    def switch(self, janela, texto, comando=None):
        return ctk.CTkSwitch(
            master=janela,
            text=texto,
            command=comando,
            text_color="black",
            font=("Arial", 20, "bold"),
        )