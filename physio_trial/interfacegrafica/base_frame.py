import customtkinter

class BaseFrame(customtkinter.CTkFrame):

    """Superclasse que fornece uma frame padrão"""

    def __init__(self, master, titulo):
        super().__init__(master)

        #frame principal
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
       
        if titulo:
            self.label_titulo = customtkinter.CTkLabel(self, text=titulo, width=200, height=50, font=("Arial", 45, "bold"))
            self.label_titulo.grid(row=0, column=0, sticky="nsew", columnspan=5, padx=20, pady=20)