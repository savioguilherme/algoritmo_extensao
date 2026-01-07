from inject import autoparams
from interfacegrafica.base_frame import BaseFrame
from interfacegrafica.base_widgets import BaseWidgets
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from CTkMessagebox import CTkMessagebox

class MenuAdministrador(BaseFrame):
     
    """Menu do administrador do sistema"""

    @autoparams()
    def __init__(self, master, user_id, voltar_callback, abrir_menu_senha, cadastro_fisioterapeuta, cadastro_pesquisador, listar_fisioterapeutas, listar_pesquisadores, usuario_service: BaseUsuarioService):
        super().__init__(master, titulo="Menu Administrador")

        self.widgets = BaseWidgets()

        self.voltar_callback = voltar_callback
        self.cadastro_fisioterapeuta = cadastro_fisioterapeuta
        self.cadastro_pesquisador = cadastro_pesquisador
        self.listar_fisioterapeutas = listar_fisioterapeutas
        self.listar_pesquisadores = listar_pesquisadores
        self.abrir_menu_senha = abrir_menu_senha
        
        self.usuario_service = usuario_service
        self.user_id = user_id
        self.usuario_logado = None
        
        # Configurando o frame
        self.grid_rowconfigure((1,2,3), weight=0)
        self.grid_columnconfigure((1,2,3), weight=1)

        self.carregar_usuario_logado()
       
        self.btn_fisioterapeuta = self.widgets.button(self, texto="Cadastrar Fisioterapeuta", comando=self.cadastro_fisioterapeuta, cor="blue")
        self.btn_fisioterapeuta.grid(row=1, column=1, sticky="e", padx=(20,10), pady=(20,10))

        self.btn_pesquisador = self.btn_cadastrar_paci = self.widgets.button(self, texto="Cadastrar Pesquisador", comando=self.cadastro_pesquisador, cor="blue")
        self.btn_pesquisador.grid(row=1, column=2, sticky="w", padx=(10,20), pady=(20,10))

        self.btn_listar_fisioterapeuta = self.widgets.button(self, texto="Listar Fisioterapeutas", comando=self.listar_fisioterapeutas, cor="blue")
        self.btn_listar_fisioterapeuta.grid(row=2, column=1, sticky="e", padx=(20,10), pady=(10,10))

        self.btn_listar_pesquisadores = self.widgets.button(self, texto="Listar Pesquisadores", comando=self.listar_pesquisadores, cor="blue")
        self.btn_listar_pesquisadores.grid(row=2, column=2, sticky="w", padx=(10,20), pady=(10,10))

        self.btn_trocar_senha = self.widgets.button(self, texto="Alterar Senha", comando=self.abrir_janela_trocar_senha, cor="blue")
        self.btn_trocar_senha.grid(row=3, column=1, sticky="e", padx=(20,10), pady=(10,20))

        self.btn_voltar = self.widgets.button(self, texto="Sair", comando=self.voltar_callback, cor="red")
        self.btn_voltar.grid(row=3, column=2, sticky="w", padx=(10,20), pady=(10,20))

    def carregar_usuario_logado(self):
        try:
            self.usuario_logado = self.usuario_service.consultar(self.user_id)
        except Exception as e:
            return None
    
    def abrir_janela_trocar_senha(self):
        self.abrir_menu_senha()

    '''def criar_popup_trocar_senha(self):
        self.janela_senha = ctk.CTkToplevel(self)
        self.janela_senha.title(f"Alterar Senha - {self.usuario_logado.nome}")
        self.janela_senha.geometry("400x350")
        self.janela_senha.resizable(False, False)
        
        # Centralizar
        self.janela_senha.update_idletasks()
        largura = 400
        altura = 350
        x = (self.janela_senha.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela_senha.winfo_screenheight() // 2) - (altura // 2)
        self.janela_senha.geometry(f"{largura}x{altura}+{x}+{y}")
        
        # Tornar a janela focada
        self.janela_senha.focus_set()
        
        # Configurar para fechar com ESC
        self.janela_senha.bind('<Escape>', lambda e: self.janela_senha.destroy())
        
        # Configurar grid
        for i in range(5):
            self.janela_senha.grid_rowconfigure(i, weight=1)
        self.janela_senha.grid_columnconfigure((0,1), weight=1)
        
        # Título
        titulo = self.widgets.label_titulo_popup(
            self.janela_senha,
            f"Alterar Senha"
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Nome do administrador
        nome_label = self.widgets.label_menor(
            self.janela_senha,
            f"Administrador: {self.usuario_logado.nome}",
            fonte=("Arial", 12, "bold")
        )
        nome_label.grid(row=0, column=0, columnspan=2, pady=(30,0))
        
        # Nova Senha
        self.widgets.label_campo(
            self.janela_senha,
            "Nova Senha:"
        ).grid(row=1, column=0, padx=10, pady=15, sticky="e")
        
        self.entry_nova_senha = self.widgets.entry_senha(
            self.janela_senha,
            "Digite a nova senha"
        )
        self.entry_nova_senha.grid(row=1, column=1, padx=10, pady=15, sticky="w")
        
        # Confirmar Nova Senha
        self.widgets.label_campo(
            self.janela_senha,
            "Confirmar Senha:"
        ).grid(row=2, column=0, padx=10, pady=15, sticky="e")
        
        self.entry_confirmar_senha = self.widgets.entry_senha(
            self.janela_senha,
            "Confirme a nova senha"
        )
        self.entry_confirmar_senha.grid(row=2, column=1, padx=10, pady=15, sticky="w")
        
        # Frame para botões
        frame_botoes = self.widgets.frame_botoes(self.janela_senha)
        frame_botoes.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Botão Salvar
        self.widgets.button_menor(
            frame_botoes,
            "Salvar",
            self.trocar_senha_simplificado,
            "green",
            fonte=("Arial", 14, "bold"),
            largura=120
        ).grid(row=0, column=0, padx=10)
        
        # Botão Cancelar
        self.widgets.button_menor(
            frame_botoes,
            "Cancelar",
            self.janela_senha.destroy,
            "red",
            fonte=("Arial", 14, "bold"),
            largura=120
        ).grid(row=0, column=1, padx=10)
        
        # Label para mensagens
        self.label_mensagem = self.widgets.label_menor(
            self.janela_senha,
            "",
            "transparent"
        )
        self.label_mensagem.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Focar no primeiro campo
        self.janela_senha.after(100, lambda: self.entry_nova_senha.focus_set())

    def trocar_senha_simplificado(self):
        """Processa a troca de senha sem verificar senha antiga"""
        # Obter valores dos campos
        nova_senha = self.entry_nova_senha.get()
        confirmar_senha = self.entry_confirmar_senha.get()
        
        # Validações básicas
        if not nova_senha or not confirmar_senha:
            self.label_mensagem.configure(text="Preencha todos os campos!", text_color="red")
            return
        
        if nova_senha != confirmar_senha:
            self.label_mensagem.configure(text="As senhas não coincidem!", text_color="red")
            return
        
        if len(nova_senha) < 6:
            self.label_mensagem.configure(text="A senha deve ter pelo menos 6 caracteres!", text_color="red")
            return
        
        try:
            import bcrypt
            
            # Gerar novo hash para a nova senha
            nova_senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Atualizar a senha no objeto do administrador
            self.usuario_logado.senha = nova_senha_hash
            
            # Atualizar no banco de dados
            self.usuario_service.atualizar_adm(self.usuario_logado)
            
            # Sucesso
            self.label_mensagem.configure(text="✓ Senha alterada com sucesso!", text_color="green")
            
            # Limpar campos
            self.entry_nova_senha.delete(0, 'end')
            self.entry_confirmar_senha.delete(0, 'end')
            
            # Fechar janela após 2 segundos
            self.janela_senha.after(2000, self.fechar_janela_com_sucesso)
            
        except Exception as e:
            self.label_mensagem.configure(text=f"Erro: {str(e)}", text_color="red")'''