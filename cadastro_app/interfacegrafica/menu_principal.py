import customtkinter
from interfacegrafica.base_frame import BaseFrame

class MenuPrincipal(BaseFrame):

    """Menu principal"""

    def __init__(self, master, abrir_menu_administrador, abrir_menu_fisioterapeuta, abrir_menu_pesquisador, encerrar):
        super().__init__(master, "Menu Principal")

        self.abrir_menu_administrador = abrir_menu_administrador
        self.abrir_menu_fisioterapeuta = abrir_menu_fisioterapeuta
        self.abrir_menu_pesquisador = abrir_menu_pesquisador
        self.encerrar = encerrar

        # Configuração interna dos botões
        botoes = [
            ("Pesquisador", self.abrir_menu_pesquisador),
            ("Fisioterapeuta", self.abrir_menu_fisioterapeuta),
            ("Administrador", self.abrir_menu_administrador),
            ("Encerrar", self.encerrar)
        ]

        for i, (texto, comando) in enumerate(botoes):

            cor = "red" if texto == "Encerrar" else None
    
            botao_menu = customtkinter.CTkButton(self.container, text=texto, width=250, height=40, command=comando, font=("Arial", 20, "bold"), fg_color=cor)
            botao_menu.grid(row=1, column=i, padx=20, pady=20)
           