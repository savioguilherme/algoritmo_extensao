import customtkinter

class BaseFrame(customtkinter.CTkFrame):

    """Superclasse que controla layout e centralização das telas"""

    def __init__(self, master, titulo=""):
        super().__init__(master)

        #frame de fundo
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        # frame principal onde são construidos os widgets das subclasses
        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, padx=20, pady=20)
        self.container.grid_columnconfigure((0,1,2,3), weight=1)
        self.container.grid_rowconfigure((0,1,2,3), weight=0)

        if titulo:
            self.label_titulo = customtkinter.CTkLabel(self.container, text=titulo, width=250, height=40, font=("Arial", 45, "bold"))
            self.label_titulo.grid(row=0, column=0, columnspan=4, padx=20, pady=(10,20), sticky="nsew")