import bcrypt

from inject import autoparams

from armazenamento.context.app_context import current_user_id
from armazenamento.context.app_context import current_user_type
from armazenamento.context.app_context import current_user_types_list
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.services.base.base_usuario_tipo_service import BaseUsuarioTipoService
from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.decorators.auth_method import auth_method

from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

class UsuarioService(BaseUsuarioService):

    @autoparams()
    def __init__(self, dal: DataAccessLayer, user_type_service: BaseUsuarioTipoService):
        super().__init__(dal)
        self._user_type_service = user_type_service

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
            current_user_types_list.set(self._user_type_service.listar_tipos())
            return user_id

        raise PermissionError("Senha inválida.")

    def logout(self) -> None:
        current_user_type.set(None)
        current_user_id.set(None)
        current_user_types_list.set(None)

    @auth_method
    def listar_usuarios(self, lista_tipos: list[int]) -> list[Administrador | Fisioterapeuta | Pesquisador]:
        result = self._dal.call_function(
            "ufn_usuario_listar",
            p_tipos=lista_tipos
        )

        if result is None:
            return []
        
        final_list: list[Administrador | Fisioterapeuta | Pesquisador] = []
        user_types_list: list[int] = current_user_types_list.get() or []

        if len(user_types_list) == 0:
            return final_list

        for row in result:
            row_type: int = row['tipo']
            if row_type not in user_types_list:
                continue
            elif row_type == user_types_list[0]:
                final_list.append(
                    Administrador(
                        id_administrador=row['id_usuario'],
                        nome_administrador=row['nome'],
                        email=row['email'],
                        data_nascimento=row['data_nascimento'],
                        tipo=user_types_list[0],
                        login=row['login'],
                        senha=row['senha'],
                        status_administrador=row['ativo']
                    )
                )
            elif row_type == user_types_list[1]:
                final_list.append(
                    Fisioterapeuta(
                        id_fisioterapeuta=row['id_usuario'],
                        nome_fisioterapeuta=row['nome'],
                        email=row['email'],
                        data_nascimento=row['data_nascimento'],
                        tipo=user_types_list[1],
                        login=row['login'],
                        senha=row['senha'],
                        status_fisioterapeuta=row['ativo']
                    )
                )
            elif row_type == user_types_list[2]:
                final_list.append(
                    Pesquisador(
                        id_pesquisador=row['id_usuario'],
                        nome_pesquisador=row['nome'],
                        email=row['email'],
                        data_nascimento=row['data_nascimento'],
                        tipo=user_types_list[2],
                        login=row['login'],
                        senha=row['senha'],
                        status_pesquisador=row['ativo']
                    )
                )
            else:
                raise Warning(f"Tipo de usuário desconhecido: {row_type}")

        return final_list

    # fazer um só retorna usuário
    @auth_method
    def consultar(self, id: int):
        result = self._dal.call_function("ufn_usuario_consultar", p_id_usuario=id)

        if result is None:
            return None
        
        user_types_list = current_user_types_list.get() or []

        if len(user_types_list) == 0:
            return None

        return Administrador(
            id_administrador=result['id_usuario'],
            nome_administrador=result['nome'],
            email=result['email'],
            data_nascimento=result['data_nascimento'],
            tipo=user_types_list[0],
            login=result['login'],
            senha=result['senha'],
            status_administrador=result['ativo']
        ) if result['tipo'] == user_types_list[0] else (
            Fisioterapeuta(
                id_fisioterapeuta=result['id_usuario'],
                nome_fisioterapeuta=result['nome'],
                email=result['email'],
                data_nascimento=result['data_nascimento'],
                tipo=user_types_list[1],
                login=result['login'],
                senha=result['senha'],
                status_fisioterapeuta=result['ativo']
            ) if result['tipo'] == user_types_list[1] else (
                Pesquisador(
                    id_pesquisador=result['id_usuario'],
                    nome_pesquisador=result['nome'],
                    email=result['email'],
                    data_nascimento=result['data_nascimento'],
                    tipo=user_types_list[2],
                    login=result['login'],
                    senha=result['senha'],
                    status_pesquisador=result['ativo']
                ) if result['tipo'] == user_types_list[2] else None
            )
        )

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
        self._dal.call_procedure(
            "usp_usuario_alterar",
            p_id_usuario=adm.id_pessoa,
            p_email=adm.email,
            p_nome=adm.nome,
            p_data_nascimento=adm.data_nascimento,
            p_login=adm.login,
            p_senha=adm.senha,
            p_ativo=adm.status_pessoa
        )

    @auth_method
    def inserir_fisioterapeuta(self, fisio: Fisioterapeuta) -> int:
        result = self._dal.call_procedure(
            "usp_usuario_inserir",
            p_email=fisio.email,
            p_nome=fisio.nome,
            p_data_nascimento=fisio.data_nascimento,
            p_tipo=fisio.tipo,
            p_login=fisio.login,
            p_senha=bcrypt.hashpw(fisio.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=fisio.status_pessoa,
            p_id_usuario=None
        )

        if result is not None:
            return result['p_id_usuario']
        
        return None

    @auth_method
    def atualizar_fisioterapeuta(self, fisio: Fisioterapeuta) -> None:
        self._dal.call_procedure(
            "usp_usuario_alterar",
            p_id_usuario=fisio.id_pessoa,
            p_email=fisio.email,
            p_nome=fisio.nome,
            p_data_nascimento=fisio.data_nascimento,
            p_login=fisio.login,
            p_senha=fisio.senha,
            p_ativo=fisio.status_pessoa
        )

    @auth_method
    def inserir_pesquisador(self, pesq: Pesquisador) -> int:
        result = self._dal.call_procedure(
            "usp_usuario_inserir",
            p_email=pesq.email,
            p_nome=pesq.nome,
            p_data_nascimento=pesq.data_nascimento,
            p_tipo=pesq.tipo,
            p_login=pesq.login,
            p_senha=bcrypt.hashpw(pesq.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=pesq.status_pessoa,
            p_id_usuario=None
        )

        if result is not None:
            return result['p_id_usuario']
        
        return None

    @auth_method
    def atualizar_pesquisador(self, pesq: Pesquisador) -> None:
        self._dal.call_procedure(
            "usp_usuario_alterar",
            p_id_usuario=pesq.id_pessoa,
            p_email=pesq.email,
            p_nome=pesq.nome,
            p_data_nascimento=pesq.data_nascimento,
            p_login=pesq.login,
            p_senha=pesq.senha,
            p_ativo=pesq.status_pessoa
        )

    @auth_method
    def deletar_usuario(self, id_usuario_desativado: int) -> None:
        return self._dal.call_procedure(
            "usp_usuario_deletar",
            p_id_usuario_desativado=id_usuario_desativado
        )
