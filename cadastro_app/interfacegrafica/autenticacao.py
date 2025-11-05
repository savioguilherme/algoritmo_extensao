from armazenamento.armazenamento import Armazenamento

class Autenticacao:
    
    """Realiza autenticação de usuários (administrador, pesquisador ou fisioterapeuta)."""

    def __init__(self, usuario: str, senha: str):
        # Instancia de armazemaento
        self.guardar = Armazenamento()
        #usuario e senha recebidos da classe login
        self.usuario = usuario
        self.senha = senha

    # Verifica se o usuário e senha existem em alguma das abas do Excel.
    def verificar(self):
        abas = ["administradores", "fisioterapeutas", "pesquisadores", "pacientes"]

        for aba in abas:
            try:
                df = self.guardar.carregar(aba)

                # Se a aba não tiver colunas de login/senha, pula
                if "Login" not in df.columns or "Senha" not in df.columns:
                    continue

                # Verifica se existe correspondência
                usuario_encontrado = df[
                    (df["Login"] == self.usuario) & (df["Senha"] == self.senha)
                ]

                if not usuario_encontrado.empty:
                    nome = usuario_encontrado.iloc[0]["Nome"]
                    return {
                        "autenticado": True,
                        "tipo": aba,
                        "nome": nome,
                    }

            except Exception as e:
                print(f"Erro ao verificar aba {aba}: {e}")

        # Se nenhuma aba tiver correspondência
        return {
            "autenticado": False,
            "tipo": None,
            "nome": None,
        }
