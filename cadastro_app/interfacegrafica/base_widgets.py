import customtkinter 

class BaseWidgets():

    '''  '''

    def __init__(self, nome_var, var):
        self.nome_var = nome_var; 
        self.var = var
        self.label()
    
    def label(self):
        self.nome_var = customtkinter.CTkLabel(self.var, text="Login: ", font=("Arial", 20, "bold"))
        self.nome_var.grid(row=1, column=0, sticky="e", padx=20, pady=10)
    
    def botao(self): 
        pass
