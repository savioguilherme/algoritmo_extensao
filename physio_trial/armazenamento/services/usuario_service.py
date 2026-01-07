import bcrypt

from psycopg.types.json import Jsonb
from inject import autoparams
from datetime import datetime, time

from armazenamento.context.app_context import current_user_id, current_user_type, current_user_types_list, current_session_codes_list
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.services.base.base_usuario_tipo_service import BaseUsuarioTipoService
from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService
from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.decorators.auth_method import auth_method

from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

from greedy.wrapper import wrapper

class UsuarioService(BaseUsuarioService):

    @autoparams()
    def __init__(
        self,
        dal: DataAccessLayer,
        user_type_service: BaseUsuarioTipoService, 
        codigo_sessao_service: BaseCodigoSessaoService
    ):
        super().__init__(dal)
        self._user_type_service = user_type_service
        self._codigo_sessao_service = codigo_sessao_service

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
            current_session_codes_list.set(self._codigo_sessao_service.listar_codigos_sessoes())
            return user_id

        raise PermissionError("Senha inválida.")

    @auth_method
    def logout(self) -> None:
        current_user_type.set(None)
        current_user_id.set(None)
        current_user_types_list.set(None)
        current_session_codes_list.set(None)

    @auth_method
    def listar_usuarios(self, lista_tipos: list[int], apenas_ativos: bool) -> list[Administrador | Fisioterapeuta | Pesquisador]:
        result = self._dal.call_function(
            "ufn_usuario_listar",
            p_apenas_ativos=apenas_ativos,
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
                fisio: Fisioterapeuta = Fisioterapeuta(
                    id_fisioterapeuta=row['id_usuario'],
                    nome_fisioterapeuta=row['nome'],
                    email=row['email'],
                    data_nascimento=row['data_nascimento'],
                    tipo=user_types_list[1],
                    login=row['login'],
                    senha=row['senha'],
                    status_fisioterapeuta=row['ativo']
                )

                fisio.restricoes_fisioterapeuta.disponibilidade_semanal = [set() for _ in range(7)]

                for disp in row["disponibilidades"] or []:
                    dia: int = disp["dia"]           # 0..6
                    horarios = disp["horarios"]      # list[str]

                    fisio.restricoes_fisioterapeuta.disponibilidade_semanal[dia] = {
                        time.fromisoformat(h) for h in horarios
                    }

                restricoes: set[datetime] = set(row['restricoes'] or [])

                fisio.restricoes_fisioterapeuta.restricoes = restricoes

                final_list.append(fisio)
            elif row_type == user_types_list[2]:
                pesq: Pesquisador = Pesquisador(
                    id_pesquisador=row['id_usuario'],
                    nome_pesquisador=row['nome'],
                    email=row['email'],
                    data_nascimento=row['data_nascimento'],
                    tipo=user_types_list[2],
                    login=row['login'],
                    senha=row['senha'],
                    status_pesquisador=row['ativo']
                )

                pesq.restricoes_pesquisador.disponibilidade_semanal = [set() for _ in range(7)]

                for disp in row["disponibilidades"] or []:
                    dia: int = disp["dia"]           # 0..6
                    horarios = disp["horarios"]      # list[str]

                    pesq.restricoes_pesquisador.disponibilidade_semanal[dia] = {
                        time.fromisoformat(h) for h in horarios
                    }

                restricoes: set[datetime] = set(row['restricoes'] or [])

                pesq.restricoes_pesquisador.restricoes = restricoes

                final_list.append(pesq)
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
        
        disponibilidade_semanal: list[set[time]] = [set() for _ in range(7)] if result['tipo'] in (user_types_list[1], user_types_list[2]) else []

        for disp in result["disponibilidades"] or []:
            dia: int = disp["dia"]           # 0..6
            horarios = disp["horarios"]      # list[str]

            disponibilidade_semanal[dia] = {
                time.fromisoformat(h) for h in horarios
            }

        restricoes: set[datetime] = set(result['restricoes'] or [])

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
            self._definir_restricoes_usuario(
            self._definir_disponibilidade_semanal_usuario(Fisioterapeuta(
                id_fisioterapeuta=result['id_usuario'],
                nome_fisioterapeuta=result['nome'],
                email=result['email'],
                data_nascimento=result['data_nascimento'],
                tipo=user_types_list[1],
                login=result['login'],
                senha=result['senha'],
                status_fisioterapeuta=result['ativo']
            ), disponibilidade_semanal=disponibilidade_semanal), restricoes=restricoes)
            if result['tipo'] == user_types_list[1] else (
                self._definir_restricoes_usuario(
                self._definir_disponibilidade_semanal_usuario(Pesquisador(
                    id_pesquisador=result['id_usuario'],
                    nome_pesquisador=result['nome'],
                    email=result['email'],
                    data_nascimento=result['data_nascimento'],
                    tipo=user_types_list[2],
                    login=result['login'],
                    senha=result['senha'],
                    status_pesquisador=result['ativo']
                ), disponibilidade_semanal=disponibilidade_semanal), restricoes=restricoes)
                if result['tipo'] == user_types_list[2] else None
            )
        )

    @auth_method
    def inserir_adm(self, adm: Administrador) -> int:
        result = self._dal.call_procedure(
            "usp_usuario_inserir",
            p_email=adm.email,
            p_nome=adm.nome,
            p_data_nascimento=adm.data_nascimento.isoformat(),
            p_tipo=current_user_types_list.get()[0],
            p_login=adm.login,
            p_senha=bcrypt.hashpw(adm.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=adm.status_pessoa,
            p_disponibilidades=None,
            p_restricoes=None,
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
            p_data_nascimento=adm.data_nascimento.isoformat(),
            p_login=adm.login,
            p_senha=bcrypt.hashpw(adm.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=adm.status_pessoa,
            p_disponibilidades=None,
            p_restricoes=None
        )

    @auth_method
    def inserir_fisioterapeuta(self, fisio: Fisioterapeuta) -> int:
        result = self._dal.call_procedure(
            "usp_usuario_inserir",
            p_email=fisio.email,
            p_nome=fisio.nome,
            p_data_nascimento=fisio.data_nascimento.isoformat(),
            p_tipo=current_user_types_list.get()[1],
            p_login=fisio.login,
            p_senha=bcrypt.hashpw(fisio.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=fisio.status_pessoa,
            p_disponibilidades=Jsonb(
                [
                    {"dia": dia, "horarios": [h.isoformat() for h in horarios]}
                    for dia, horarios in enumerate(fisio.restricoes_fisioterapeuta.disponibilidade_semanal)
                ]
            ),
            p_restricoes=Jsonb([dt.isoformat() for dt in fisio.restricoes_fisioterapeuta.restricoes]),
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
            p_data_nascimento=fisio.data_nascimento.isoformat(),
            p_login=fisio.login,
            p_senha=bcrypt.hashpw(fisio.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=fisio.status_pessoa,
            p_disponibilidades=Jsonb(
                [
                    {"dia": dia, "horarios": [h.isoformat() for h in horarios]}
                    for dia, horarios in enumerate(fisio.restricoes_fisioterapeuta.disponibilidade_semanal)
                ]
            ),
            p_restricoes=Jsonb([dt.isoformat() for dt in fisio.restricoes_fisioterapeuta.restricoes])
        )

        _ = wrapper()

    @auth_method
    def inserir_pesquisador(self, pesq: Pesquisador) -> int:
        result = self._dal.call_procedure(
            "usp_usuario_inserir",
            p_email=pesq.email,
            p_nome=pesq.nome,
            p_data_nascimento=pesq.data_nascimento.isoformat(),
            p_tipo=current_user_types_list.get()[2],
            p_login=pesq.login,
            p_senha=bcrypt.hashpw(pesq.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=pesq.status_pessoa,
            p_disponibilidades=Jsonb(
                [
                    {"dia": dia, "horarios": [h.isoformat() for h in horarios]}
                    for dia, horarios in enumerate(pesq.restricoes_pesquisador.disponibilidade_semanal)
                ]
            ),
            p_restricoes=Jsonb([dt.isoformat() for dt in pesq.restricoes_pesquisador.restricoes]),
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
            p_data_nascimento=pesq.data_nascimento.isoformat(),
            p_login=pesq.login,
            p_senha=bcrypt.hashpw(pesq.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            p_ativo=pesq.status_pessoa,
            p_disponibilidades=Jsonb(
                [
                    {"dia": dia, "horarios": [h.isoformat() for h in horarios]}
                    for dia, horarios in enumerate(pesq.restricoes_pesquisador.disponibilidade_semanal)
                ]
            ),
            p_restricoes=Jsonb([dt.isoformat() for dt in pesq.restricoes_pesquisador.restricoes])
        )

        _ = wrapper()

    @auth_method
    def deletar_usuario(self, id_usuario_desativado: int) -> None:
        return self._dal.call_procedure(
            "usp_usuario_deletar",
            p_id_usuario_desativado=id_usuario_desativado
        )
    
    def _definir_restricoes_usuario(self, usuario: Fisioterapeuta | Pesquisador, restricoes: set[datetime]) -> Fisioterapeuta | Pesquisador:
        if isinstance(usuario, Fisioterapeuta):
            usuario.restricoes_fisioterapeuta.restricoes = restricoes
        elif isinstance(usuario, Pesquisador):
            usuario.restricoes_pesquisador.restricoes = restricoes
        else:
            raise TypeError("Tipo de usuário inválido para definir restrições.")

        return usuario

    def _definir_disponibilidade_semanal_usuario(self, usuario: Fisioterapeuta | Pesquisador, disponibilidade_semanal: list[set[time]]) -> Fisioterapeuta | Pesquisador:
        if isinstance(usuario, Fisioterapeuta):
            usuario.restricoes_fisioterapeuta.disponibilidade_semanal = disponibilidade_semanal
        elif isinstance(usuario, Pesquisador):
            usuario.restricoes_pesquisador.disponibilidade_semanal = disponibilidade_semanal
        else:
            raise TypeError("Tipo de usuário inválido para definir disponibilidade semanal.")

        return usuario
