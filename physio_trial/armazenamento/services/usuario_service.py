import bcrypt

from inject import autoparams

from armazenamento.context.app_context import current_user_id
from armazenamento.context.app_context import current_user_type
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.decorators.auth_method import auth_method

from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

class UsuarioService(BaseUsuarioService):

    @autoparams()
    def __init__(self, dal: DataAccessLayer):
        super().__init__(dal)

    def login(self, username: str, password: str) -> int | None:
        byted_password = b'' + password.encode('utf-8')

        user_data: Administrador | Fisioterapeuta | Pesquisador | None = self._dal.call_function(
            "ufn_usuario_consultar_por_login",
            p_login=username
        )

        hashed_password = user_data['senha'] if user_data is not None else None

        if hashed_password is None:
            raise PermissionError("Login inválido.")

        elif bcrypt.checkpw(byted_password, hashed_password.encode('utf-8')):
            user_id = user_data['id_usuario']
            current_user_id.set(user_id)
            current_user_type.set(user_data['tipo'])
            return user_id

        raise PermissionError("Senha inválida.")

    def logout(self) -> None:
        current_user_type.set(None)
        current_user_id.set(None)

    @auth_method
    def listar_usuarios(self, lista_tipos: list[int]) -> list[Administrador | Fisioterapeuta | Pesquisador]:
        return self._dal.usuario_dal.listar_usuarios(lista_tipos)

    # fazer um só retorna usuário
    @auth_method
    def consultar_adm(self, id_adm: int):
        return self._dal.usuario_dal.consultar_adm(id_adm)

    @auth_method
    def inserir_adm(self, adm: Administrador) -> int:
        result = self._dal.call_procedure(
            "usp_usuario_inserir",
            p_email=adm.email,
            p_nome=adm.nome,
            p_data_nascimento=adm.data_nascimento,
            p_tipo=adm.tipo,
            p_login=adm.login,
            p_senha=bcrypt.hashpw(adm.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=adm.status_pessoa,
            p_id_usuario=None
        )

        if result is not None:
            return result['p_id_usuario']
        
        return None

    @auth_method
    def atualizar_adm(self, adm: Administrador) -> None:
        self._dal.usuario_dal.atualizar_adm(adm)

    @auth_method
    def consultar_fisioterapeuta(self, id_fisio: int):
        return self._dal.usuario_dal.consultar_fisioterapeuta(id_fisio)

    @auth_method
    def inserir_fisioterapeuta(self, fisio: Fisioterapeuta) -> int:
        return self._dal.usuario_dal.inserir_fisioterapeuta(fisio)

    @auth_method
    def atualizar_fisioterapeuta(self, fisio: Fisioterapeuta) -> None:
        self._dal.usuario_dal.atualizar_fisioterapeuta(fisio)

    @auth_method
    def consultar_pesquisador(self, id_pesq: int):
        return self._dal.usuario_dal.consultar_pesquisador(id_pesq)

    @auth_method
    def inserir_pesquisador(self, pesq: Pesquisador) -> int:
        return self._dal.usuario_dal.inserir_pesquisador(pesq)

    @auth_method
    def atualizar_pesquisador(self, pesq: Pesquisador) -> None:
        self._dal.call_procedure()

    @auth_method
    def deletar_usuario(self, id_usuario_desativado: int) -> None:
        return self._dal.call_procedure(
            "usp_usuario_deletar",
            p_id_usuario_desativado=id_usuario_desativado
        )
